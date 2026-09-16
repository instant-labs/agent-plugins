# Instant agent plugins

Plugins that connect coding agents to Instant's products. Each plugin bundles
an MCP server pointer, skills that teach the agent when and how to use it, and
slash commands. The same plugin directory installs into Claude Code, Codex,
Cursor, Grok Bot, and Grok Build; only the manifest file differs per client.

| Plugin | What it does | MCP server |
| --- | --- | --- |
| [instantdomainsearch](plugins/instantdomainsearch) | Domain availability across hundreds of extensions, bulk checks, and alternatives when a name is taken | `https://api.instantdomainsearch.com/mcp`, no auth |

Nothing here runs code on your machine. Every plugin is a hosted MCP pointer
plus markdown. See each plugin's README for the endpoints it calls.

## Install

The marketplace name is `instant-marketplace`; plugin ids are the directory
names under `plugins/`.

### Claude Code

```sh
claude plugin marketplace add instant-labs/agent-plugins
claude plugin install instantdomainsearch@instant-marketplace
```

### Codex

```sh
codex plugin marketplace add https://github.com/instant-labs/agent-plugins
codex plugin add instantdomainsearch@instant-marketplace
```

### Cursor and Grok Bot

Search for **Instant Domain Search** under **Settings → Plugins**. If it is
not listed yet, click **Import** under **Team Marketplaces** and paste
`https://github.com/instant-labs/agent-plugins`, then install it from there.

### Grok Build

```sh
grok plugin marketplace add instant-labs/agent-plugins
grok plugin install instantdomainsearch --trust
```

### Skills only

```sh
npx skills add instant-labs/agent-plugins
```

This installs the skills without the MCP server. Add the server yourself from
[instantdomainsearch.com/mcp](https://instantdomainsearch.com/mcp).

## Layout

```text
.grok-plugin/marketplace.json      catalog read by Grok Build
.claude-plugin/marketplace.json    catalog read by Claude Code
.cursor-plugin/marketplace.json    catalog read by Cursor and Grok Bot
.agents/plugins/marketplace.json   catalog read by Codex
plugins/<name>/
  .grok-plugin/plugin.json         one manifest per client, same content
  .claude-plugin/plugin.json
  .cursor-plugin/plugin.json
  .codex-plugin/plugin.json        adds the `interface` block Codex shows in its directory
  .mcp.json                        MCP servers, `type: http`
  .cursor-mcp.json                 the same servers in Cursor's format (no `type`)
  skills/<skill>/SKILL.md
  commands/<command>.md
  assets/
  README.md
scripts/validate.py                checks manifests and catalogs agree
```

Skills refer to tools by their MCP name (`search_domains`) and the server
(`instantdomainsearch`), never a client's prefixed form, so one skill file
serves every client.

## Checks

Run `python3 scripts/validate.py` before you push; CI runs the same check.

## License

MIT. See [LICENSE](LICENSE).
