---
name: instant
description: >-
  Check whether domain names are registered and find alternatives using the
  Instant MCP server. Use whenever the user asks if a domain is
  available, taken, or free; wants to check a name across extensions (.com,
  .io, .ai, .dev, and hundreds more); needs alternatives because a name is
  taken; or is picking a domain for a project, product, startup, or side
  project. Also use when naming a new app or repository so the suggested
  name comes with a domain the user can actually register.
---

# Instant

The `instant` MCP server from [instant.ai](https://instant.ai) reports domain registration status from
the index behind [instantdomainsearch.com](https://instantdomainsearch.com).
It needs no account, API key, or configuration. Every domain result carries a
`buy_url`, the page where the user registers the domain.

## Tools

Use these three tools on the `instant` MCP server. Your client may
show them with the server name as a prefix; the tool is the same.

| Tool | Use when | Key arguments |
| --- | --- | --- |
| `search_domains` | One name, many extensions | `name` (label only, no extension), `tlds` (optional array, no leading dots), `limit` (1-100, default 32) |
| `check_domain_availability` | Specific full domain names | `domains` (array of `label.tld`, at most 50) |
| `generate_domain_variations` | The name is taken and the user wants alternatives on the same root | `name` (label only), `sort` (`rank` default, or `distance`), `limit` (1-100, default 32) |

### Choosing a tool

- "Is acme.com available?" → `check_domain_availability` with
  `{"domains": ["acme.com"]}`.
- "What extensions can I get acme on?" → `search_domains` with
  `{"name": "acme"}`; add `tlds` when the user names extensions.
- "acme.com is taken, what else?" → `generate_domain_variations` with
  `{"name": "acme"}`, then optionally `search_domains` on the best variations
  with other extensions.
- A list of candidate names → one `check_domain_availability` call with all
  of them (batch, up to 50), not one call per name.

### Argument rules

The server rejects malformed domain input. Normalize before calling so names
and extensions are sent in the expected form:

- `name` is the label only: `acme`, never `acme.com`. Lowercase letters,
  digits, and hyphens; no spaces. Strip spaces from multi-word ideas
  (`"Blue Harbor"` → `blueharbor`).
- `tlds` entries are lowercase with no leading dot: `["com", "io", "co.uk"]`.
- `domains` entries are lowercase full names: `["acme.com", "shop.co.uk"]`.
  The first dot separates label from extension; the server also lowercases names.
- `generate_domain_variations` returns `.com` results only.

## Reading results

Each domain in a result has:

- `label` and `tld`: the two halves of the name.
- `isRegistered`: `true` (in the zone or observed in DNS), `false` (extension
  covered, name absent), or `null` (the index has no data for that extension).
  `search_domains` reports `false` where `check_domain_availability` would
  report `null`, so confirm an unusual extension with
  `check_domain_availability` before calling it available.
- `rank`: how common the extension is, higher is more common.
- `listings` and `markets`: aftermarket listings when the name is for sale.
  `premium` with `is_premium: true` means the registry prices the name above
  standard.
- All prices are USD cents: `premium.usd_cents`, `listings.lowestPrice`, and
  `markets[].price`. `400000` is $4,000.
- `buy_url`: the registration page on instantdomainsearch.com.

Status comes from the search index, built from registry zone files and DNS
observation feeds, not from a live registry query. Say "not registered as of
the last index build" rather than promising the name is free; the registration
page runs the live check.

## Presenting results

- Lead with what the user asked for: available names first, then taken names.
- Render `buy_url` as a markdown link, for example `[Register acme.io](https://instantdomainsearch.com/get/acme.io?src=mcp)`.
- Treat `null` as unknown, not available.
- Mention aftermarket listings and premium prices when present; a listing alone does not prove the domain is registered.
- Do not list every field. Name, status, and the link are enough unless the user asks for more.

## Example

User: "I'm building a CLI called shipwright. Can I get the domain?"

1. Call `search_domains` with `{"name": "shipwright", "tlds": ["com", "dev", "io", "sh"]}`.
2. If every result is registered, call `generate_domain_variations` with `{"name": "shipwright", "limit": 10}`.
3. Reply with the available names and their registration links, and note which were taken.
