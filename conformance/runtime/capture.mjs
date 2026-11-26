import fs from "node:fs/promises";
import path from "node:path";
import http from "node:http";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import pixelmatch from "pixelmatch";
import { PNG } from "pngjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const output = path.resolve(root, "runtime-output");
await fs.rm(output, { recursive: true, force: true });
await fs.mkdir(output, { recursive: true });

const variants = {
  reference: "examples/task-board/reference/index.html",
  independent: "examples/task-board/independent/index.html",
  mutated: "examples/task-board/independent-mutated/index.html"
};
const server = http.createServer(async (req, res) => {
  const key = new URL(req.url, "http://localhost").pathname.slice(1);
  const file = variants[key];
  if (!file) { res.writeHead(404).end("Not found"); return; }
  try {
    const html = await fs.readFile(path.join(root, file));
    res.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    res.end(html);
  } catch { res.writeHead(500).end("Unable to load fixture"); }
});
await new Promise(resolve => server.listen(4173, "127.0.0.1", resolve));

const browser = await chromium.launch({ headless: true });
const captures = {};
const apiLog = {};
const pageErrors = {};

async function runVariant(name) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1 });
  let records = [];
  let nextId = 1;
  let failNext = false;
  apiLog[name] = [];
  pageErrors[name] = [];
  page.on("pageerror", error => pageErrors[name].push(error.message));
  await page.route("**/api/tasks**", async route => {
    const request = route.request();
    const method = request.method();
    const url = new URL(request.url());
    const body = request.postDataJSON?.() ?? null;
    if (failNext) {
      failNext = false;
      apiLog[name].push({ method, path: url.pathname, request: body, response: { status: 503, body: { error: "Service unavailable" } } });
      await route.fulfill({ status: 503, contentType: "application/json", body: JSON.stringify({ error: "Service unavailable" }) });
      return;
    }
    let response;
    if (method === "POST" && url.pathname === "/api/tasks") {
      const record = { id: String(nextId++), title: body.title, completed: false };
      records.push(record); response = { status: 200, body: record };
    } else if (method === "PATCH") {
      const id = url.pathname.split("/").pop();
      records = records.map(item => item.id === id ? { ...item, ...body } : item);
      response = { status: 200, body: records.find(item => item.id === id) };
    } else if (method === "DELETE") {
      const id = url.pathname.split("/").pop();
      records = records.filter(item => item.id !== id);
      response = { status: 200, body: { deleted: true, id } };
    } else {
      response = { status: 404, body: { error: "Not found" } };
    }
    apiLog[name].push({ method, path: url.pathname, request: body, response });
    await route.fulfill({ status: response.status, contentType: "application/json", body: JSON.stringify(response.body) });
  });

  await page.goto(`http://127.0.0.1:4173/${name}`);
  const snapshots = {};
  async function save(label) {
    const file = `${name}-${label}.png`;
    await page.screenshot({ path: path.join(output, file), fullPage: true });
    snapshots[label] = {
      screenshot: file,
      url: page.url(),
      viewport: page.viewportSize(),
      document: await page.locator("body").evaluate(body => {
        const describe = element => {
          const style = getComputedStyle(element);
          const rect = element.getBoundingClientRect();
          const attrs = Object.fromEntries([...element.attributes].map(a => [a.name, a.value]));
          return {
            tag: element.tagName.toLowerCase(), id: element.id || null,
            classes: [...element.classList], attributes: attrs,
            text: [...element.childNodes].filter(n => n.nodeType === Node.TEXT_NODE).map(n => n.textContent.trim()).filter(Boolean).join(" "),
            rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height, top: rect.top, right: rect.right, bottom: rect.bottom, left: rect.left },
            computed: Object.fromEntries(Array.from(style).map(property => [property, style.getPropertyValue(property)])),
            pseudoElements: {
              before: getComputedStyle(element, "::before").content,
              after: getComputedStyle(element, "::after").content
            },
            children: [...element.children].map(describe)
          };
        };
        return describe(body);
      }),
      accessibilityTree: await page.locator("body").ariaSnapshot(),
      accessibilitySemantics: await page.locator("body").evaluate(body => [...body.querySelectorAll("*")].map(el => ({
        tag: el.tagName.toLowerCase(), role: el.getAttribute("role"),
        ariaLabel: el.getAttribute("aria-label"), ariaLive: el.getAttribute("aria-live"),
        ariaPressed: el.getAttribute("aria-pressed"), ariaRequired: el.getAttribute("aria-required"),
        name: el.getAttribute("name"), type: el.getAttribute("type"),
        tabIndex: el.tabIndex, disabled: "disabled" in el ? el.disabled : null
      }))),
      visibleText: await page.locator("body").innerText(),
      focusedElement: await page.evaluate(() => ({
        tag: document.activeElement?.tagName.toLowerCase(),
        id: document.activeElement?.id || null,
        ariaLabel: document.activeElement?.getAttribute("aria-label")
      }))
    };
  }

  await save("empty");
  // Native required-field validation: empty submission must not call the API.
  await page.getByRole("button", { name: "Add task" }).click();
  snapshots.empty.nativeValidation = await page.locator("#task-input, #title").evaluate(el => ({
    valid: el.checkValidity(), validationMessage: el.validationMessage
  }));
  snapshots.empty.apiRequestCountAfterEmptySubmit = apiLog[name].length;

  const input = page.locator("#task-input, #title");
  await input.fill("   ");
  await page.getByRole("button", { name: "Add task" }).click();
  snapshots.empty.whitespaceSubmission = {
    inputValue: await input.inputValue(),
    taskCount: await page.locator("li").count(),
    apiRequestCount: apiLog[name].length
  };

  await input.fill("Prepare release notes");
  await page.getByRole("button", { name: "Add task" }).click();
  await page.getByText("Prepare release notes").waitFor();
  await save("one-active");

  // Keyboard focus order and keyboard form submission.
  await page.reload();
  await page.keyboard.press("Tab");
  const firstFocus = await page.evaluate(() => ({ tag: document.activeElement.tagName.toLowerCase(), id: document.activeElement.id }));
  await page.keyboard.type("Keyboard-created task");
  await page.keyboard.press("Tab");
  await page.keyboard.press("Enter");
  await page.getByText("Keyboard-created task").waitFor();
  // Tab through real focus order; activate every control with keyboard keys only.
  async function tabUntil(selector) {
    for (let attempt = 0; attempt < 12; attempt++) {
      await page.keyboard.press("Tab");
      if (await page.locator(selector).evaluate(element => element === document.activeElement)) return;
    }
    throw new Error(`Keyboard focus did not reach ${selector}`);
  }
  await tabUntil('[data-filter="active"]');
  await page.keyboard.press("Enter");
  const keyboardActiveCount = await page.locator("li").count();
  await tabUntil('[data-filter="completed"]');
  await page.keyboard.press("Enter");
  const keyboardCompletedCount = await page.locator("li").count();
  await tabUntil('[data-filter="all"]');
  await page.keyboard.press("Enter");
  await tabUntil('input[type="checkbox"]');
  const checkboxFocused = await page.locator('input[type="checkbox"]').evaluate(element => element === document.activeElement);
  if (!checkboxFocused) throw new Error("Keyboard tab sequence did not focus the task checkbox");
  await page.keyboard.press(" ");
  await page.waitForFunction(() => document.querySelector('input[type="checkbox"]')?.checked === true);
  const expectedKeyboardSummary = name === "mutated" ? "1 tasks · 0 active" : "1 task · 0 active";
  await page.waitForFunction(expected => document.querySelector("#summary, #meta")?.textContent === expected, expectedKeyboardSummary);
  const keyboardCompletedSummary = await page.locator("#summary, #meta").innerText();
  await tabUntil('button[aria-label="Delete Keyboard-created task"]');
  await page.keyboard.press("Enter");
  await page.getByText("Keyboard-created task").waitFor({ state: "detached" });
  // Return to All using keyboard before the pointer-driven visual-state run.
  await tabUntil('[data-filter="all"]');
  await page.keyboard.press("Enter");
  if (keyboardActiveCount !== 1) throw new Error("Keyboard Active filter did not show the active task");
  if (keyboardCompletedCount !== 0) throw new Error("Keyboard Completed filter should be empty before completion");
  if (keyboardCompletedSummary !== expectedKeyboardSummary) throw new Error("Keyboard completion did not update the task summary");
  await save("keyboard-workflow");
  snapshots["keyboard-workflow"].interactionResults = {
    firstFocus, keyboardActiveCount, keyboardCompletedCount, keyboardCompletedSummary,
    keyboardDeleteSucceeded: true,
    requests: [...apiLog[name]]
  };

  // Run pointer workflow separately for full visual-state comparison.
  await input.fill("Prepare release notes");
  await page.getByRole("button", { name: "Add task" }).click();
  await page.getByText("Prepare release notes").waitFor();
  await save("one-active");
  const checkbox = page.getByRole("checkbox", { name: "Complete Prepare release notes" });
  await checkbox.check();
  await save("completed");
  await page.getByRole("button", { name: "Active" }).click();
  await save("active-filter-empty");
  await page.getByRole("button", { name: "Completed" }).click();
  await save("completed-filter");
  await page.getByRole("button", { name: "All" }).click();
  await save("all-filter");
  await page.getByRole("button", { name: "Delete Prepare release notes" }).click();
  await save("deleted");

  // Probe behaviour, candidate business rules, and runtime data boundaries.
  // These are observations of this fixture and its deterministic adapter, not production-service claims.
  await page.reload();
  const probeStart = apiLog[name].length;
  async function createProbeTask(value) {
    const title = value.trim();
    const existingCount = await page.getByText(title, { exact: true }).count();
    await input.fill(value);
    const response = page.waitForResponse(candidate =>
      candidate.url().includes("/api/tasks") && candidate.request().method() === "POST"
    );
    await page.getByRole("button", { name: "Add task" }).click();
    await response;
    await page.waitForFunction(({ expectedTitle, expectedCount }) => {
      const rows = [...document.querySelectorAll("#task-list li, #items li")];
      return rows.filter(row => row.querySelector("span")?.textContent === expectedTitle).length >= expectedCount;
    }, { expectedTitle: title, expectedCount: existingCount + 1 });
  }

  await createProbeTask("  Trim boundary  ");
  const trimPost = apiLog[name].slice(probeStart).find(event => event.method === "POST" && event.request?.title === "Trim boundary");
  const trimResult = {
    submitted: "  Trim boundary  ",
    renderedText: await page.getByText("Trim boundary", { exact: true }).count(),
    apiRequestTitle: trimPost?.request?.title ?? null,
    responseRecord: trimPost?.response?.body ?? null
  };

  await createProbeTask("Duplicate title");
  await createProbeTask("Duplicate title");
  const duplicateCount = await page.getByText("Duplicate title", { exact: true }).count();

  const htmlLikeTitle = "Safe <img src=x onerror=alert(1)> & 東京";
  await createProbeTask(htmlLikeTitle);
  const htmlLikeResult = {
    exactTextRendered: await page.getByText(htmlLikeTitle, { exact: true }).count(),
    injectedImageCount: await page.locator("#task-list img, #items img").count()
  };

  const longTitle = "L".repeat(512);
  await createProbeTask(longTitle);
  const longTitleResult = {
    submittedLength: longTitle.length,
    renderedExactMatchCount: await page.getByText(longTitle, { exact: true }).count()
  };
  const initialProbeRecords = apiLog[name].slice(probeStart).filter(event => event.method === "POST");
  const initialIds = initialProbeRecords.map(event => event.response?.body?.id).filter(Boolean);

  // Reload isolates the state-count truth table from the preceding title probes.
  await page.reload();
  const matrixStart = apiLog[name].length;
  await createProbeTask("Matrix active one");
  await createProbeTask("Matrix active two");
  await createProbeTask("Matrix completed");
  const matrixCheckbox = page.getByRole("checkbox", { name: "Complete Matrix completed" });
  const completeResponse = page.waitForResponse(candidate =>
    candidate.url().includes("/api/tasks/") && candidate.request().method() === "PATCH"
  );
  await matrixCheckbox.check();
  await completeResponse;
  await page.waitForFunction(() => document.querySelector("#summary, #meta")?.textContent === "3 tasks · 2 active");
  const afterComplete = {
    total: await page.locator("li").count(),
    summary: await page.locator("#summary, #meta").innerText()
  };
  await page.getByRole("button", { name: "Active" }).click();
  const activeFilterCount = await page.locator("li").count();
  await page.getByRole("button", { name: "Completed" }).click();
  const completedFilterCount = await page.locator("li").count();
  await page.getByRole("button", { name: "All" }).click();
  const uncompleteResponse = page.waitForResponse(candidate =>
    candidate.url().includes("/api/tasks/") && candidate.request().method() === "PATCH"
  );
  await matrixCheckbox.uncheck();
  await uncompleteResponse;
  await page.waitForFunction(() => document.querySelector("#summary, #meta")?.textContent === "3 tasks · 3 active");
  const afterToggleBack = await page.locator("#summary, #meta").innerText();
  const matrixPatch = apiLog[name].slice(matrixStart).filter(event => event.method === "PATCH").map(event => event.response?.body);
  const matrixDeleteResults = [];
  while (await page.locator('button[aria-label^="Delete Matrix"]').count()) {
    const beforeDeleteCount = await page.locator('button[aria-label^="Delete Matrix"]').count();
    const deleteResponse = page.waitForResponse(candidate =>
      candidate.url().includes("/api/tasks/") && candidate.request().method() === "DELETE"
    );
    await page.locator('button[aria-label^="Delete Matrix"]').first().click();
    await deleteResponse;
    await page.waitForFunction(expected => document.querySelectorAll('button[aria-label^="Delete Matrix"]').length === expected, beforeDeleteCount - 1);
    matrixDeleteResults.push("deleted");
  }
  const matrixFinalSummary = await page.locator("#summary, #meta").innerText();

  const probeResults = {
    titleNormalization: trimResult,
    duplicateTitlesAccepted: duplicateCount === 2,
    duplicateTitleCount: duplicateCount,
    htmlLikeTitle: htmlLikeResult,
    longTitle: longTitleResult,
    observedPostIdentifiers: initialIds,
    identifiersUniqueWithinProbe: new Set(initialIds).size === initialIds.length,
    mixedTaskTruthTable: {
      afterCompletingOne: afterComplete,
      activeFilterCount,
      completedFilterCount,
      afterTogglingBack: afterToggleBack,
      expectedTotal: 3,
      expectedActiveAfterComplete: 2,
      expectedCompletedFilter: 1
    },
    patchResponseSamples: matrixPatch,
    matrixDeleteOperations: matrixDeleteResults.length,
    finalSummaryAfterDelete: matrixFinalSummary
  };
  if (trimResult.apiRequestTitle !== "Trim boundary") throw new Error("Leading/trailing whitespace normalization did not match the observed rule");
  if (duplicateCount !== 2) throw new Error("Duplicate-title probe did not preserve both records");
  if (htmlLikeResult.exactTextRendered !== 1 || htmlLikeResult.injectedImageCount !== 0) throw new Error("HTML-like title was not rendered as literal text");
  if (longTitleResult.renderedExactMatchCount !== 1) throw new Error("Long title was not preserved");
  if (activeFilterCount !== 2 || completedFilterCount !== 1) throw new Error("Mixed-task filter truth table did not match");
  if (afterComplete.summary !== "3 tasks · 2 active") throw new Error("Unexpected summary after completing one of three tasks");
  if (afterToggleBack !== "3 tasks · 3 active") throw new Error("Completion toggle-back did not restore active count");
  if (matrixDeleteResults.length !== 3 || matrixFinalSummary !== "0 tasks · 0 active") throw new Error("Mixed-task deletion did not restore the empty state");
  await save("business-data-probes");
  snapshots["business-data-probes"].probeResults = probeResults;

  // Record failure semantics without pretending that an error UI exists.
  failNext = true;
  await input.fill("Failure probe");
  await page.getByRole("button", { name: "Add task" }).click();
  await page.waitForTimeout(150);
  await save("api-failure");
  const result = {
    variant: name,
    environment: {
      browser: "Chromium", browserVersion: browser.version(),
      userAgent: await page.evaluate(() => navigator.userAgent),
      platform: await page.evaluate(() => navigator.platform),
      language: await page.evaluate(() => navigator.language),
      devicePixelRatio: await page.evaluate(() => window.devicePixelRatio),
      viewport: page.viewportSize(),
      colorScheme: await page.evaluate(() => matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"),
      loadedFonts: await page.evaluate(() => [...document.fonts].map(font => ({ family: font.family, status: font.status, weight: font.weight, style: font.style })))
    },
    snapshots, businessDataProbes: snapshots["business-data-probes"]?.probeResults ?? null, apiEvents: apiLog[name], pageErrors: pageErrors[name],
    failureObservation: {
      failedResponse: apiLog[name].findLast(event => event.response.status === 503) ?? null,
      visibleErrorText: await page.locator('[role="alert"], [aria-live="assertive"]').allInnerTexts(),
      note: "This implementation does not render a user-facing error or recovery control for a rejected create request; the failed request and page error are retained."
    }
  };
  await fs.writeFile(path.join(output, `${name}.capture.json`), JSON.stringify(result, null, 2));
  await page.close();
  return result;
}

try {
  for (const name of Object.keys(variants)) captures[name] = await runVariant(name);
  if (JSON.stringify(apiLog.reference) !== JSON.stringify(apiLog.independent)) {
    throw new Error("Reference and independent API request/response traces differ");
  }
  if (JSON.stringify(pageErrors.reference) !== JSON.stringify(pageErrors.independent)) {
    throw new Error("Reference and independent runtime error outcomes differ");
  }

  const comparison = [];
  for (const state of ["empty", "one-active", "completed", "active-filter-empty", "completed-filter", "all-filter", "deleted"]) {
    const a = PNG.sync.read(await fs.readFile(path.join(output, `reference-${state}.png`)));
    const b = PNG.sync.read(await fs.readFile(path.join(output, `independent-${state}.png`)));
    const diff = new PNG({ width: a.width, height: a.height });
    const pixels = pixelmatch(a.data, b.data, diff.data, a.width, a.height, { threshold: 0.1 });
    await fs.writeFile(path.join(output, `baseline-${state}-diff.png`), PNG.sync.write(diff));
    comparison.push({ state, width: a.width, height: a.height, differingPixels: pixels, totalPixels: a.width * a.height, exactPixelMatch: pixels === 0 });
    if (pixels !== 0) throw new Error(`Baseline pixel mismatch in state "${state}": ${pixels} pixels`);
  }
  const mutated = PNG.sync.read(await fs.readFile(path.join(output, "mutated-one-active.png")));
  const reference = PNG.sync.read(await fs.readFile(path.join(output, "reference-one-active.png")));
  const mutationDiff = pixelmatch(reference.data, mutated.data, new PNG({ width: reference.width, height: reference.height }).data, reference.width, reference.height, { threshold: 0.1 });
  if (mutationDiff === 0) throw new Error("Expected deliberate mutation to produce a visual mismatch, but screenshots were identical.");

  await fs.writeFile(path.join(output, "comparison.json"), JSON.stringify({
    environment: {
      browser: "Chromium via Playwright", browserVersion: browser.version(),
      viewport: "1280x800 CSS px", deviceScaleFactor: 1,
      hostPlatform: process.platform, nodeVersion: process.version
    },
    baselinePixelComparisons: comparison,
    deliberateMutation: { state: "one-active", differingPixels: mutationDiff, expectedDifference: "singular/plural task summary" },
    scopeLimitations: [
      "This run captures the declared Task Board fixture and listed interaction states only; it does not prove completeness for arbitrary software.",
      "Computed style and geometry are browser/OS/font-rendering dependent; portability requires recording the rendering environment.",
      "The API is a deterministic in-memory route adapter, not production network, server, database, authentication, or durable persistence.",
      "Failure behavior is captured as observed, including the absence of a rendered recovery UI."
    ]
  }, null, 2));
  console.log(JSON.stringify({ baselinePixelComparisons: comparison, mutationDifferingPixels: mutationDiff }));
} finally {
  await browser.close();
  await new Promise(resolve => server.close(resolve));
}
