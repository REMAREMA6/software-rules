const express = require("express");
const paths = ["/Report", "/report", "/Report/", "/report/"];

async function request(port, route) {
  const response = await fetch(`http://127.0.0.1:${port}${route}`);
  await response.arrayBuffer();
  return { path: route, status: response.status };
}

async function runProfile(label, caseSensitive, strict) {
  const app = express();
  if (caseSensitive !== null) app.set("case sensitive routing", caseSensitive);
  if (strict !== null) app.set("strict routing", strict);
  app.get("/Report", (_req, res) => res.status(200).send("matched"));
  const server = app.listen(0, "127.0.0.1");
  await new Promise(resolve => server.once("listening", resolve));
  const port = server.address().port;
  const decisions = [];
  for (const path of paths) decisions.push(await request(port, path));
  await new Promise((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
  return { label, config: { caseSensitive, strict, activation: "before-first-request" }, decisions };
}

async function runLateMutation() {
  const app = express();
  app.get("/Report", (_req, res) => res.status(200).send("matched"));
  const server = app.listen(0, "127.0.0.1");
  await new Promise(resolve => server.once("listening", resolve));
  const port = server.address().port;
  const decisions = [await request(port, "/Report")];
  app.set("case sensitive routing", true);
  decisions.push(await request(port, "/report"));
  await new Promise((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
  return { label: "late-case-sensitive-change", config: { caseSensitive: "changed-to-true-after-first-request", strict: false, activation: "after-router-initialization" }, decisions };
}

(async () => {
  const scenarios = [];
  scenarios.push(await runProfile("defaults", null, null));
  scenarios.push(await runProfile("case-sensitive", true, false));
  scenarios.push(await runProfile("strict", false, true));
  scenarios.push(await runProfile("case-sensitive-and-strict", true, true));
  scenarios.push(await runLateMutation());
  console.log(JSON.stringify({ source: "Express 5.3.0", sourceCommit: process.env.EXPRESS_SOURCE_COMMIT, scenarios }, null, 2));
})().catch(error => { console.error(error); process.exit(1); });
