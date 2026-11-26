# Normalization

**Status:** Draft — Phase 5

## 1. Purpose

Normalization creates a comparison projection from a raw observation. It does not rewrite, replace, or erase the original observation or evidence.

Every normalization operation MUST identify its input dimension, method, method version, parameters, output representation, and whether information was discarded. Operations MUST be deterministic for the same inputs and declared parameters, unless explicitly classified as probabilistic; probabilistic transformations are not eligible for exact comparison.

## 2. General rules

1. Preserve raw observations and evidence unchanged.
2. Store normalized values as derived comparison data linked to the raw observation IDs.
3. Apply the same declared operation/version to both sides where meaningful.
4. Record every transformation in order; do not hide chained transformations.
5. Do not normalize away distinctions that may affect software behaviour.
6. If a safe transformation cannot be established, leave values unnormalized and classify as unknown or not-comparable.
7. Normalization must be facet- and dimension-aware. There is no universal deep-sort, lowercase, trim, or stringify operation.

## 3. Common normalization domains

### Identifiers
- Capture-local record IDs are not cross-implementation semantic identity.
- Explicit stable domain identifiers may be compared when their namespace and lifecycle are the same.
- Generated IDs, memory addresses, random tokens, session IDs, and framework-generated keys MUST NOT be equated merely because their shape or position matches.
- Volatile identifiers may be masked only when the field is proven irrelevant to the compared outcome; record the mask rule and retain the raw value.

### Time
- Parse timestamps with their declared timezone/offset; compare instants after conversion to a common timeline.
- Preserve original timestamp, precision, timezone, and clock-source uncertainty.
- Do not remove time ordering or latency differences by rounding unless a declared tolerance justifies it.
- Wall-clock timestamps and monotonic durations are distinct quantities.

### Units and numeric values
- Convert units only when dimensions are compatible and conversion is defined. Record source unit, target unit, conversion, and precision.
- Do not round before applying the declared tolerance.
- Distinguish integer counts, decimal quantities, percentages, ratios, and measured durations.
- Floating-point comparisons require a metric and explicit absolute and/or relative tolerance; do not assume exact binary equality is meaningful.

### Collections and ordering
- Preserve order where the facet defines order as observable: UI paint order, tab order, message sequence, API arrays, workflow steps, and priority lists.
- Treat a collection as unordered only when its semantics explicitly say order is irrelevant. Canonical sorting then requires a stable, documented key.
- Duplicate elements MUST be retained unless the domain explicitly defines set semantics.

### Text and strings
- Unicode normalization, whitespace folding, case folding, locale handling, and line-ending normalization are separate operations, not automatic defaults.
- Preserve locale, encoding, and directionality where relevant.
- Do not strip punctuation, labels, accessibility names, or visible content as "noise" without a facet-specific justification.

### Structured values
- Object/property ordering may be ignored only where the data format defines it as semantically irrelevant.
- Absent, null, false, zero, empty string, and empty collection remain distinct.
- Redacted, unavailable, unknown, not observed, not applicable, partial, and conflicting states MUST remain distinct.
- Do not recursively sort every array or coerce unlike types.

### Geometry and presentation
- Coordinate space, viewport, device scale, scroll position, font availability, rendering engine, and layout environment are comparison conditions.
- CSS pixels, device pixels, points, and physical units are not interchangeable without a recorded conversion.
- Geometry tolerances MUST be explicit and justified by the capture method and purpose.
- Pixel-image comparison and resolved-layout comparison are separate dimensions; one cannot silently substitute for the other.

### Performance and resource measurements
- Record workload, warm/cold state, hardware/runtime, sampling, aggregation, and measurement method.
- Compare distributions or declared statistics rather than selecting a convenient single sample.
- Report measurement noise and uncertainty. Do not treat a tolerance as universal across environments.

## 4. Canonical serialization

Canonical serialization MAY be used to compare structured values only after semantic ordering, numeric representation, Unicode, and missingness rules are fixed for that facet. A serialization algorithm/version MUST be named. Canonical bytes are a derived artifact, not a replacement for source data.

## 5. Normalization profile

A report identifies a versioned profile and lists operations by facet and dimension. Each operation records method/version, parameters, input/output representation, and `preservesRaw: true`. A profile change can change comparison results and therefore requires a new profile version.
