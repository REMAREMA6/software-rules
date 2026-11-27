# Independent React Task Board replica

This is an independent React 19 implementation of the plain HTML/CSS/JavaScript Task Board source at `examples/task-board/reference/index.html`.

It uses its own React state, JSX tree, and event handlers. The source implementation is not imported or used as a runtime dependency.

## Build

```sh
npm install --no-audit --no-fund
npm run build
```

The conformance workflow serves the production build and compares it with the pinned source fixture using the shared Playwright runtime.
