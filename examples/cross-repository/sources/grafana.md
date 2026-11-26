# Source candidate — Grafana

**Repository:** grafana/grafana  
**URL:** https://github.com/grafana/grafana  
**Immutable inspected commit:** d82f399ab7ff0aba6b762f6137fe72ec06be0480  
**Licence:** GNU AGPL v3 (LICENSE at inspected commit; confirm obligations before redistributing a derivative)  
**Primary stack:** Go backend and web frontend; exact module boundary to be selected.  
**Candidate facets:** Configuration; integrations; identity/authentication; authorization; API; performance/resources.

## Evidence inspected

- conf/defaults.ini contains documented default settings and comments describing runtime options.
- pkg/setting/setting_nats.go contains a typed NATS authentication configuration model and comments describing supported modes.
- These source declarations are not runtime observations of effective configuration or precedence.

## Candidate rule areas

Configuration defaults and effective settings; precedence between defaults, environment, and configuration files; mode-based NATS authentication selection.

## Boundary and limitations

Select one isolated configuration setting and one observable runtime effect. Inspect the actual loader and tests before writing a rule. Do not infer precedence from defaults.ini alone. Record AGPL implications and avoid copying code unnecessarily.

**Status:** candidate only; no Phase 6 pass claimed.
