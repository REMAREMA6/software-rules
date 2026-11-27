'use strict';

const { Queue, QueueEvents, Worker } = require('./dist/cjs');
const IORedis = require('ioredis');
const { randomUUID } = require('node:crypto');

const redisOptions = {
  host: process.env.REDIS_HOST || '127.0.0.1',
  port: Number(process.env.REDIS_PORT || 6379),
  maxRetriesPerRequest: null,
};

async function runScenario(label, { attempts, backoffStrategy, processor }) {
  const queueName = `software-rules-${label}-${randomUUID()}`;
  const queueConnection = new IORedis(redisOptions);
  const workerConnection = new IORedis(redisOptions);
  const eventsConnection = new IORedis(redisOptions);
  const queue = new Queue(queueName, { connection: queueConnection });
  const events = new QueueEvents(queueName, { connection: eventsConnection });
  const trace = [];
  const startedAt = Date.now();
  let processorAttempts = 0;
  const strategyAttempts = [];

  const worker = new Worker(queueName, async job => {
    processorAttempts += 1;
    trace.push({ event: 'processor', attempt: processorAttempts, attemptsMade: job.attemptsMade, atMs: Date.now() - startedAt });
    return processor(job);
  }, {
    connection: workerConnection,
    settings: {
      backoffStrategy: (attemptsMade, type, error, job) => {
        strategyAttempts.push(attemptsMade);
        const delayMs = backoffStrategy(attemptsMade, type, error, job);
        trace.push({ event: 'backoff', attemptsMade, type, error: error.message, jobId: job.id, atMs: Date.now() - startedAt });
        trace.push({ event: 'backoff-result', attemptsMade, delayMs, atMs: Date.now() - startedAt });
        return delayMs;
      },
    },
  });

  for (const eventName of ['waiting', 'delayed', 'failed', 'completed']) {
    events.on(eventName, data => trace.push({ event: `queue:${eventName}`, data, atMs: Date.now() - startedAt }));
  }

  await Promise.all([queue.waitUntilReady(), worker.waitUntilReady(), events.waitUntilReady()]);

  const outcome = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`${label}: timed out`)), 12000);
    worker.once('completed', (job, result) => {
      clearTimeout(timer);
      resolve({ terminal: 'completed', jobId: job.id, attemptsMade: job.attemptsMade, result });
    });
    worker.on('failed', (job, error) => {
      if (job && job.attemptsMade >= attempts || error.name === 'UnrecoverableError' || strategyAttempts.at(-1) === -1) {
        clearTimeout(timer);
        resolve({ terminal: 'failed', jobId: job.id, attemptsMade: job.attemptsMade, error: error.message });
      }
    });
    queue.add('probe', { label }, { attempts, backoff: { type: 'software-rules-custom' } })
      .catch(error => {
        clearTimeout(timer);
        reject(error);
      });
  });

  await new Promise(resolve => setTimeout(resolve, 100));
  const job = await queue.getJob(outcome.jobId);
  const finalState = job ? await job.getState() : 'missing';
  const result = {
    label,
    configuredAttempts: attempts,
    processorAttempts,
    strategyAttempts,
    outcome,
    finalState,
    trace,
  };

  await worker.close();
  await events.close();
  await queue.obliterate({ force: true });
  await queue.close();
  // BullMQ close() owns and closes each supplied Redis connection.
  return result;
}

(async () => {
  const results = [];
  results.push(await runScenario('positive-backoff-completes', {
    attempts: 3,
    backoffStrategy: attempt => attempt * 40,
    processor: async job => {
      if (job.attemptsMade < 2) throw new Error('transient');
      return 'ok';
    },
  }));
  results.push(await runScenario('minus-one-suppresses-retry', {
    attempts: 3,
    backoffStrategy: () => -1,
    processor: async () => { throw new Error('stop'); },
  }));
  results.push(await runScenario('zero-delay-respects-attempt-limit', {
    attempts: 2,
    backoffStrategy: () => 0,
    processor: async () => { throw new Error('always-fails'); },
  }));

  const checks = [
    results[0].processorAttempts === 3 &&
      JSON.stringify(results[0].strategyAttempts) === '[1,2]' &&
      results[0].outcome.terminal === 'completed' &&
      results[0].finalState === 'completed',
    results[1].processorAttempts === 1 &&
      JSON.stringify(results[1].strategyAttempts) === '[1]' &&
      results[1].outcome.terminal === 'failed' &&
      results[1].finalState === 'failed',
    results[2].processorAttempts === 2 &&
      JSON.stringify(results[2].strategyAttempts) === '[1]' &&
      results[2].outcome.terminal === 'failed' &&
      results[2].finalState === 'failed',
  ];

  const report = {
    source: 'BullMQ pinned source checkout',
    sourceCommit: process.env.BULLMQ_SOURCE_COMMIT,
    packageVersion: require('./package.json').version,
    redis: process.env.REDIS_HOST + ':' + process.env.REDIS_PORT,
    checks,
    passed: checks.every(Boolean),
    scenarios: results,
  };
  process.stdout.write(JSON.stringify(report, null, 2) + '\n');
  if (!report.passed) process.exitCode = 1;
})().catch(error => {
  process.stderr.write(error.stack + '\n');
  process.exitCode = 1;
});
