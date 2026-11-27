'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
require('reflect-metadata');

const { DataSource, EntitySchema } = require(require('node:path').resolve(process.cwd(), 'build/compiled'));
const captureStartedAt = new Date().toISOString();

const Post = new EntitySchema({
  name: 'Post',
  tableName: 'post',
  columns: {
    id: { type: Number, primary: true, generated: true },
    title: { type: String, nullable: false },
  },
});

const Category = new EntitySchema({
  name: 'Category',
  tableName: 'category',
  columns: {
    id: { type: Number, primary: true, generated: true },
    name: { type: String, nullable: false },
  },
});

function classifyError(error) {
  const message = String(error && error.message || error);
  return /NOT NULL|constraint failed/i.test(message)
    ? 'integrity-constraint'
    : (error && error.name || 'unknown-error');
}

async function createDataSource() {
  const dataSource = new DataSource({
    type: 'better-sqlite3',
    database: ':memory:',
    entities: [Post, Category],
    synchronize: true,
    logging: false,
  });
  await dataSource.initialize();
  return dataSource;
}

async function runCommitScenario() {
  const dataSource = await createDataSource();
  try {
    const callbackResult = await dataSource.manager.transaction(async manager => {
      const post = await manager.save(Post, { title: 'Post #1' });
      const category = await manager.save(Category, { name: 'Category #1' });
      return { postId: post.id, categoryId: category.id };
    });
    const posts = await dataSource.manager.find(Post);
    const categories = await dataSource.manager.find(Category);
    return {
      label: 'commit-success',
      terminal: 'committed',
      callbackResult,
      postRows: posts.map(row => ({ id: row.id, title: row.title })),
      categoryRows: categories.map(row => ({ id: row.id, name: row.name })),
      postCount: posts.length,
      categoryCount: categories.length,
    };
  } finally {
    await dataSource.destroy();
  }
}

async function runRollbackScenario() {
  const dataSource = await createDataSource();
  let error = null;
  let readsVisibleBeforeFailure = false;
  try {
    try {
      await dataSource.manager.transaction(async manager => {
        const post = await manager.save(Post, { title: 'Post #1' });
        const category = await manager.save(Category, { name: 'Category #1' });
        const loadedPost = await manager.findOneByOrFail(Post, { title: 'Post #1' });
        const loadedCategory = await manager.findOneByOrFail(Category, { name: 'Category #1' });
        readsVisibleBeforeFailure = loadedPost.id === post.id && loadedCategory.id === category.id;
        await manager.save(Post, {});
      });
    } catch (caught) {
      error = caught;
    }

    const posts = await dataSource.manager.find(Post);
    const categories = await dataSource.manager.find(Category);
    return {
      label: 'rollback-on-invalid-post',
      terminal: 'rolled-back',
      errorPropagated: Boolean(error),
      errorCategory: error ? classifyError(error) : 'none',
      readsVisibleBeforeFailure,
      postRowsAfter: posts.map(row => ({ id: row.id, title: row.title })),
      categoryRowsAfter: categories.map(row => ({ id: row.id, name: row.name })),
      postCountAfter: posts.length,
      categoryCountAfter: categories.length,
    };
  } finally {
    await dataSource.destroy();
  }
}

async function main() {
  const pnpmLockPath = require('node:path').resolve(process.cwd(), '../../pnpm-lock.yaml');
  const pnpmLockDigest = fs.existsSync(pnpmLockPath)
    ? crypto.createHash('sha256').update(fs.readFileSync(pnpmLockPath)).digest('hex')
    : null;
  const scenarios = [
    await runCommitScenario(),
    await runRollbackScenario(),
  ];
  const report = {
    capturedAt: captureStartedAt,
    completedAt: new Date().toISOString(),
    source: 'TypeORM pinned source checkout',
    sourceCommit: process.env.TYPEORM_SOURCE_COMMIT,
    packageVersion: require('./package.json').version,
    driver: 'better-sqlite3',
    pnpmVersion: '12.22.0',
    pnpmLockDigest,
    scenarios,
  };
  const commit = scenarios[0];
  const rollback = scenarios[1];
  const checks = [
    commit.terminal === 'committed' && commit.postCount === 1 && commit.categoryCount === 1,
    commit.callbackResult.postId === 1 && commit.callbackResult.categoryId === 1,
    rollback.terminal === 'rolled-back' && rollback.errorPropagated,
    rollback.errorCategory === 'integrity-constraint',
    rollback.readsVisibleBeforeFailure,
    rollback.postCountAfter === 0 && rollback.categoryCountAfter === 0,
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
