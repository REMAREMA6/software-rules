'use strict';

const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const sourceRoot = process.env.MEDUSA_SOURCE_ROOT;
const ts = require(process.env.TYPESCRIPT_PATH || 'typescript');
const sourceFiles = {
  validator: 'packages/modules/pricing/src/utils/validate-price-list-dates.ts',
  dateHelper: 'packages/core/utils/src/common/is-date.ts',
  errorClass: 'packages/core/utils/src/common/errors.ts',
  serviceUsage: 'packages/modules/pricing/src/services/pricing-module.ts',
};

function sha256(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}

function compile(sourcePath, outputPath) {
  const source = fs.readFileSync(sourcePath, 'utf8');
  const result = ts.transpileModule(source, {
    compilerOptions: {
      module: ts.ModuleKind.CommonJS,
      target: ts.ScriptTarget.ES2022,
      esModuleInterop: true,
    },
    fileName: sourcePath,
    reportDiagnostics: true,
  });
  const errors = (result.diagnostics || []).filter(item => item.category === ts.DiagnosticCategory.Error);
  if (errors.length) {
    throw new Error(ts.formatDiagnosticsWithColorAndContext(errors, {
      getCurrentDirectory: () => sourceRoot,
      getCanonicalFileName: value => value,
      getNewLine: () => '\n',
    }));
  }
  fs.writeFileSync(outputPath, result.outputText);
}

function hydrate(input) {
  const output = { ...input };
  for (const field of ['starts_at', 'ends_at']) {
    const value = output[field];
    if (value && typeof value === 'object' && typeof value.__date === 'string') {
      output[field] = new Date(value.__date);
    }
  }
  return output;
}

function classify(error) {
  const message = String(error && error.message || error);
  return {
    errorType: error && error.type || 'unknown',
    errorName: error && error.name || 'Error',
    isMedusaError: Boolean(error && error.__isMedusaError),
    errorField: message.includes('starts at') ? 'starts_at' : message.includes('ends at') ? 'ends_at' : null,
  };
}

async function main() {
  const tempRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'medusa-price-date-rule-'));
  const shimDir = path.join(tempRoot, 'node_modules', '@medusajs', 'framework', 'utils');
  fs.mkdirSync(shimDir, { recursive: true });

  const validatorPath = path.join(sourceRoot, sourceFiles.validator);
  const dateHelperPath = path.join(sourceRoot, sourceFiles.dateHelper);
  const errorClassPath = path.join(sourceRoot, sourceFiles.errorClass);
  compile(dateHelperPath, path.join(tempRoot, 'is-date.js'));
  compile(errorClassPath, path.join(tempRoot, 'errors.js'));
  compile(validatorPath, path.join(tempRoot, 'validate-price-list-dates.js'));

  fs.writeFileSync(
    path.join(shimDir, 'index.js'),
    "const { isDate } = require('../../../../is-date.js');\n" +
    "const { MedusaError } = require('../../../../errors.js');\n" +
    "module.exports = { isDate, MedusaError };\n"
  );
  const { validatePriceListDates } = require(path.join(tempRoot, 'validate-price-list-dates.js'));

  const cases = [
    ['omitted-both', {}],
    ['null-both', { starts_at: null, ends_at: null }],
    ['empty-string-both', { starts_at: '', ends_at: '' }],
    ['valid-start-iso', { starts_at: '2026-01-01T00:00:00.000Z' }],
    ['valid-end-iso', { ends_at: '2026-12-31T23:59:59.999Z' }],
    ['invalid-start', { starts_at: 'not-a-date' }],
    ['invalid-end', { ends_at: 'not-a-date' }],
    ['date-object-start', { starts_at: { __date: '2026-01-01T00:00:00.000Z' } }],
    ['reversed-range', { starts_at: '2026-12-31T00:00:00.000Z', ends_at: '2026-01-01T00:00:00.000Z' }],
    ['both-invalid-start-first', { starts_at: 'bad-start', ends_at: 'bad-end' }],
  ];

  const capturedAt = new Date().toISOString();
  const scenarios = cases.map(([label, input]) => {
    try {
      validatePriceListDates(hydrate(input));
      return { label, input, outcome: 'accepted', errorType: null, errorName: null, isMedusaError: false, errorField: null };
    } catch (error) {
      return { label, input, outcome: 'rejected', ...classify(error), validationOrder: label === 'both-invalid-start-first' ? 'starts_at-first' : 'not-discriminated' };
    }
  }).map(item => ({ ...item, validationOrder: item.validationOrder || 'not-discriminated' }));

  const packageJson = JSON.parse(fs.readFileSync(path.join(sourceRoot, 'packages/modules/pricing/package.json'), 'utf8'));
  const commit = process.env.MEDUSA_SOURCE_COMMIT;
  const report = {
    capturedAt,
    completedAt: new Date().toISOString(),
    source: 'Medusa pinned source utility runtime',
    sourceCommit: commit,
    pricingModuleVersion: packageJson.version,
    typescriptVersion: ts.version,
    dependencyResolution: 'The validator, isDate helper, and MedusaError class are transpiled from the pinned source commit; a temporary module shim resolves the original framework-utils import to those same pinned helper sources.',
    sourceFileDigests: Object.fromEntries(Object.entries(sourceFiles).map(([key, value]) => [key, sha256(path.join(sourceRoot, value))])),
    scenarios,
  };

  const byLabel = Object.fromEntries(scenarios.map(item => [item.label, item]));
  const checks = [
    byLabel['omitted-both'].outcome === 'accepted',
    byLabel['null-both'].outcome === 'accepted',
    byLabel['empty-string-both'].outcome === 'accepted',
    byLabel['valid-start-iso'].outcome === 'accepted',
    byLabel['valid-end-iso'].outcome === 'accepted',
    byLabel['invalid-start'].outcome === 'rejected' && byLabel['invalid-start'].errorType === 'invalid_data' && byLabel['invalid-start'].isMedusaError,
    byLabel['invalid-end'].outcome === 'rejected' && byLabel['invalid-end'].errorType === 'invalid_data' && byLabel['invalid-end'].isMedusaError,
    byLabel['date-object-start'].outcome === 'accepted',
    byLabel['reversed-range'].outcome === 'accepted',
    byLabel['both-invalid-start-first'].outcome === 'rejected' && byLabel['both-invalid-start-first'].errorField === 'starts_at',
  ];
  report.checks = checks;
  report.passed = checks.every(Boolean);
  process.stdout.write(JSON.stringify(report, null, 2) + '\n');
  fs.rmSync(tempRoot, { recursive: true, force: true });
  if (!report.passed) process.exitCode = 1;
}

main().catch(error => {
  process.stderr.write(error.stack + '\n');
  process.exit(1);
});
