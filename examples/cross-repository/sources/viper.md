# Source record — Viper configuration library

**Repository:** spf13/viper  
**URL:** https://github.com/spf13/viper  
**Immutable inspected commit:** 394040caccbdf5821fa6839386a35f0fb1b1ee9e  
**Release:** v1.21.0  
**Licence:** MIT  
**Primary stack:** Go  
**Selected facet:** Configuration; behaviour; data

## Evidence inspected

- Pinned Viper module source and Go module manifest.
- Configuration lookup precedence for defaults, files, environment variables, changed pflag flags, and runtime overrides.
- Automatic environment mapping, nested key replacers, explicit environment bindings, case-insensitive YAML keys, and empty environment handling.

## Accepted bounded case

[VIPER-CONFIG-001](../../conformance/replication-lab/cases/VIPER-CONFIG-001/CASE.md) compares pinned Viper v1.21.0 with an independent Python 3.12 model across nine configuration scenarios. Six deliberate mutations were detected; Software Rules 0.2.0 captures/comparison passed schema and evidence-integrity validation in [run #45941776949](https://github.com/REMAREMA6/software-rules/actions/runs/45941776949), artifact `15172438139`.

## Boundary and limitations

Remote providers, watchers/reload, secret managers, multiple-file merge, custom merge strategies, and application-specific runtime reconfiguration remain outside scope. This is not complete Viper or configuration-facet coverage.
