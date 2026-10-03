# onecell for Claude Code

[onecell](https://onecell.io) is durable memory for people and agents: a private Inbox, cells for your projects, and a shared hive for your cluster — one ledger that you and every agent you use can search and cite.

This plugin installs both halves in one step:

- **The onecell MCP server** (`https://onecell.io/api/mcp`), so Claude Code can list your cells, search and cite them, remember facts, and write drafts.
- **The onecell skills** — the rules Claude Code follows: Inbox vs hive, dry runs before writes, search then cite, and when to ask you before moving, sharing or publishing anything.

## Install

In Claude Code:

```
/plugin marketplace add onecell-io/onecell-plugin
/plugin install onecell@onecell
```

Then sign in: run `/mcp`, pick **onecell**, and authenticate. Your browser opens to approve; there is no API key to copy.

Check it worked by asking Claude Code to *list my onecell cells*.

onecell is invite-only for now. You need an account on [onecell.io](https://onecell.io).

## Optional: hooks

A second plugin lets onecell join a session without being asked:

```
/plugin install onecell-hooks@onecell
```

- **Relevant memory:** when a prompt strongly matches something in your onecell, a few lines from it are added to Claude Code's context.
- **Save nudges:** when a turn looks like it decided, merged or shipped something, Claude Code is asked to save a short draft to your private Capture cell.
- **Briefing:** at the start of a session, and after `/clear` or compaction, a few lines on your active cluster, open decisions and recent drafts.

When you enable it, Claude Code asks for an **API key**. Create one at [onecell.io/settings/agents](https://onecell.io/settings/agents#keys) with **Drafts only** ticked, and paste it there; Claude Code keeps it in your system's credential store. The hooks talk to onecell with that key, so they work however onecell itself is connected (this plugin, `claude mcp add`, or not at all). They need `curl` and `jq`.

Each behaviour is **off until you turn it on** at [onecell.io/settings/agents](https://onecell.io/settings/agents#hooks). Once installed, the plugin sends each prompt and Claude's last reply to onecell.io so onecell can decide whether to answer. Neither is stored, and with the switches off onecell ignores them. If you'd rather nothing leave your machine, don't install it.

## Staying current

The skills here are synced from onecell.io daily. Turn on auto-update for this marketplace (`/plugin` → Marketplaces → onecell → Enable auto-update), or run `/plugin marketplace update onecell` now and then.

If onecell ships a new tool and Claude Code can't find it, reconnect the server: `/mcp` → onecell → reconnect.

## Other agents

Claude Desktop, Claude.ai, Cowork, Cursor, VS Code, Codex and Grok each have their own setup — see **[onecell.io/settings/agents](https://onecell.io/settings/agents)**.
