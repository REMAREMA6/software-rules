# Comparison specification

**Status:** Draft — Phase 5  
**Purpose:** Define a reproducible, evidence-bounded comparison between two Software Rules captures.

## Reading order

1. [Comparison model](COMPARISON-MODEL.md)
2. [Normalization](NORMALIZATION.md)
3. [Matching rules](MATCHING-RULES.md)
4. [Difference classification](DIFFERENCE-CLASSIFICATION.md)
5. [Coverage and limitations](COVERAGE-AND-LIMITATIONS.md)

The machine-readable report structure is in `schemas/v1/comparison-report.schema.json`. Worked examples are in `comparison/examples/`.

## Normative boundary

Comparison operates on captured records and evidence. It does not infer unobserved behaviour, silently repair incomplete captures, or treat source-derived rules and declared contracts as runtime observations. A result applies only to the declared captures, matched conditions, facets, dimensions, and evidence.
