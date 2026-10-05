---
name: onecell
description: >
  Use the onecell hive over MCP — personal Inbox plus shared team cells, hybrid
  search, mermaid artifacts, memory facts, invites. Trigger when the user mentions
  onecell, the hive, cells, Inbox vs shared notes, MCP search, mermaid in the hive,
  or connecting Codex/Claude/Cowork/Grok/Cursor to onecell.io. Also trigger when any
  other skill or workflow (Notion, shopping, email, research, coding) produces a
  durable decision, artifact, receipt, or account fact worth keeping — even if the
  user did not say onecell — to offer saving it.
---

# onecell

A workspace is one person. Inbox is private. The hive is a cell teammates share with you. You see your own cells plus what is shared with you, never anyone else's Inbox.

Connect at `{origin}/api/mcp` (OAuth) or Bearer `ic_…`. First install: fetch `{origin}/agent-setup/prompt.md` and run this client's section (Codex: `codex mcp add` + `codex mcp login`, see `{origin}/agent-setup/codex`; Cowork: Claude.ai Connectors custom URL; Grok: add the MCP URL in chat). This skill lives at `{origin}/skills/onecell.md`.

## Keep this skill fresh

Saved copies drift. Once per agent session, after MCP connects and before real hive work: re-fetch `{origin}/skills/onecell.md` (and `{origin}/skills/onecell-bridge.md` if this client keeps it) and overwrite the local copies. If the live skill names tools you do not have, re-run agent-setup: a skill file alone is not a working install.

## Health check

1. Tools include at least `list_cells`, `search`, `recall`, `remember`, `get_fact`, `create_document`, `get_document`.
2. `list_cells` shows Inbox plus shared cells; `get_active_cluster` (and `list_clusters` if you may be in several).
3. `recall` (empty query lists recent facts) or `search` a short real query.
4. A tool this skill names is missing (say `move_cell`)? The client cached an old tool list. Ask the human to reconnect onecell (Claude Code: `/mcp` → reconnect) rather than working around it.

## Clusters

One login can belong to several clusters. Inbox is one private cell shown in every cluster; every other cell, hive included, belongs to one cluster. `list_cells`, `search`, `recall` and `list_documents` cover the **active** cluster plus Inbox; naming a cell by slug or id works in any cluster.

- The active cluster is one preference shared with the human's sidebar. To look around, use `list_cells` `all_clusters: true`; to work elsewhere, name the `cell`. Switch (`set_active_cluster`) only when the human asks or for member and invite work there (Decision points → Switch cluster).
- New cells land in the active cluster. Invites, `list_invites`, `list_members` and `share_cell` follow the active cluster; its owner invites.
- `create_cluster` makes the new cluster active, switching the human's sidebar (Decision points → Create a cluster). `join_cluster` accepts a pending invite for this email.

## First moves

1. `list_cells`: note `owned`, slug, `embedding_policy` (`none` is never searchable; `local_only` needs a local embedder). `create_cell` opens one in your workspace, shared with no one until `share_cell`.
2. `search` the question (optional `cell`). Hits come grouped by document with short passages and heading trails; a query always returns candidates, so judge by score. For settled, load-bearing context (what to build on, not every mention) pass `weight: true`: among close matches, documents more sources link to rank higher.
3. `get_document` only for the hit you will use. On a long page: `outline`, then `section` (a heading's id) or `blocks` (ids).

Cite as: cell · heading path · passage. Never paste a whole document into the reply.

## Decision points

Some choices belong to the human. Ask in one line and name the default; skip what they already answered. If this client cannot ask, take the default: it is always the least exposed choice. `dry_run` checks the call; this table checks the person. Do both.

| Moment | Ask | Default |
|---|---|---|
| Capture — another skill produced durable work | "Save {one-line summary} to your Inbox?" | Write nothing. Mention it once in the reply. |
| Shape — `recall` / `search` found a close note or fact | "Update {title}, or start a new note?" One sentence → `remember`; longer → document. | New Inbox draft that links the near match. Never overwrite. |
| Destination | "Inbox (private) or {hive / named cell}?" Offer only cells you can write to. | Inbox |
| New cell | "Create cell {name}, or use {existing}?" | Existing cell, else Inbox |
| Publish | "Publish, or keep as draft?" `validate_document` `strict: true` first; say what it would fix. | Draft |
| Contradicting fact | "Replace '{old}' with '{new}'?" (`remember` with `supersedes`) | Keep the old fact. Report the conflict. |
| Share a cell | "Share {cell} with {who} as viewer or editor?" | Viewer |
| Public link | "Create a public link? Anyone with it can read {title}." | No link |
| Invite | "Email the invite, or give you a join link to paste?" | Email |
| Trash | "Trash {title}? Restorable for 30 days." | Don't |
| Move | "Move {title} (+{n} nested) from {cell} to {cell} in {cluster}?" See Move work. | Don't |
| Create a cluster | "Create cluster {name}? It becomes your active cluster, so your sidebar switches to it." | Don't |
| Switch cluster | "Switch to {cluster}? Your sidebar switches too." | Don't. Name cells with `cell`, or find them with `list_cells` `all_clusters`. |
| Move a cell to a cluster | "Move {cell} ({n} docs) to {cluster}? {people} aren't in {cluster}, so it leaves their sidebar and search." | Don't |
| Move out of a shared cell | "{from} is shared — the people there lose {title}. Move anyway?" | Don't |
| Mention | "Mention {name}? They're told in onecell and by their agent." | Don't — only someone the human named or asked to bring in |

## Move work

Where work lives decides who sees it, so moving is the human's call. Never pick a destination silently.

1. **Which.** Use the document the human named; otherwise `search` and offer up to three. Several → confirm the set once.
2. **Where.** `list_cells` `all_clusters: true`; offer two or three cells you own (`owned: true`), grouped by cluster, active first, plus Inbox. Nothing fits → ask about a new cell; never invent one.
3. **Dry run** `update_document` with `id` and `cell`. Read `move`: `children` come along, `to.cluster` is where it lands, `leaves_shared` means people who see the current cell lose it.
4. **Confirm** in one line; if `leaves_shared`, name who loses it and default to no. Then the same call with `dry_run: false`, and reply with `{origin}/cells/{to.slug}/{documentId}`. If it landed outside the active cluster, say so; don't switch for them.

**A whole cell** that belongs in another cluster (a project spinning out): `move_cell` keeps its documents, memory, shares and links together. Dry run each; `losing_access` names people not in the destination. Confirm per cell (Decision points → Move a cell to a cluster) and suggest inviting them there. Inbox and a hive never move: move their documents instead. Never delete a cell or empty one so it can be deleted; that is the human's, in the UI.

## Across other skills

When any other skill or workflow produces a **durable** decision, artifact, receipt or account fact, even if the human never said onecell:

1. Health check if not done this session; `recall` / `search` before inventing status or duplicating a note.
2. **Offer first** (Decision points → Capture). Write nothing without a yes.
3. On yes: a one-line fact → `remember` (entity slug; `cell` if it belongs on the hive). Anything longer → an Inbox draft (Park a session).

## Park a session

Human paste:

> Save this session to onecell as a draft in my Capture cell (my Inbox if I have no Capture cell). Use prompt blocks for key turns, text blocks with html links for URLs, code blocks for logs or pasted artifacts, and one remember for the decision. Do not publish or put it on the hive unless I say so. Reply with the document UUID link.

Recipe:

1. Destination: **Capture**, the private cell for your own drafts (`list_cells`: one you own with slug `capture`); Inbox if none. A named cell only if the human names it.
2. `create_document` (dry run, then real), title `Session — {client} — {date}`, tags `kind:{kind}` and `state:draft` (see Writes).
3. Blocks: a short `heading` summary, `prompt` turns (trim long ones), `text` with html links for URLs, `code` for logs and pastes, `text` for what was decided.
4. **Link what the conversation referred to.** People connect ideas in passing ("that's what we said about pricing"); write each callback as a link to that document. Links are how onecell learns what is load-bearing, and a session saved without them reads as unconnected.
5. Draft unless the human says publish. One `remember` for the durable decision, not the transcript. Reply with `{origin}/cells/{cellSlug}/{documentId}`.

## Hooks

If the human turned hooks on (Settings → Agents):

- **onecell memory that may be relevant** lines came from your prompt: use and cite them; don't search the same thing again.
- **onecell briefing** opens a session or follows `/clear`: unread mentions, active cluster, open decisions, recent Capture drafts. Under **Unread mentions** a line reads `- {who} (via agent) in {cell} · {document}: "…"`; tell the human, and `list_mentions` has the links. The briefing marks nothing read.
- **this turn looks like it settled something** is a suggestion: if worth keeping, save one short Capture draft (Inbox if none) and at most one `remember`, then stop. Never publish or share from a nudge.
- Never call `hook_event` yourself.

## Linking documents for humans

Link a note as `{origin}/cells/{cellSlug}/{documentId}`: the second segment is the document **UUID**, not its slug (a slug there 404s). Example: `https://onecell.io/cells/onecell-go-live/03ca4e14-fc18-4bdf-9d06-8529d538189e`. Ids come from `get_document`, `list_documents` or search hits. Use a readable label. The same form inside a document's text is a link onecell records.

## Writes

Every write defaults to `dry_run: true`: call once, read `{applied, reason}`, then again with `dry_run: false`. `create_document` is always a draft; publish with `set_status`.

- **`draft_only_key`**: your credential is drafts only. It can read, create and edit drafts and `remember`, but not publish, share, delete, invite, edit a published document, move one, or accept or reject a decision. Say so and ask the human; don't retry or look for a way around it.
- **A few blocks:** `update_document` `block_ops`: `insert` (`after` / `before` a block id, or `at` `start` / `end`), `replace`, `delete`, `move`, by id, in order, all or nothing. Send only what changes; ids come from `outline` or `section`. A replaced block keeps its id.
- **A rewrite:** `blocks` replaces the whole array. `get_document` the whole document first and send every block. Never both.
- Pass `expected_version`. Removing half the blocks is refused (`mass_removal`) unless acknowledged. Writes answer with what changed and the new version; `verbose: true` returns the document.
- **Link, don't just mention.** When a document builds on, answers or replaces another, link it in the text. A superseded document gets a link to its replacement as well as `state:superseded`.
- **Tags** (lowercase, `key:value`, 20 max) are recommended conventions, never required:
  - `kind:` how it was formed: `question`, `thought`, `idea`, `vision`, `spec`, `ticket`, `decision`, `reference`. Suggest one at capture; titles often say it (Spec:, Ticket:).
  - `state:` how decided: `draft` → `proposed` → `accepted` → `superseded`.
  - `work:` ticket progress: `todo`, `doing`, `done`.
  - Change them with `tags_add` / `tags_remove` (no `blocks` needed); find them with `list_documents` `tags` (all must match; `work:*` matches a prefix).
- Title and summary length warnings are advice and never block: aim for a title under 65 characters and a summary under 200, but don't retry just to clear one.
- **Files:** for a file on disk, `create_upload` and PUT it to the returned `upload_url` (single use, 10 minutes); the bytes never pass through the conversation. `upload_asset` (base64) costs about a token per 3 characters: tiny files only. 8 MB per file, 1 GB of your uploads in all; the bytes decide the type. Pass `document_id` (create the document first) so the file stays visible to its readers. Put the returned `block` in the document.
- `delete_document` trashes (out of search at once); `restore_document` brings it back; `list_documents` `trash: true` lists the bin, emptied after 30 days.
- A document is public at `/p/<slug>` only when published and its `visibility` is `public`. Ask first; drafts-only keys cannot change it. Public published documents tagged `help:recipe` in onecell's recipes cell appear on onecell.io/help.
- Move with `update_document` `cell`, following Move work; nested children come along, and granted cells cannot receive a move.

## Blocks

Don't smuggle a diagram into a text or code block. Ids are generated if omitted.

| Need | Block |
|---|---|
| Prose | `{type: text, html}` |
| Title | `{type: heading, level: 1-4, text}` |
| Diagram | `{type: mermaid, source, caption?}` |
| Sketch | `{type: drawing, scene, caption}` — Excalidraw elements (rectangle, ellipse, diamond, arrow, line, text); caption required to publish. Reading one, use the caption and skip the scene JSON |
| Picture | `{type: image, assetId, alt, caption?}` — `create_upload` (kind `image`) for the `assetId`; alt required to publish |
| Transclusion | `{type: embed, documentId}` — unreadable targets resolve null; on public pages only a published public target in the same workspace expands |
| Agent turn | `{type: prompt, role: user / assistant / system, body, model?}` |
| Link card | `{type: bookmark, url, title, note?}` — http(s) URL |
| Attachment | `{type: file, assetId, filename, note?}` — `create_upload` (kind `file`): PDF, text, Markdown, CSV, JSON, zip, Office |
| Code | `{type: code, lang, code}` |
| Aside | `{type: callout, variant: info / warning / danger / success / quote, html}` |
| Grid | `{type: table, header, rows, align?}` — `header: true` makes the first row the header; rows the same length |
| How-to | `{type: steps, steps: [{name, body}]}` |
| Break | `{type: divider}` |
| To-do | `{type: checklist, items: [{text, checked}]}` — plain text items |
| Chart | `{type: chart, kind: bar / line / pie, columns, rows, caption, title?, xLabel?, yLabel?, unit?, stacked?}` — category column then ≤8 series; caption required to publish; pie ≤6 slices |
| Video | `{type: video, provider: youtube / vimeo / loom, videoId, url, title, hash?, start?, caption?}` — loads only when a reader clicks |
| Formula | `{type: math, tex, display, caption?}` — KaTeX; must parse to publish |
| Collapsible | `{type: toggle, summary, html, open}` |
| Sequence of events | `{type: timeline, entries: [{when, title, body?, tone?: good / bad / neutral}], caption?}` — 1–100 in the order written; incidents, history, changelogs (how-to is steps) |
| Headline numbers | `{type: stats, items: [{label, value, unit?, delta?, tone?: good / bad / neutral, note?}], caption?}` — 1–6 tiles; value is display text |
| Interactive HTML | `{type: sandbox, title, html, description, height?}` — inline HTML/CSS/JS only (no network; images as data: URLs), ≤256 KB, ≤3 per document; description required to publish. Enabled per cluster: on `not_rolled_out` tell the person the `hint`. Never sandbox untrusted HTML |
| Change | `{type: diff, lang, before, after, filename?, caption?}` — both sides whole; the diff is drawn for you |
| Decision | `{type: decision, title, status: proposed / accepted / rejected / superseded, date?: YYYY-MM-DD, context, decision, consequences?}` — plain text, one per decision. Never write `decidedBy` / `decidedAt` |
| Cite memory | `{type: fact, factId}` — renders the live belief; never copy fact text into prose |

## Decisions

Open questions live as `decision` blocks with status `proposed`. When the human asks what is open, or a session reaches a choice already written down:

1. `list_decisions` `all_clusters: true` (so another cluster's are not missed), then ask one question per decision, the proposal first. Never decide for them.
2. On an answer: read the block (`section` or `blocks`), then `update_document` `block_ops` `replace` it with the new `status` (and `decision` / `consequences` if the answer differs), with `expected_version`. Dry run first.
3. The server records the decider from your key. Report: title → new status, and the link.

## Memory

`remember`: one sentence, an `entity` slug, `cell` for hive facts; it stores at once. `recall` before inventing a plan. A new belief replacing an old one → `remember` with `supersedes` (Decision points → Contradicting fact); `forget` only when something stopped being true with no successor. History remains either way.

## Memory pointer

A pasted pointer means: reload that belief live. Never trust inlined fact text.

1. Parse `cellId` (a cell UUID; `cell` accepts it), `memoryId`, `validFrom`.
2. `get_fact({ id: memoryId })`; on `not_found`, retry with `include_expired: true`.
3. If the returned `validFrom` differs from the pointer's, warn and prefer the live row. If it has `supersededBy`, follow it to the live fact.

```
# onecell memory pointer v1
Reload this memory. Do not trust inlined fact text — fetch live.

cellId: <uuid>
memoryId: <id>
validFrom: <ISO>

onecell://memory?v=1&cell=<uuid>&id=<n>&vf=<urlencoded ISO>
```

## Cell pointer

A pasted cell pointer means: work from that cell's live state, not a pasted dump. Resolve `cellId` / `cellSlug` (`cell` accepts either), then scope `search`, `list_documents` and `recall` to it. If the pointer's `vu` (newest update) is older than the live cell's, say it has changed. Never dump every document.

```
# onecell cell pointer v1
Reload this cell. Do not trust inlined dumps — fetch live via MCP.

cellId: <uuid>
cellSlug: <slug>
updatedAt: <ISO>

onecell://cell?v=1&cell=<uuid>&slug=<slug>&vu=<urlencoded ISO>
```

## Mentions

Bring a teammate in (a dependency on their work, a review, a decision for them) by @mentioning them. They are told in onecell and by their agent.

1. `list_members` with `cell`: who you can mention there, with `can_open` — `drafts` (told now), `published` (told once published), `none` (not told). Mentions in Inbox tell no one.
2. In rich text (text, callout, toggle, steps or prompt body): `<span data-mention="{workspaceId}">@{Name}</span>`. In a decision's `context`, `decision` or `consequences`: `@[{Name}](ws:{workspaceId})`. Nowhere else: elsewhere publishing refuses it (`mention.plain_text_field`).
3. Dry run: `mentions` shows who is told (`notify`), who later (`not_yet_visible`) and who not (`skipped`). Ask first (Decision points → Mention). Re-saving never tells anyone twice.

Your own: `list_mentions`, unread first. Pass `mark_read` (ids or `"all"`) only once the human has seen them.

## Team

- Share a cell: `list_members`, then `share_cell` (owner only; viewer by default; check `mailed`). Or open it to the whole cluster with `share_cell` `cluster` (`none` / `viewer` / `editor`), which includes future members: ask first. `list_cell_grants` shows both. Inbox cannot be shared.
- `invite_member`: they sign in with that email; `send_email: false` returns a join link. `resend_invite` and `list_invites` for pending ones.
- `share_document` mints a read link: a credential, shown once. Dry run, ask the human, then mint. `revoke_share` and `revoke_cell_grant` take access back.

## Isolation

A key or OAuth token is one workspace. If `search` or `get_document` returns nothing, you have no access: stop, and don't retry as someone else.
