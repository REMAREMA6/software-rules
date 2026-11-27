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

  // Replication completeness is evaluated against the declared property inventory,
  // not inferred from the count of observations or successful comparisons.
  const scope = capture.replicationScope;
  if (!scope || !Array.isArray(scope.propertyInventory) || scope.propertyInventory.length === 0) {
    errors.push("replicationScope.propertyInventory: a non-empty declared replication property inventory is required");
  } else {
    const seenProperties = new Set();
    const blocking = new Set(["partial","not-observed","unknown","unavailable","conflicting","source-inferred"]);
    let unresolvedRequired = false;
    for (const [i,property] of scope.propertyInventory.entries()) {
      const path = `replicationScope.propertyInventory[${i}]`;
      if (seenProperties.has(property.propertyId)) errors.push(`${path}.propertyId: duplicate identifier "${property.propertyId}"`);
      seenProperties.add(property.propertyId);
      if (!(scope.facets ?? []).includes(property.facet)) errors.push(`${path}.facet: facet "${property.facet}" is not declared in replicationScope.facets`);
      const obsRefs = property.observationRefs ?? [];
      const evidenceRefs = property.evidenceRefs ?? [];
      for (const id of obsRefs) ref(observations.has(id),id,`${path}.observationRefs`,"observation");
      for (const id of evidenceRefs) ref(evidence.has(id),id,`${path}.evidenceRefs`,"evidence");
      if (["captured","partial"].includes(property.status)) {
        if (obsRefs.length === 0) errors.push(`${path}: ${property.status} property requires observationRefs`);
        if (evidenceRefs.length === 0) errors.push(`${path}: ${property.status} property requires evidenceRefs`);
      }
      const linkedObservations = obsRefs.map(id => observations.get(id)).filter(Boolean);
      const evidenceLinkedByObservations = new Set();
      for (const id of obsRefs) {
        const observation = observations.get(id);
        if (observation && observation.facet !== property.facet) errors.push(`${path}: observation "${id}" belongs to facet "${observation.facet}", not "${property.facet}"`);
        if (observation) for (const evidenceId of observation.evidenceRefs ?? []) evidenceLinkedByObservations.add(evidenceId);
        if (property.status === "captured" && observation && observation.status !== "observed") errors.push(`${path}: captured property references non-observed observation "${id}"`);
      }
      for (const id of evidenceRefs) {
        const evidenceRecord = evidence.get(id);
        if (property.status === "source-inferred") {
          if (evidenceRecord && evidenceRecord.evidenceClass !== "source-artifact") {
            errors.push(`${path}: source-inferred property must reference source-artifact evidence, not "${evidenceRecord.evidenceClass}"`);
          }
        } else if (!evidenceLinkedByObservations.has(id)) {
          errors.push(`${path}: evidence "${id}" is not attached to any observation linked by this property`);
        }
      }
      if (property.status === "captured") {
        const hasAdequateRuntimeObservation = linkedObservations.some(observation =>
          observation.status === "observed" &&
          observation.payload?.completeness?.status !== "partial" &&
          (observation.evidenceRefs ?? []).some(id => evidence.get(id)?.evidenceClass === "runtime")
        );
        if (!hasAdequateRuntimeObservation) errors.push(`${path}: captured property requires at least one observed record linked to runtime evidence and not explicitly marked partial`);
      }
      if (property.requirement === "required" && blocking.has(property.status)) unresolvedRequired = true;
      if (property.requirement === "required" && property.status === "excluded") errors.push(`${path}: required property cannot be excluded from the declared replication scope`);
      if (property.requirement === "required" && property.status === "not-applicable" && !property.rationale) errors.push(`${path}: required not-applicable property needs a rationale`);
    }
    const declared = scope.completeness?.status;
    const expected = unresolvedRequired ? "incomplete" : "complete";
    if (declared === "complete" && unresolvedRequired) errors.push("replicationScope.completeness.status: cannot be complete while required inventory properties are unresolved");
    if (declared === "incomplete" && !unresolvedRequired) errors.push("replicationScope.completeness.status: marked incomplete but no required inventory property is unresolved");
    if (declared === "undetermined" && !unresolvedRequired) errors.push("replicationScope.completeness.status: undetermined requires an unresolved inventory assessment or an explicitly incomplete inventory definition");
    if (!["complete","incomplete","undetermined"].includes(declared)) errors.push("replicationScope.completeness.status: missing or invalid completeness status");
  }
  return errors;
}
if (process.argv[1] && import.meta.url === new URL(`file://${process.argv[1]}`).href) { const file=process.argv[2]; if (!file) { console.error("Usage: node validate-integrity.mjs <capture.json>"); process.exit(2); } const errors=validateCapture(JSON.parse(fs.readFileSync(file,"utf8"))); if (errors.length) { console.error(errors.map(e=>`FAIL ${e}`).join("\n")); process.exit(1); } console.log(`PASS cross-record integrity and replication inventory: ${file}`); }
