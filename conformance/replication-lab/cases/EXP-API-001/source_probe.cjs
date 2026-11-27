'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const http = require('node:http');
const express = require(process.cwd());

const captureStartedAt = new Date().toISOString();
const app = express();

app.get('/widgets', (req, res) => res.send('get'));
app.put('/widgets', (req, res) => res.send('put'));
app.options('/override', (req, res) => res.set('Allow', 'GET').send('GET'));
app.use((req, res) => res.status(404).send('not found'));

function selectedHeaders(headers) {
  return {
    'content-type': headers.get('content-type'),
    'content-length': headers.get('content-length'),
    allow: headers.get('allow'),
  };
}

async function main() {
  const server = http.createServer(app);
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const requests = [
    ['get-base', 'GET', '/widgets'],
    ['head-fallback', 'HEAD', '/widgets'],
    ['options-auto', 'OPTIONS', '/widgets'],
    ['options-missing', 'OPTIONS', '/missing'],
    ['options-explicit', 'OPTIONS', '/override'],
    ['case-and-trailing-slash', 'GET', '/WIDGETS/'],
    ['query-ignored', 'GET', '/widgets?color=blue'],
  ];
  const scenarios = [];

  try {
    for (const [label, method, path] of requests) {
      const response = await fetch(base + path, { method });
      scenarios.push({
        label,
        request: { method, path },
        response: {
          status: response.status,
          headers: selectedHeaders(response.headers),
          body: await response.text(),
        },
      });
    }
  } finally {
    await new Promise((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
  }

  const lockDigest = fs.existsSync('package-lock.json')
    ? crypto.createHash('sha256').update(fs.readFileSync('package-lock.json')).digest('hex')
    : null;
  const report = {
    capturedAt: captureStartedAt,
    completedAt: new Date().toISOString(),
    source: 'Express pinned source checkout',
    sourceCommit: process.env.EXPRESS_SOURCE_COMMIT,
    packageVersion: require('./package.json').version,
    dependencyLockDigest: lockDigest,
    configuration: {
      caseSensitiveRouting: app.enabled('case sensitive routing'),
      strictRouting: app.enabled('strict routing'),
    },
    scenarios,
  };
  const get = scenarios.find(item => item.label === 'get-base').response;
  const head = scenarios.find(item => item.label === 'head-fallback').response;
  const checks = [
    get.status === 200 && get.body === 'get',
    head.status === 200 && head.body === '' && head.headers['content-length'] === get.headers['content-length'],
    scenarios.find(item => item.label === 'options-auto').response.headers.allow === 'GET, HEAD, PUT',
    scenarios.find(item => item.label === 'options-auto').response.body === 'GET, HEAD, PUT',
    scenarios.find(item => item.label === 'options-missing').response.status === 404,
    scenarios.find(item => item.label === 'options-explicit').response.headers.allow === 'GET',
    scenarios.find(item => item.label === 'options-explicit').response.body === 'GET',
    scenarios.find(item => item.label === 'case-and-trailing-slash').response.status === 200,
    scenarios.find(item => item.label === 'query-ignored').response.status === 200,
    report.configuration.caseSensitiveRouting === false,
    report.configuration.strictRouting === false,
  ];
  report.checks = checks;
  report.passed = checks.every(Boolean);
  process.stdout.write(JSON.stringify(report, null, 2) + '\n');
  if (!report.passed) process.exitCode = 1;
}

main().catch(error => {
  process.stderr.write(error.stack + '\n');
  process.exit(1);
});
