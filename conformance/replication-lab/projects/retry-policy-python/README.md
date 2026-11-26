# Python retry-policy replica

This is an independent, deliberately narrow replica of the job retry decision rule investigated in case BMQ-ER-002. It does not attempt to recreate BullMQ, Redis, its worker scheduler, or its queue storage.

## Run

```bash
python -m unittest -v
```

The tests cover the configured attempt limit, unrecoverable failures, maximum started attempts, fixed/custom delay outcomes, immediate retry, exponential delay calculation, and an off-by-one mutation.

## Scope warning

A passing local test suite validates this Python model against the currently extracted source-code rule. It does not yet establish source runtime equivalence. The BullMQ runtime probe, end-to-end queue state/event capture, and comparison report remain required before this case can pass Phase 6.
