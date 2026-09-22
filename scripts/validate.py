#!/usr/bin/env python3
"""Check that every plugin's manifests and the root catalogs agree.

Run from the repository root. Exits non-zero on the first group of problems.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
MANIFEST_DIRS = (".grok-plugin", ".claude-plugin", ".cursor-plugin", ".codex-plugin")
SHARED_FIELDS = ("name", "version", "description", "author", "homepage", "repository", "license", "keywords")
CATALOGS = {
    "grok": ROOT / ".grok-plugin" / "marketplace.json",
    "claude": ROOT / ".claude-plugin" / "marketplace.json",
    "cursor": ROOT / ".cursor-plugin" / "marketplace.json",
    "codex": ROOT / ".agents" / "plugins" / "marketplace.json",
}
GENERIC_KEYWORDS = {
    "domain", "domains", "mcp", "api", "cli", "search", "database", "deploy",
    "domain availability", "domain brainstorming", "trademark", "trademarks", "uspto trademarks",
}


def load(path: Path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        raise SystemExit(f"missing: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"invalid JSON in {path.relative_to(ROOT)}: {e}")


def frontmatter(path: Path) -> dict:
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fields = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line and not line.startswith((" ", "\t")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def check_plugin(plugin: Path, problems: list[str]) -> dict:
    rel = plugin.relative_to(ROOT)
    manifests = {d: load(plugin / d / "plugin.json") for d in MANIFEST_DIRS}
    base = manifests[".grok-plugin"]
    if base.get("name") != plugin.name:
        problems.append(f"{rel}: manifest name {base.get('name')!r} != directory name")
    for d, m in manifests.items():
        for field in SHARED_FIELDS:
            if m.get(field) != base.get(field):
                problems.append(f"{rel}/{d}/plugin.json: {field} differs from .grok-plugin/plugin.json")
        if d != ".codex-plugin" and m.get("displayName") != base.get("displayName"):
            problems.append(f"{rel}/{d}/plugin.json: displayName differs from .grok-plugin/plugin.json")
    codex = manifests[".codex-plugin"]
    for field in ("skills", "mcpServers", "interface"):
        if field not in codex:
            problems.append(f"{rel}/.codex-plugin/plugin.json: missing {field}")
    if codex.get("interface", {}).get("displayName") != base.get("displayName"):
        problems.append(f"{rel}: codex interface.displayName != displayName")
    if manifests[".cursor-plugin"].get("mcpServers") != "./.cursor-mcp.json":
        problems.append(f"{rel}/.cursor-plugin/plugin.json: mcpServers must be './.cursor-mcp.json'; Cursor only auto-discovers mcp.json")
    for kw in base.get("keywords", []):
        if kw.lower() in GENERIC_KEYWORDS:
            problems.append(f"{rel}: generic keyword {kw!r}; reviewers reject these")

    mcp = load(plugin / ".mcp.json").get("mcpServers", {})
    cursor_mcp = load(plugin / ".cursor-mcp.json").get("mcpServers", {})
    if set(mcp) != set(cursor_mcp):
        problems.append(f"{rel}: .mcp.json and .cursor-mcp.json list different servers")
    for name, server in mcp.items():
        if server.get("type") != "http" or not str(server.get("url", "")).startswith("https://"):
            problems.append(f"{rel}/.mcp.json: server {name} must be type http with an https url")
        if cursor_mcp.get(name, {}).get("url") != server.get("url"):
            problems.append(f"{rel}: server {name} url differs between .mcp.json and .cursor-mcp.json")

    for skill in sorted((plugin / "skills").glob("*/SKILL.md")):
        fm = frontmatter(skill)
        if "name" not in fm or "description" not in fm:
            problems.append(f"{skill.relative_to(ROOT)}: frontmatter needs name and description")
        if fm.get("name") not in (None, skill.parent.name):
            problems.append(f"{skill.relative_to(ROOT)}: name != directory name")
    for command in sorted((plugin / "commands").glob("*.md")):
        fm = frontmatter(command)
        for field in ("name", "description", "argument-hint"):
            if field not in fm:
                problems.append(f"{command.relative_to(ROOT)}: frontmatter needs {field}")
        if "$ARGUMENTS" not in command.read_text():
            problems.append(f"{command.relative_to(ROOT)}: body never uses $ARGUMENTS")
    for text in (plugin / "skills").rglob("*.md"):
        if "__" in text.read_text() and any(f"{plugin.name}__" in line for line in text.read_text().splitlines()):
            problems.append(f"{text.relative_to(ROOT)}: uses a client-prefixed tool name")
    if not (plugin / "README.md").is_file():
        problems.append(f"{rel}: missing README.md")
    return base


def check_catalogs(plugins: dict[str, dict], problems: list[str]) -> None:
    names = set(plugins)
    for client, path in CATALOGS.items():
        catalog = load(path)
        entries = {e["name"]: e for e in catalog.get("plugins", [])}
        for missing in sorted(names - set(entries)):
            problems.append(f"{path.relative_to(ROOT)}: no entry for {missing}")
        for extra in sorted(set(entries) - names):
            problems.append(f"{path.relative_to(ROOT)}: entry {extra} has no plugin directory")
        for name, entry in entries.items():
            source = entry.get("source")
            path_value = source["path"] if isinstance(source, dict) else source
            if path_value != f"./plugins/{name}":
                problems.append(f"{path.relative_to(ROOT)}: {name} source is {path_value!r}")
            if client == "codex" and ("policy" not in entry or "category" not in entry):
                problems.append(f"{path.relative_to(ROOT)}: {name} needs policy and category")
            if client != "codex":
                for field in ("description", "displayName", "author", "homepage", "keywords"):
                    if entry.get(field) != plugins.get(name, {}).get(field):
                        problems.append(f"{path.relative_to(ROOT)}: {name} {field} differs from the manifest")


def main() -> int:
    problems: list[str] = []
    plugins = {p.name: check_plugin(p, problems) for p in sorted(PLUGINS.iterdir()) if p.is_dir()}
    check_catalogs(plugins, problems)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    print(f"OK: {len(plugins)} plugin(s), 4 catalogs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
