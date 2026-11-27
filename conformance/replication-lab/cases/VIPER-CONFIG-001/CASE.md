# Case — Viper configuration source precedence and environment mapping

**Case ID:** VIPER-CONFIG-001  
**Status:** Pending runtime and evidence validation.  
**Facet(s):** Configuration; behaviour; data; errors and recovery  
**Source:** https://github.com/spf13/viper  
**Immutable source commit:** `394040caccbdf5821fa6839386a35f0fb1b1ee9e`  
**Source version:** Viper v1.21.0  
**Source stack:** Go  
**Replica stack:** Python 3.12  
**Licence:** MIT

## Declared scope

The case exercises Viper's configuration lookup precedence across defaults, YAML files, environment variables, changed command-line flags, and explicit runtime overrides. It also tests automatic environment mapping, nested-key replacement, explicit environment binding, case-insensitive file keys, and empty environment values.

## Technology-independent rules

1. A default value is returned only when no higher-precedence source provides a value.
2. File values override defaults.
3. Environment values override file values when automatic environment lookup is enabled.
4. Changed command-line flags override environment and file values.
5. Explicit runtime overrides have the highest precedence.
6. A configured key replacer maps nested keys to environment variable names.
7. Explicit environment bindings map a named environment variable to a logical key.
8. Key lookup is case-insensitive for the selected YAML configuration keys.
9. With AllowEmptyEnv enabled, an explicitly empty environment value is not treated as absent.

## Probes and mutations

Nine deterministic scenarios cover defaults, YAML, environment, flags, overrides, empty environment values, nested key mapping, explicit binding, and full precedence. Six mutations alter precedence or environment lookup semantics.

## Acceptance gate

Accept only after all nine source/replica configuration outcomes match, all six mutations are detected, and Software Rules 0.2.0 captures/comparison pass schema and cross-record integrity validation. This is bounded Viper configuration evidence, not complete configuration-facet coverage.
