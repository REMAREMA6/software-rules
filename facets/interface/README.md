# Interface Facet

**Maturity:** Draft — Software Rules specification 0.3.0  
**Facet ID:** `interface`  
**Purpose:** Capture the observable structure and presentation of a running user interface so independent implementations can be compared without depending on the original UI framework.

## 1. Boundary

The interface facet covers what a human or assistive technology can perceive or inspect at the UI boundary:
- Rendered hierarchy and node identity/relationships.
- Resolved visual properties and layout geometry.
- Positioning, clipping, visibility, transforms, and stacking.
- Text and other rendered content.
- Accessibility semantics and exposed interaction affordances.
- UI assets and their resolved references.
- Current UI state and the visible result of a state change.
- Viewport, device, platform, and rendering context.

It does not define the business meaning of an action, domain policy, durable storage, API exchange, or authorization decision. Those belong to their own facets and may be linked to interface observations.

A web DOM is one platform-specific observation source, not the definition of the facet. Native interfaces require equivalent platform inspection, such as a native view hierarchy and accessibility tree. Where a platform has no inspectable tree, record the available black-box evidence and its limitations.

## 2. Required capture context

Record target/build, platform and OS version, application/browser and version, viewport/window dimensions, device scale factor or density, orientation, locale, timezone when it affects rendering, color scheme, reduced-motion setting, zoom/text scaling, input modality, font availability, relevant user/permission state, route/screen, initial state, and capture timing/readiness condition. Mark unknown or unavailable values explicitly.

For responsive interfaces, viewport dimensions and relevant device configuration are part of the comparison conditions, not incidental metadata.

## 3. Observable dimensions

| Dimension | Required information |
|---|---|
| Hierarchy | Node/element identity within capture, node type, parent/child and sibling order, shadow/embedded boundaries where inspectable |
| Attributes/state | Relevant attributes, properties, form values, selected/checked/disabled/expanded/focused state, platform equivalents |
| Content | Rendered text, accessible name/description, content type, truncation/overflow evidence; sensitive values may be redacted |
| Computed presentation | Resolved/computed properties after cascade, inheritance, variables, defaults, and layout resolution; include property names, values, units, and source/inspection method |
| Geometry | Bounding rectangle, coordinate space, dimensions, box model where available, scroll offsets, viewport relation |
| Positioning | Position mode, containing block/context where inspectable, offsets, transforms, clipping and overflow |
| Layering | Stacking-context membership, z-order/paint order where obtainable, overlays, modal/top-layer state; do not treat a raw z-index number as a complete global order |
| Visibility | Rendered/visible state, occlusion if measured, display/visibility/opacity, viewport intersection, clipping; distinguish hidden from not inspected |
| Accessibility | Role, accessible name/description, states/properties, relationships, focus order, keyboard affordances, live-region semantics |
| Interaction affordances | Exposed action type, enabled state, target, focusability, hit region if measurable; actual action outcome links to Behaviour |
| Assets | Resolved image/font/icon/media reference, intrinsic dimensions, rendered dimensions, format, source/variant where observable, loading/failure state |
| Rendering evidence | Screenshot/video/frame reference, capture dimensions, timestamp, and correspondence to structured snapshot |
| UI state | Route/screen, active tab, open menu/dialog, validation state, loading/empty/error state, selection and other visible state |

Do not assume a CSS property has the same meaning on native platforms. Facet payloads may use platform-specific property groups while retaining shared semantic concepts.

## 4. Resolution requirements

The primary representation is the value resolved by the running platform at capture time, not merely the authored stylesheet or component declaration. Preserve:
- Raw platform-reported value and unit.
- Normalized value only when a documented normalization is possible.
- Property/source method (for example computed style, layout API, native inspector).
- Coordinate system and measurement precision.
- Browser/engine/platform version and relevant rendering configuration.

Do not substitute declared CSS, design tokens, source constants, or framework props for computed runtime values. Such declarations may be linked as source/contract evidence, separately classified.

For web captures, distinguish computed values from used/actual layout measurements where the platform APIs expose both. Record the exact API/method rather than calling all values “computed style”.

## 5. Node identity and hierarchy

Node identifiers need only be stable within a defined snapshot/session unless a stronger identity mechanism is demonstrated. Record the identity scope and matching hints separately (stable application key, accessibility identifier, selector/path, native resource ID). Do not assume generated DOM IDs or memory addresses are stable across runs.

Preserve parent-child structure and order. If a node cannot be inspected, record the gap and its cause; do not silently omit it from a claim of complete hierarchy capture. For virtualized lists, record the rendered window and virtualization limitations.

## 6. Geometry and layering

Every geometry value identifies its coordinate space (viewport, document, screen, window, local parent, or platform-specific space), origin, units, precision, and capture time. Record scroll offsets and transforms needed to interpret positions. Geometry from different coordinate spaces must not be compared directly.

Layering is more than numeric z-index. Record stacking contexts/roots and paint-order evidence where available, including fixed/sticky positioning, modal/top-layer behavior, native elevation, and overlays. If exact paint order cannot be established, state that limitation.

## 7. Accessibility

Capture the platform-exposed accessibility tree independently of visual hierarchy when they differ. Record role, name, description, states, properties, relationships, focusability, focus order, and relevant actions. An accessibility tree does not prove visual appearance; a screenshot does not prove accessible semantics.

## 8. Assets

Capture resolved asset identity rather than only a source path where possible. Record asset URL/resource identifier, final resolved URL or platform resource, format, intrinsic and rendered dimensions, object-fit/content mode, crop/position, font family/weight/style as resolved, load status, and evidence. Respect access controls and avoid copying proprietary asset bytes unless authorized.

## 9. Scenario and state coverage

A capture plan should cover relevant routes/screens, viewport classes, orientation, responsive breakpoints, interaction states, focus/hover/pressed/disabled states, dialogs/menus, loading/empty/error/success states, scrolling, dynamic content, and user/permission variations. Do not claim full interface coverage from one screenshot or one DOM snapshot.

## 10. Observation payload concept

A facet observation may contain:
- Snapshot identity and capture time.
- Platform and viewport context.
- Root(s) and ordered node records.
- Node identity, parent, order, type, attributes/state/content.
- Resolved style/property map.
- Geometry and coordinate metadata.
- Positioning, clipping, visibility, and layering data.
- Accessibility record or linked accessibility snapshot.
- Asset references and loading state.
- UI state and rendering evidence references.
- Completeness, exclusions, redactions, and inspection limitations.

This is a conceptual payload inventory. The current draft JSON Schema mapping is maintained in `schemas/v1/facets/interface.schema.json`; platform-specific adapters and completeness of an individual inventory remain scope-dependent.

## 11. Evidence and limitations

Preferred evidence includes structured DOM/native hierarchy snapshots, platform-reported computed/resolved properties, layout geometry, accessibility snapshots, asset resolution records, and screenshots/video frames for visual corroboration. Record tool/API and version, collection timing, permissions, sampling, and known observer effects.

Screenshots are useful evidence but insufficient as the sole representation: they do not reliably expose hierarchy, exact values, accessibility semantics, hidden states, or responsive constraints. Conversely, structured snapshots may not reproduce anti-aliasing, font rasterization, animation, or compositor output exactly.

## 12. Cross-facet links

- Interface → Behaviour: action/trigger and resulting UI transition.
- Interface → Business rules: displayed decision/validation result, without inferring the underlying rule solely from appearance.
- Interface → Data: displayed values and formatting, linked to data observations when established.
- Interface → Identity/Authorization: identity state and access-dependent affordances; do not infer authorization solely from a hidden/disabled control.
- Interface → API/Integrations: network activity only when separately observed.
- Interface → Errors and recovery: visible error presentation linked to the underlying failure where known.

## 13. Worked conceptual example

**Scenario:** Open a product listing at a 1280 × 800 CSS-pixel viewport after the page reaches its defined ready condition.

**Execution:** One navigation against a named build, browser/OS version, locale, and user state.

**Observations:** Capture the rendered node tree and parent/child order; resolved typography, colors, spacing and layout properties; element rectangles in viewport CSS pixels; scroll position; stacking contexts and overlay state; accessibility tree; resolved image/font assets; screenshot.

**Rule proposition:** Under the specified build, route, viewport, and state, the listing exposes the captured hierarchy, resolved presentation, geometry, and accessibility semantics.

**Limitations:** This one execution does not establish mobile layout, other browsers, hover/focus states, later asynchronous content, or all products. This example is illustrative, not a capture from a real target.

## 14. Research mappings

The facet should reuse DOM/CSSOM and WebDriver concepts for web inspection, WAI-ARIA for accessibility semantics, and platform accessibility/UI inspection APIs for native interfaces. These are observation sources and domain standards, not a complete cross-platform Software Rules payload. See [standards review](././research/STANDARDS-REVIEW.md) and [references](././research/REFERENCES.md).
