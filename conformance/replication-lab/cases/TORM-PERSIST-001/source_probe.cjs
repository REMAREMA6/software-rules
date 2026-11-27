'use strict';
const { DataSource } = require('/tmp/typeorm/packages/typeorm/build/package/index.js');
async function main() {
  const ds = new DataSource({ type: 'sqljs', autoSave: false, synchronize: false, logging: false });
  await ds.initialize();
  try {
    await ds.query('CREATE TABLE records (id INTEGER PRIMARY KEY, value TEXT NOT NULL)');
    let rollbackError = null;
    let rollbackCallbackResult = null;
    let rowsInsideCallback = [];
    try {
      rollbackCallbackResult = await ds.manager.transaction(async manager => {
        await manager.query('INSERT INTO records(value) VALUES (?)', ['rolled-back']);
        const inside = await manager.query('SELECT id, value FROM records ORDER BY id');
        rowsInsideCallback = inside;
        if (inside.length !== 1 || inside[0].value !== 'rolled-back') throw new Error('transaction-read-your-write-failed');
        throw new Error('forced-transaction-failure');
      });
    } catch (error) { rollbackError = { name: error.name, message: error.message }; }
    const afterRollback = await ds.query('SELECT id, value FROM records ORDER BY id');
    const committedReturn = await ds.manager.transaction(async manager => {
      await manager.query('INSERT INTO records(value) VALUES (?)', ['committed']);
      return 'callback-result';
    });
    const afterCommit = await ds.query('SELECT id, value FROM records ORDER BY id');
    const report = {
      source: 'TypeORM source checkout',
      sourceCommit: process.env.TYPEORM_SOURCE_COMMIT,
      typeormVersion: require('/tmp/typeorm/packages/typeorm/package.json').version,
      driver: 'sqljs',
      scenarios: {
        rollback: { error: rollbackError, callbackResult: rollbackCallbackResult, rowsInsideCallback, rowsAfterRollback: afterRollback },
        commit: { callbackReturn: committedReturn, rowsAfterCommit: afterCommit }
      }
    };
    const checks = [
      rollbackError && rollbackError.name === 'Error' && rollbackError.message === 'forced-transaction-failure',
      rollbackCallbackResult === null,
      afterRollback.length === 0,
      committedReturn === 'callback-result',
      afterCommit.length === 1 && afterCommit[0].value === 'committed'
    ];
    report.checks = checks;
    report.passed = checks.every(Boolean);
    process.stdout.write(JSON.stringify(report, null, 2) + '\n');
    if (!report.passed) process.exitCode = 1;
  } finally { await ds.destroy(); }
}
main().catch(error => { process.stderr.write(error.stack + '\n'); process.exit(1); });
