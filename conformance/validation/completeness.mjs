export function validateComparisonCompleteness(report) {
  const errors = [];
  const completeness = report.replicationCompleteness;
  if (!completeness) return ["replicationCompleteness is required"];
  const { referenceStatus, implementationStatus, result } = completeness;
  const statuses = ["complete", "incomplete", "undetermined"];
  if (!statuses.includes(referenceStatus) || !statuses.includes(implementationStatus)) {
    errors.push("replicationCompleteness statuses must be complete, incomplete, or undetermined");
    return errors;
  }
  let expected;
  if (referenceStatus === "undetermined" || implementationStatus === "undetermined") expected = "undetermined";
  else if (referenceStatus === "incomplete" && implementationStatus === "incomplete") expected = "incomplete-both";
  else if (referenceStatus === "incomplete") expected = "incomplete-reference";
  else if (implementationStatus === "incomplete") expected = "incomplete-implementation";
  else expected = "complete-both";
  if (result !== expected) errors.push(`replicationCompleteness.result must be "${expected}" for the two capture statuses, received "${result}"`);
  if (expected !== "complete-both" && /faithful replication (?:is|has been) (?:established|supported)|complete equivalence (?:is|has been) (?:established|supported)/i.test(report.conclusion?.statement ?? "")) {
    errors.push("conclusion: cannot claim faithful replication or complete equivalence while either capture is incomplete or undetermined");
  }
  return errors;
}
