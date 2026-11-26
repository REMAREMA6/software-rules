# Runtime browser conformance harness

This harness runs the three Task Board implementations in Chromium under the same fixed environment and retains machine-readable observations and screenshots.

## Run

```bash
npm install --prefix conformance/runtime
npx --prefix conformance/runtime playwright install --with-deps chromium
npm run capture --prefix conformance/runtime
```

The script starts a local fixture server and supplies a deterministic in-memory API route adapter. It captures:

- Full-page screenshots for empty, populated, completed, filtered, deleted, keyboard-operated, and API-failure states.
- The rendered DOM hierarchy and text.
- Every computed CSS property and pseudo-element content for every element, plus element geometry and rendered DOM hierarchy.
- Native semantics, ARIA attributes, focus order samples, and native required-field validation.
- API request/response events and rejected-request behavior.
- Page errors and visible error/recovery UI (including an explicit record when none exists).

It compares reference and independent baseline screenshots pixel-for-pixel for seven common workflow states. The successful Phase 6 run produced zero differing pixels in all seven states; the deliberately mutated build produced a 272-pixel mismatch in the one-active state. It also asserts matching baseline API traces and runtime error outcomes.

## Output

The script writes `runtime-output/` containing one JSON capture per implementation, PNG screenshots, per-state pixel-diff images, and `comparison.json`. GitHub Actions uploads this directory as the `task-board-runtime-captures` artifact.

## Interpretation and limits

A passing run establishes only that the enumerated Task Board states were executed and that the baseline pair rendered identically under the recorded Chromium/viewport environment. It does not prove that every conceivable software rule has been discovered, nor does it establish cross-platform font/raster equivalence. Computed style and pixel rendering are environment-dependent. The API remains an in-memory adapter; production transport, server, persistence, identity, and authorization are outside this fixture's declared boundary.

A capture is not replication-complete merely because the automation passes. The property inventory must be reviewed against the actual output artifacts, and unresolved required properties must remain incomplete. The CI job intentionally does not promote a capture to complete automatically. The Phase 6 Task Board inventories were reviewed against the output archive and are now marked complete for their explicit declared scope; see `examples/task-board/captures/`.
