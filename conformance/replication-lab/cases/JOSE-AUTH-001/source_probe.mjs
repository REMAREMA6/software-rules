import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { pathToFileURL } from 'node:url'

const sourceRoot = process.env.JOSE_SOURCE_ROOT
const jose = await import(pathToFileURL(path.join(sourceRoot, 'dist/webapi/index.js')).href)
const { SignJWT, jwtVerify } = jose

const now = 1700000000
const issuer = 'https://issuer.example'
const audience = 'api.example'
const secret = new TextEncoder().encode('software-rules-jose-hmac-key-32bytes!!')
const secret384 = new TextEncoder().encode('software-rules-jose-hmac-key-48bytes!!')
const baseOptions = {
  algorithms: ['HS256'],
  issuer,
  audience,
  currentDate: new Date(now * 1000),
}
const sourceFiles = [
  'src/jwt/verify.ts',
  'src/lib/jwt_claims_set.ts',
  'src/lib/jws_verify.ts',
  'test/jwt/verify.test.ts',
  'package.json',
  'LICENSE.md',
  'tsconfig.json',
]

async function sign(payload, alg = 'HS256', key = secret) {
  return new jose.SignJWT(payload).setProtectedHeader({ alg }).sign(key)
}

function classify(error) {
  const code = error && error.code
  const claim = error && error.claim
  const reason = error && error.reason
  if (code === 'ERR_JWT_EXPIRED') return 'token-expired'
  if (code === 'ERR_JWS_SIGNATURE_VERIFICATION_FAILED') return 'signature-invalid'
  if (code === 'ERR_JOSE_ALG_NOT_ALLOWED') return 'algorithm-not-allowed'
  if (code === 'ERR_JWT_CLAIM_VALIDATION_FAILED') {
    if (claim === 'nbf') return 'token-not-yet-valid'
    if (claim === 'iss') return reason === 'missing' ? 'issuer-missing' : 'issuer-mismatch'
    if (claim === 'aud') return reason === 'missing' ? 'audience-missing' : 'audience-mismatch'
    return 'claim-invalid'
  }
  return 'other-error'
}

function sha256(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(path.join(sourceRoot, file))).digest('hex')
}

async function runCase(label, payload, options = {}, alg = 'HS256', key = secret, tamper = false) {
  let token = await sign(payload, alg, key)
  if (tamper) {
    const parts = token.split('.')
    const last = parts[2].at(-1)
    parts[2] = (parts[2][0] === 'A' ? 'B' : 'A') + parts[2].slice(1)
    token = parts.join('.')
  }
  const verifyOptions = {
    ...baseOptions,
    ...options,
  }
  try {
    const result = await jwtVerify(token, key, verifyOptions)
    return {
      label,
      token,
      keyBase64url: Buffer.from(key).toString('base64url'),
      verificationOptions: {
        algorithms: verifyOptions.algorithms,
        issuer: verifyOptions.issuer,
        audience: verifyOptions.audience,
        currentDateEpochSeconds: now,
      },
      outcome: 'accepted',
      errorCategory: null,
      errorCode: null,
      errorClaim: null,
      claims: result.payload,
      protectedHeader: result.protectedHeader,
    }
  } catch (error) {
    return {
      label,
      token,
      keyBase64url: Buffer.from(key).toString('base64url'),
      verificationOptions: {
        algorithms: verifyOptions.algorithms,
        issuer: verifyOptions.issuer,
        audience: verifyOptions.audience,
        currentDateEpochSeconds: now,
      },
      outcome: 'rejected',
      errorCategory: classify(error),
      errorCode: error && error.code || null,
      errorClaim: error && error.claim || null,
      claims: null,
      protectedHeader: null,
    }
  }
}

const scenarios = []
scenarios.push(await runCase('valid-token', {
  sub: 'user-1', iss: issuer, aud: audience, exp: now + 600, nbf: now - 60,
}))
scenarios.push(await runCase('expired-token', {
  sub: 'user-1', iss: issuer, aud: audience, exp: now - 1, nbf: now - 60,
}))
scenarios.push(await runCase('not-before-future', {
  sub: 'user-1', iss: issuer, aud: audience, exp: now + 600, nbf: now + 1,
}))
scenarios.push(await runCase('issuer-mismatch', {
  sub: 'user-1', iss: 'https://wrong-issuer.example', aud: audience, exp: now + 600,
}))
scenarios.push(await runCase('audience-mismatch', {
  sub: 'user-1', iss: issuer, aud: 'other-api.example', exp: now + 600,
}))
scenarios.push(await runCase('tampered-signature', {
  sub: 'user-1', iss: issuer, aud: audience, exp: now + 600,
}, {}, 'HS256', secret, true))
scenarios.push(await runCase('algorithm-not-allowed', {
  sub: 'user-1', iss: issuer, aud: audience, exp: now + 600,
}, {}, 'HS384', secret384))
scenarios.push(await runCase('missing-exp-is-optional', {
  sub: 'user-1', iss: issuer, aud: audience,
}))
scenarios.push(await runCase('audience-array-match', {
  sub: 'user-1', iss: issuer, aud: [audience, 'other-api.example'], exp: now + 600,
}))
scenarios.push(await runCase('missing-issuer', {
  sub: 'user-1', aud: audience, exp: now + 600,
}))
scenarios.push(await runCase('missing-audience', {
  sub: 'user-1', iss: issuer, exp: now + 600,
}))

const packageJson = JSON.parse(fs.readFileSync(path.join(sourceRoot, 'package.json'), 'utf8'))
const report = {
  capturedAt: new Date().toISOString(),
  completedAt: new Date().toISOString(),
  source: 'panva/jose pinned source build',
  sourceCommit: process.env.JOSE_SOURCE_COMMIT,
  packageVersion: packageJson.version,
  runtime: process.version,
  sourceFiles,
  sourceFileDigests: Object.fromEntries(sourceFiles.map(file => [file, sha256(file)])),
  testTimeEpochSeconds: now,
  scenarios,
}
const expected = {
  'valid-token': ['accepted', null],
  'expired-token': ['rejected', 'token-expired'],
  'not-before-future': ['rejected', 'token-not-yet-valid'],
  'issuer-mismatch': ['rejected', 'issuer-mismatch'],
  'audience-mismatch': ['rejected', 'audience-mismatch'],
  'tampered-signature': ['rejected', 'signature-invalid'],
  'algorithm-not-allowed': ['rejected', 'algorithm-not-allowed'],
  'missing-exp-is-optional': ['accepted', null],
  'audience-array-match': ['accepted', null],
  'missing-issuer': ['rejected', 'issuer-missing'],
  'missing-audience': ['rejected', 'audience-missing'],
}
report.checks = scenarios.map(item => {
  const [outcome, category] = expected[item.label]
  return item.outcome === outcome && item.errorCategory === category
})
report.passed = report.checks.every(Boolean)
process.stdout.write(JSON.stringify(report, null, 2) + '\n')
if (!report.passed) process.exitCode = 1
