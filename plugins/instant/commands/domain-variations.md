---
name: domain-variations
description: Generate prefix and suffix alternatives for a taken name and show which are available
argument-hint: <name> [--distance] [--limit N]
---

# Generate domain alternatives

Generate domain alternatives for: $ARGUMENTS

Call `generate_domain_variations` on the `instant` MCP server with `name` set to the
first argument, lowercased, with any extension, spaces, and leading dots
stripped. The server rejects names that contain an extension or spaces.
Pass `sort: "distance"` when `--distance` is present, otherwise leave `sort`
unset. Pass `limit` when `--limit N` is present, otherwise 20.

Results are `.com` only. Reply with the available names first, each with its
`research_url` as a markdown link, then a short line on how many were taken. Offer
to check the best names on other extensions with `/domain <name> io dev ai`.
