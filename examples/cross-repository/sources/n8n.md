# Source candidate — n8n

**Repository:** n8n-io/n8n  
**URL:** https://github.com/n8n-io/n8n  
**Immutable inspected commit:** c07a0ac9c7186d893fdea2123d550e0b19a57dce  
**Licence:** Sustainable Use License with additional file/edition restrictions; LICENSE.md explicitly says some Enterprise-marked files are not licensed under the Sustainable Use License. Review the exact files before any reuse.  
**Primary stack:** TypeScript/Node.js workflow automation platform.  
**Candidate facets:** Integrations; behaviour; background processing; errors/recovery; data; authentication; API.

## Evidence inspected

- packages/nodes-base/TESTING_PROMPT_WORKFLOW.md calls for end-to-end workflow execution, API-failure scenarios, binary data handling, and authentication coverage.
- This is testing guidance, not direct evidence of a specific integration's runtime contract.

## Candidate rule areas

Select one community-licensed node/integration and capture its input mapping, authentication requirements, execution order, output transformation, and failure behaviour.

## Boundary and limitations

Exclude Enterprise-marked code unless licensing is separately established. Verify the selected node's exact licence status, external provider contract, and runtime tests. Use a controlled provider test double for deterministic failure probes.

**Status:** candidate only; no Phase 6 pass claimed.
