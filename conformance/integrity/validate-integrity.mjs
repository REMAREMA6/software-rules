import fs from "node:fs";

export function validateCapture(capture) {
  const errors = [];
  const index = (items, key) => new Map((items ?? []).map((item) => [item[key], item]));
  const scenarios = index(capture.scenarios, "scenarioId");
  const executions = index(capture.executions, "executionId");
  const observations = index(capture.observations, "observationId");
  const evidence = index(capture.evidence, "evidenceId");
  const targets = new Set([capture.target?.targetId].filter(Boolean));
  const ref = (exists, value, path, kind) => { if (!exists) errors.push(`${path}: unresolved ${kind} reference "${value}"`); };
  for (const [name, items, key] of [["scenarios",capture.scenarios,"scenarioId"],["executions",capture.executions,"executionId"],["observations",capture.observations,"observationId"],["evidence",capture.evidence,"evidenceId"]]) {
    const seen = new Set();
    for (const [i,item] of (items ?? []).entries()) { if (seen.has(item[key])) errors.push(`${name}[${i}].${key}: duplicate identifier "${item[key]}"`); seen.add(item[key]); }
  }
  for (const [i,e] of (capture.executions ?? []).entries()) { ref(scenarios.has(e.scenarioId),e.scenarioId,`executions[${i}].scenarioId`,"scenario"); ref(targets.has(e.targetId),e.targetId,`executions[${i}].targetId`,"target"); }
  for (const [i,o] of (capture.observations ?? []).entries()) {
    ref(targets.has(o.targetId),o.targetId,`observations[${i}].targetId`,"target");
    if (o.executionId) { ref(executions.has(o.executionId),o.executionId,`observations[${i}].executionId`,"execution"); const e=executions.get(o.executionId); if (e && e.targetId!==o.targetId) errors.push(`observations[${i}]: targetId differs from linked execution`); }
    for (const id of o.evidenceRefs ?? []) ref(evidence.has(id),id,`observations[${i}].evidenceRefs`,"evidence");
  }
  for (const [i,r] of (capture.runtimeRules ?? []).entries()) for (const field of ["supportingObservationIds","qualifyingObservationIds","contradictingObservationIds"]) for (const id of r[field] ?? []) ref(observations.has(id),id,`runtimeRules[${i}].${field}`,"observation");
  for (const [i,r] of (capture.sourceRules ?? []).entries()) for (const id of r.sourceEvidenceRefs ?? []) ref(evidence.has(id),id,`sourceRules[${i}].sourceEvidenceRefs`,"evidence");
  for (const [i,c] of (capture.coverage ?? []).entries()) { for (const id of c.scenarioIds ?? []) ref(scenarios.has(id),id,`coverage[${i}].scenarioIds`,"scenario"); for (const id of c.executionIds ?? []) ref(executions.has(id),id,`coverage[${i}].executionIds`,"execution"); }
  return errors;
}
if (process.argv[1] && import.meta.url === new URL(`file://${process.argv[1]}`).href) { const file=process.argv[2]; if (!file) { console.error("Usage: node validate-integrity.mjs <capture.json>"); process.exit(2); } const errors=validateCapture(JSON.parse(fs.readFileSync(file,"utf8"))); if (errors.length) { console.error(errors.map(e=>`FAIL ${e}`).join("\n")); process.exit(1); } console.log(`PASS cross-record integrity: ${file}`); }
