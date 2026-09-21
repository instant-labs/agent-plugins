# Instant: Claude plugin directory submission

Submit at [Claude's plugin submission form](https://claude.ai/admin-settings/directory/submissions/plugins/new)
after the rebrand is published to the repository's `main` branch. The values
below are prepared listing content; they are not confirmation of a submission.

## Listing details

| Field | Value |
| --- | --- |
| Plugin name | `instant` |
| Display name | Instant |
| Publisher | instant.ai |
| Version | `1.0.1` |
| Category | Development / Developer Tools, according to the form's available categories |
| Website | <https://instant.ai> |
| Documentation | <https://instant.ai/mcp> |
| Public repository | <https://github.com/instant-labs/agent-plugins> |
| Plugin directory | `plugins/instant` |
| Plugin source URL | <https://github.com/instant-labs/agent-plugins/tree/main/plugins/instant> |
| Claude manifest | `plugins/instant/.claude-plugin/plugin.json` |
| Marketplace manifest | `.claude-plugin/marketplace.json` |
| Marketplace name | `instant-marketplace` |
| Install identifier | `instant@instant-marketplace` |
| MCP endpoint | `https://mcp.instant.ai/mcp` |
| Transport | Streamable HTTP |
| Authentication | None; no account or API key required |
| Cost | Free to use; domain registration is a separate purchase on the linked registration site |
| Privacy policy | <https://instant.ai/policies/privacy> |
| Terms of use | <https://instant.ai/policies/terms> |
| Support | <https://instant.ai/contact> |
| Issue tracker | <https://github.com/instant-labs/agent-plugins/issues> |
| License | MIT |
| Icon | [1024 × 1024 PNG](../plugins/instant/assets/logo.png), with [SVG source](../plugins/instant/assets/logo.svg) |

Use the submitting account's real contact information for any contact fields.
Review any publisher attestations in the form before submitting.

## Short description

Find domains and name ideas with instant.ai.

## Description

Find available domains and brandable names with instant.ai. Check names across
extensions, verify domains in bulk, generate alternatives, and search USPTO
trademark records. Free, with no account or API key required.

## Features and use cases

- Search one name across hundreds of domain extensions.
- Check up to 50 full domain names in one request.
- Generate prefix and suffix alternatives when a name is taken.
- Brainstorm names for a project, product, or company and check the domains.
- Inspect registration links, aftermarket listings, and premium pricing.
- Search indexed USPTO trademark records and inspect a matching filing.

## Reviewer setup

After the rebrand is published, install from the public marketplace:

```sh
claude plugin marketplace add instant-labs/agent-plugins
claude plugin install instant@instant-marketplace
```

Start a new session, then try:

1. `/instant:domain example.com example.net` — returns indexed registration
   status for both domains.
2. `/instant:domain northstar com ai dev` — searches one name across extensions.
3. `/instant:domain-variations northstar` — suggests `.com` alternatives.
4. "Suggest five brandable names for a matcha cafe and check their .com domains."
   — uses the brainstorming skill and checks candidates before presenting them.
5. "Search USPTO trademarks for northstar, then show the details of a matching
   record." — searches indexed records and reports snapshot freshness.

Domain registration status comes from a daily search index. Uncovered
extensions can have unknown status; registration links perform the live check.
Trademark results report the indexed snapshot and do not establish legal
clearance for a name.

## Data access and behavior

The plugin contains Markdown instructions, assets, and an MCP configuration.
It has no hooks, agent definitions, scripts, local processes, or credentials.
All MCP calls go to `https://mcp.instant.ai/mcp` and send the tool arguments to
Instant's hosted service. Domain results link to `instantdomainsearch.com`.

The server exposes six tools:

- `search_domains`
- `check_domain_availability`
- `generate_domain_variations`
- `search_trademarks`
- `get_trademark_details`
- `submit_feedback`

Search and detail tools read indexed data. The feedback tool writes a feedback
message; the plugin's skill restricts it to user-requested feedback and excludes
search queries, domain names, results, and private details. The plugin does not
register or purchase domains.

## Release and submission

1. Publish the validated rebrand to `main`. Confirm the plugin source URL above
   resolves to version `1.0.1` and the marketplace entry points to `./plugins/instant`.
2. Open the submission form in a signed-in Claude admin session. Complete any
   browser verification shown by Claude.
3. Enter the listing details and description, attach the PNG icon if requested,
   and complete account-specific fields and attestations.
4. Submit and retain the confirmation or submission identifier.

For subsequent edits, run the repository checks before publishing:

```sh
python3 scripts/validate.py
rumdl check .
claude plugin validate plugins/instant
claude plugin validate .claude-plugin/marketplace.json
```
