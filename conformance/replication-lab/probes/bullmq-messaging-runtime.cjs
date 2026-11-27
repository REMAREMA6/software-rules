'use strict';

const { Queue, QueueEvents, Worker } = require('./dist/cjs');
const IORedis = require('ioredis');
const { randomUUID } = require('node:crypto');
const redisOptions = { host: process.env.REDIS_HOST || '127.0.0.1', port: Number(process.env.REDIS_PORT || 6379), maxRetriesPerRequest: null };

async function close(client) {
  if (!client || client.status === 'end') return;
  try { await client.quit(); } catch { client.disconnect(); }
}

async function runScenario(label, configure) {
  const name = `software-rules-message-${label}-${randomUUID()}`;
  const qc = new IORedis(redisOptions), ec = new IORedis(redisOptions), wc = new IORedis(redisOptions);
  const queue = new Queue(name, { connection: qc });
  const events = new QueueEvents(name, { connection: ec });
  const eventNames = [];
  const processed = [];
  let worker;
  try {
    await Promise.all([queue.waitUntilReady(), events.waitUntilReady()]);
    for (const eventName of ['waiting', 'active', 'completed', 'failed']) {
      events.on(eventName, () => eventNames.push(eventName));
    }
    await new Promise(resolve => setTimeout(resolve, 100));
    const setup = await configure(queue);
    worker = new Worker(name, async job => {
      processed.push(job.data.payload);
      if (job.data.fail) throw new Error('consumer-failed');
      return 'acknowledged';
    }, { connection: wc, concurrency: 1, autorun: false });
    await worker.waitUntilReady();
    const terminalPromise = new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error(label + ': worker timed out')), 10000);
      worker.once('completed', (job, result) => { clearTimeout(timer); resolve({ state: 'completed', id: job.id, result }); });
      worker.once('failed', (job, error) => { clearTimeout(timer); resolve({ state: 'failed', id: job && job.id, error: error.message }); });
    });
    worker.run().catch(error => {});
    const terminal = await terminalPromise;
    await new Promise(resolve => setTimeout(resolve, 150));
    const counts = await queue.getJobCounts('waiting', 'active', 'completed', 'failed');
    return { label, setup, processed, terminal, eventNames, counts };
  } finally {
    if (worker) await worker.close(true).catch(() => {});
    await events.close().catch(() => {});
    await queue.obliterate({ force: true }).catch(() => {});
    await queue.close().catch(() => {});
    await Promise.all([close(qc), close(ec), close(wc)]);
  }
}

(async () => {
  const duplicate = await runScenario('duplicate-id-suppression', async queue => {
    const first = await queue.add('deliver', { payload: 'first' }, { jobId: 'stable-message-id' });
    const second = await queue.add('deliver', { payload: 'second' }, { jobId: 'stable-message-id' });
    const stored = await queue.getJob('stable-message-id');
    return {
      firstId: first.id,
      secondId: second.id,
      storedPayload: stored && stored.data.payload,
      storedState: stored ? await stored.getState() : 'missing',
    };
  });
  const failure = await runScenario('consumer-failure', async queue => {
    const job = await queue.add('deliver', { payload: 'failure-case', fail: true }, { jobId: 'failure-message-id', attempts: 1 });
    return { firstId: job.id, storedState: await job.getState() };
  });
  const checks = [
    duplicate.setup.firstId === duplicate.setup.secondId,
    duplicate.setup.storedPayload === 'first',
    duplicate.setup.storedState === 'waiting',
    duplicate.eventNames.join(',') === 'waiting,active,completed',
    JSON.stringify(duplicate.processed) === JSON.stringify(['first']),
    duplicate.terminal.state === 'completed',
    duplicate.counts.completed === 1,
    failure.terminal.state === 'failed',
    failure.terminal.error === 'consumer-failed',
    failure.setup.storedState === 'waiting',
    failure.eventNames.join(',') === 'waiting,active,failed',
    failure.counts.failed === 1,
  ];
  const report = {
    source: 'BullMQ pinned source checkout',
    sourceCommit: process.env.BULLMQ_SOURCE_COMMIT,
    packageVersion: require('./package.json').version,
    capturedAt: new Date().toISOString(),
    scenarios: [duplicate, failure],
    checks,
    passed: checks.every(Boolean),
  };
  process.stdout.write(JSON.stringify(report, null, 2) + '\n');
  if (!report.passed) process.exitCode = 1;
})().catch(error => { process.stderr.write(error.stack + '\n'); process.exit(1); });
