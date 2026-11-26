# Source candidate — Medusa

**Repository:** medusajs/medusa  
**URL:** https://github.com/medusajs/medusa  
**Immutable inspected commit:** 6e28e10acb9676392315b3ff1a9c7147fce4b5ab  
**Licence:** Repository states MIT except Enterprise Edition materials identified in ENTERPRISE-LICENSE.md; exclude Enterprise-only files unless separately licensed.  
**Primary stack:** TypeScript/Node.js commerce platform.  
**Candidate facets:** Business rules; data; behaviour; persistence; API; integrations.

## Evidence inspected

- packages/modules/cart/AGENTS.md describes cart workflows that coordinate pricing, promotions, taxes, inventory, and cart completion.
- A pricing integration test path exists at packages/modules/pricing/integration-tests/__tests__/services/pricing-module/calculate-price.spec.ts and includes expected monetary totals.
- These source references are leads only. Inspect the actual workflow, tests, data model, and runtime before defining a rule.

## Candidate rule areas

Promotion eligibility and application; price calculation; tax-inclusive/exclusive amounts; cart consistency when items or shipping methods change.

**Status:** candidate only; select MIT-licensed modules, inspect tests, and run controlled scenarios before capture.
