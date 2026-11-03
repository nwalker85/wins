# AGENTS.md — nwalker85/wins

Authoritative instructions for AI agents working in `nwalker85/wins` (Shipped Capability Continuum & Public Done Log).

## Repository Topology & Authority

- **Visibility:** Public (`github.com/nwalker85/wins`)
- **Primary Forge:** GitHub (`git@github.com:nwalker85/wins.git`)
- **Local Custody Path:** `/Users/nate/src/github.com/nwalker85/wins` (`.bare/` + disposable worktrees per Checkout Custody Standard)
- **Live Site:** `https://nwalker85.github.io/wins/` (GitHub Pages from `main` root)

## Hard Rules

1. **NEVER push directly to `main`.** All changes go through a branch worktree and a GitHub Pull Request.
2. **NEVER merge a PR without explicit per-PR approval from Nate.**
3. **NEVER commit unsanitized `/Users/nate/docs/wins.md` to this repository.** Only sanitized entries from `/Users/nate/docs/wins-sanitized.md` and the generated `/Users/nate/docs/wins.html` (`index.html`) belong here.
4. **Sanitization Gate:** Before opening any PR, verify zero matches for internal hostnames (`.ravenmask.net`, `hrafngud`, `bellereve`, `grani`), Linear ticket IDs (`RAV-*`), Outline document IDs, employer/client names, UIDs, or PII.
