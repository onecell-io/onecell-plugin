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

A workspace is one person. Inbox is private. The hive is a cell teammates granted you. You see own cells plus grants — never anyone else's Inbox.

Connect at `{origin}/api/mcp` (OAuth) or Bearer `ic_…`. First-time install: fetch `{origin}/agent-setup/prompt.md` and run this client's section (Codex: `codex mcp add` + `codex mcp login` — see `{origin}/agent-setup/codex`; Cowork: Claude.ai Connectors custom URL; Grok Bot: add MCP URL in chat, not Cursor mcp.json). Fetch this skill from `{origin}/skills/onecell.md`.

## Keep this skill fresh

Saved copies drift. Before meaningful hive work in a session (search, write, remember, or park):

1. Re-fetch `{origin}/skills/onecell.md` (and `{origin}/skills/onecell-bridge.md` when this client keeps companion skills).
2. Overwrite `skills/onecell/SKILL.md` (and `skills/onecell-bridge/SKILL.md` if present).
3. Do this **once per agent session** after MCP is connected — do not trust a days-old local copy.
4. If the live skill names tools you do not have, stop and re-run agent-setup; skill file alone is not a working install.

## Health check

Skill on disk ≠ done. After connect, and again when tools seem wrong:

1. Confirm MCP tools include at least: `list_cells`, `search`, `recall`, `remember`, `get_fact`, `create_document`, `get_document`.
2. Call `list_cells` — expect Inbox plus any granted cells (hive when shared).
2b. Call `get_active_cluster` (and `list_clusters` if you may belong to more than one).
3. Call `recall` (empty query lists recent facts) **or** `search` with a short real query.
3b. A tool this skill names is missing (say `move_cell`)? Your client cached an older tool list — onecell shipped since you connected. Ask the human to reconnect the onecell MCP (Claude Code: `/mcp` → reconnect onecell) rather than working around it.
4. Only then treat setup as healthy. Cite cell · heading · passage on search hits; never invent a cite.


## Clusters

One login may belong to several clusters. Session and API keys still bind to one workspace; org-scoped tools honor the **active** cluster preference.

- Before invite or Members work: `list_clusters` / `get_active_cluster`. Switch with `set_active_cluster` (dry_run first).
- Inbox = one private cell per login, shown in every cluster. Every other cell (the hive included) belongs to one cluster.
- `list_cells`, `search`, `recall` and `list_documents` cover the **active** cluster plus Inbox. Naming a cell by slug or id works in any cluster.
- The active cluster is **one preference shared with the human's UI**. Don't `set_active_cluster` just to look around — `list_cells` with `all_clusters: true` sees every cluster without moving their sidebar. To move work between clusters, see Move work.
- Work in another cluster by naming cells, not by switching: every tool that takes `cell` (`search`, `recall`, `list_documents`, `create_document`, `remember`, `update_document`) accepts one from any cluster. Switch only when the human asks, or for Members / invite work there (Decision points → Switch cluster).
- New cells land in the active cluster. Switching changes what you see, never merges rosters or writes across clusters silently.
- `create_cluster` names a new cluster while already membered — and makes it active, which switches the human's sidebar too (Decision points → Create a cluster). `join_cluster` accepts a pending invite by id for this email.
- Invite / `list_invites` / `list_members` / `share_cell` honor the active cluster only. Owner of the active cluster invites; INVITE_ADMINS is break-glass only.

## First moves

1. `list_cells` — note `owned`, slug, `embedding_policy`. `none` is not searchable; `local_only` needs a local embedder.
1b. `create_cell` opens a cell in **your** workspace. Inbox is reserved. It is not shared until `share_cell`. dry_run first. Humans can rename a cell or archive it (Inbox cannot be archived).
2. `search` the question (optional `cell`). Hits are grouped by document (5 by default), each with up to three short passages and heading trails. Judge by score; a query always returns candidates.
3. `get_document` only for the hit you will use. On a long page read less: `outline` first, then `section` (a heading id) or `blocks` (ids). Do not list-and-dump.

Cite as: cell · heading path · passage. Never paste a whole document into the reply.

## Decision points

Some choices belong to the human. Ask in one line and name the default. Skip a question the human already answered (e.g. they pasted the Park prompt). If this client cannot ask, take the default — it is always the least exposed choice. `dry_run` checks the call; this table checks the person — do both.

| Moment | Ask | Default |
|---|---|---|
| Capture — another skill produced durable work | "Save {one-line summary} to your Inbox?" | Write nothing. Mention it once in the reply. |
| Shape — `recall` / `search` found a close note or fact | "Update {title}, or start a new note?" One sentence → `remember`; longer → document. | New Inbox draft that links the near match. Never overwrite. |
| Destination | "Inbox (private) or {hive / named cell}?" Offer only cells you can write to. | Inbox |
| New cell | "Create cell {name}, or use {existing}?" | Existing cell, else Inbox |
| Publish | "Publish, or keep as draft?" Run `validate_document` `strict: true` first; say what it would fix. | Draft |
| Contradicting fact | "Replace '{old}' with '{new}'?" (`forget` + `remember`) | Keep the old fact. Report the conflict. |
| Share a cell | "Share {cell} with {who} as viewer or editor?" | Viewer |
| Public link | "Create a public link? Anyone with it can read {title}." | No link |
| Invite | "Email the invite, or give you a join link to paste?" | Email |
| Trash | "Trash {title}? Restorable for 30 days." | Don't |
| Move | "Move {title} (+{n} nested) from {cell} to {cell} in {cluster}?" — see Move work. | Don't |
| Create a cluster | "Create cluster {name}? It becomes your active cluster, so your onecell sidebar switches to it." Dry run first — it runs the real checks. | Don't |
| Switch cluster | "Switch to {cluster}? Your onecell sidebar switches too." | Don't. Name cells with `cell`, or find them with `list_cells` `all_clusters`. |
| Move a cell to a cluster | "Move {cell} ({n} docs) to {cluster}? {people} aren't in {cluster}, so it leaves their sidebar and search." | Don't |
| Move out of a shared cell | "{from} is shared — the people there lose {title}. Move anyway?" | Don't |
| Mention | "Mention {name}? They're told in onecell and by their agent." | Don't — mention only someone the human named, or asked you to bring in |

## Move work

Moving is the human's call: where work lives decides who sees it. Guide them to a destination; never pick one silently.

1. **Which document.** If the human named it exactly, use it. Otherwise `search` and offer up to three: "Move {title} ({cell}), or one of these?" Several documents → list them and confirm the set once.
2. **Where to.** `list_cells` with `all_clusters: true`. Offer two or three likely cells, grouped by cluster, active cluster first — judge by name and by where related notes live (`search` the topic). Always include Inbox: it is private and shows in every cluster. Only cells with `owned: true` can receive a move. If nothing fits, ask whether to create one (Decision points → New cell) — don't invent a cell.
3. **Dry run.** `update_document` with `id`, `cell`, `dry_run: true`. Read `move`: `children` come along, `to.cluster` is where it lands, `leaves_shared` means people who can see the current cell lose it.
4. **Confirm in one line**: "Move {title} (+{children} nested) from {from} to {to} in {cluster}?" If `leaves_shared`, say who loses it and default to not moving. No yes → do nothing.
5. **Move**: the same call with `dry_run: false`. Reply with `{origin}/cells/{to.slug}/{documentId}`. If it landed outside the active cluster, say so: "It's in {cluster} — switch there in System to see it in your sidebar." Don't switch for them unless asked.

**A whole cell to another cluster** — when the work that belongs elsewhere is a cell, not a few documents (a project spinning out into its own cluster): `move_cell` keeps its documents, memory, shares and links together. Do not recreate the cell and move documents one by one.

1. `list_clusters`; `list_cells` `all_clusters: true` to propose which cells belong. Confirm the set once.
2. `move_cell` with `cell`, `cluster`, `dry_run: true` for each. `losing_access` lists people the cell is shared with who aren't in the destination — it drops out of their sidebar and search.
3. Confirm per cell (Decision points → Move a cell to a cluster), naming those people. Suggest inviting them to the destination cluster (switch there, then `invite_member`) — ask before switching.
4. `move_cell` with `dry_run: false`. Inbox and a cluster's hive never move; move their documents instead (above).

Never delete a cell, and never move documents out of a cell to empty it — cell deletion is the human's, in the UI.

## Across other skills

When Notion, shopping, email, research, coding, or any other loaded skill produces a **durable** decision, artifact, receipt, or account fact — even if the human never said "onecell":

1. Run the health check if you have not this session (re-fetch skill + `list_cells` + `recall` or `search`).
2. `recall` / `search` the hive (and Inbox) before inventing status or duplicating a note.
3. **Offer first** (Decision points → Capture). Write nothing without a yes.
4. On yes: one-line durable facts → `remember` (entity slug; `cell` when it belongs on the hive). Longer artifacts, logs, or session narrative → draft in **Inbox** with `create_document` (see Park a session). Shape, destination, and publish follow Decision points.
5. Stay on nouns: cluster · cell · hive · Inbox. Do not add a chat UI inside onecell.

## Park a session

Human paste (Grok / Codex / Claude / Cowork):

> Save this session to onecell as a draft in my Capture cell (my Inbox if I have no Capture cell). Use prompt blocks for key turns, text blocks with html links for URLs, code blocks for logs or pasted artifacts, and one remember for the decision. Do not publish or put it on the hive unless I say so. Reply with the document UUID link.

Agent recipe:

1. Destination default: **Capture**, the private cell your own drafts go to (`list_cells`: a cell you own with slug `capture`); **Inbox** if there is none. Use a named cell only if the human names it.
2. `create_document` with `dry_run` true, then false. Title like `Session — {client} — {date}`.
3. Blocks: short `heading` summary → `prompt` turns (truncate long bodies) → `text` (html links for URLs) → `code` for logs/pastes → more `text` for decisions. Do **not** dump raw chat logs onto the hive as truth.
4. Stay **draft** unless the human asks to publish. Hive, shared cell, or publish → Decision points.
5. One `remember` for the durable decision (not the transcript).
6. Reply with `{origin}/cells/{cellSlug}/{documentId}` (UUID, not slug).

## Hooks

If the human turned hooks on (Settings → Agents), onecell can speak without being asked:

- Lines headed **onecell memory that may be relevant** were added by a hook from your prompt. Use and cite them (cell · heading); do not search for the same thing again.
- **onecell briefing** lines open a session or follow `/clear`: unread mentions, active cluster, open decisions, recent Capture drafts. A line under **Unread mentions** reads `- {who} (via agent) in {cell} · {document}: "…"` — tell the human who needs them; `list_mentions` has the links. The briefing never marks anything read.
- A stop that says **this turn looks like it settled something** is a suggestion. If it is worth keeping, save one short draft to the **Capture** cell (fall back to Inbox) and at most one `remember`, then stop. If not, or already saved, just stop. Never publish or share from a nudge.
- Never call `hook_event` yourself; it is for the client's hooks.

## Linking documents for humans

UI routes are `/cells/{cellSlug}/{documentId}` — the second segment is the document **UUID**, not its slug. A slug in that slot 404s once signed in.

When you link a note to a human (chat, email, PR), always use:

`{origin}/cells/{cellSlug}/{documentId}`

Example: `https://onecell.io/cells/onecell-go-live/03ca4e14-fc18-4bdf-9d06-8529d538189e`

Get `id` from `get_document` / `list_documents` / search hit metadata. Prefer a readable markdown label on the link. Prefer `/cells/` over the deferred `/silos/` alias. Do not invent query params.

Cite agent answers as: cell · heading path · passage. The UUID link is for opening the note in the UI — not a substitute for that cite.

## Writes

Mutating tools default `dry_run` true. Call once, read `{applied, reason}`, then again with `dry_run: false`. Human-facing choices (publish, trash, move) → Decision points.

- `create_document` is always a draft. Publish with `set_status`.
- **`draft_only_key`** means your credential is drafts only: it can read, create and edit drafts, and `remember`, but not publish, share, delete, invite, edit a published document, move a document, or accept or reject a decision. Say so and ask the human to do it (or to use a full key). Do not retry, and do not look for another way around it.
- To change a few blocks, use `update_document` `block_ops`: `insert` (`after` / `before` a block id, or `at` `start` / `end`), `replace`, `delete` or `move` a block by its id. Applied in order, all or nothing; send only the blocks you change. Ids come from `get_document` (`outline` or `section` is enough). A replaced block keeps its id.
- `blocks` **replaces the entire array**: for a rewrite or a big restructure only. Then `get_document` the whole document first, even if you found the part with `outline` / `section`, and send every block. Never both `blocks` and `block_ops`.
- Pass `expected_version` either way. Removing half or more of the blocks is refused (`mass_removal`) unless acknowledged.
- Writes answer with what changed (`changes.fields`, `changes.blockIds`) and the new `document.version`, not the document. Pass `verbose: true` only if you need the whole thing back.
- Tags classify documents for a work queue: `create_document` `tags` (lowercase, `key:value` allowed, e.g. `ticket`, `state:todo`; 20 max). Move state with `update_document` `tags_add` / `tags_remove` and `expected_version` — no `blocks` needed. Find them with `list_documents` `tags` (all must match; `state:*` matches a prefix); every row carries its tags.
- Ids on blocks are generated if omitted.
- Title and summary length warnings (`title.short`, `title.long`, `summary.short`, `summary.long`) are advice and never block a publish. Aim for a title under 65 characters and a one- or two-sentence summary under 200, but do not rewrite or retry a write just to clear one.
- Pictures and attachments: for a file on disk, `create_upload` (with `dry_run: false`) and PUT the file to the returned `upload_url` with the given `curl` command — the bytes never pass through the conversation. The link is single-use and lasts 10 minutes. `upload_asset` with `content_base64` costs about a token per 3 characters, so keep it for tiny files or clients with no shell. Either way 8 MB max, the bytes decide the type, and you put the returned `block` in the document. Pass `document_id` for the document it is going into — create the document first if needed — so the file belongs to that document's owner and keeps showing for everyone who can read it, even in a shared cell you later lose.
- `delete_document` moves to trash (out of search immediately). `restore_document` brings it back. `list_documents` with `trash: true` lists the bin. After 30 days the reconciler hard-deletes.
- Public pages: a document is readable at `/p/<slug>` only when it is published *and* its visibility is `public` (`update_document` `visibility`). Ask the human before making anything public; a draft-only key cannot change visibility. Published, public documents tagged `help:recipe` in onecell's own recipes cell appear on onecell.io/help.
- Move between cells you own, in any cluster, with `update_document` `cell` — follow Move work. Nested children come along. Granted cells cannot be a destination. In the UI, "Move to…" does the same; drop a row onto another in the same cell to nest; drop it on the cell in the sidebar to un-nest.
- Deleting a **cell** is UI-only and only for an empty one. Never try to empty a cell so it can be deleted.

`validate_document` before a big write. `strict: true` is what publishing uses.

## Blocks

Do not smuggle a diagram into a text/code block.

| Need | Block |
|---|---|
| Prose | `{type: text, html}` |
| Title | `{type: heading, level: 1-4, text}` |
| Diagram | `{type: mermaid, source, caption?}` |
| Sketch | `{type: drawing, scene, caption}` — caption required to publish. Read caption; skip scene JSON. Write Excalidraw elements (rectangle, ellipse, diamond, arrow, line, text); share pages draw them until the editor makes its own snapshot. |
| Picture | `{type: image, assetId, alt, caption?}` — `create_upload` (kind `image`) first for the `assetId`; alt required to publish; caption optional |
| Transclusion | `{type: embed, documentId}` — unreadable targets resolve null; on public/share pages only a published *public* target in the same workspace expands |
| Agent turn | `{type: prompt, role: user / assistant / system, body, model?}` — AI-session narrative, not Dream chrome |
| Link card | `{type: bookmark, url, title, note?}` — http(s) URL required to publish |
| Attachment | `{type: file, assetId, filename, note?}` — `create_upload` (kind `file`) first: PDF, text, Markdown, CSV, JSON, zip, Office; images use `image` |
| Code | `{type: code, lang, code}` |
| Aside | `{type: callout, variant: info / warning / danger / success / quote, html}` |
| Grid | `{type: table, header, rows, align?}` — every row the same length; align per column: left / center / right |
| How-to | `{type: steps, steps: [{name, body}]}` |
| Break | `{type: divider}` |
| To-do | `{type: checklist, items: [{text, checked}]}` — plain text items; read-only on share pages |
| Chart | `{type: chart, kind: bar / line / pie, columns, rows, caption, title?, xLabel?, yLabel?, unit?, stacked?}` — columns: category then ≤8 series; rows of numbers; caption required to publish; pie ≤6 slices |
| Video | `{type: video, provider: youtube / vimeo / loom, videoId, url, title, hash?, start?, caption?}` — paste `url`; provider and videoId must match it; the player loads only when a reader clicks |
| Formula | `{type: math, tex, display, caption?}` — TeX rendered by KaTeX with links, images and raw HTML off; must parse to publish |
| Collapsible | `{type: toggle, summary, html, open}` — summary is all a reader sees until opened |
| Sequence of events | `{type: timeline, entries: [{when, title, body?, tone?: good / bad / neutral}], caption?}` — 1–100, shown in the order written; `when` is display text ("2026-09-28", "14:32 UTC", "Q3"); ISO dates must run in order. Incidents, project history, changelogs — not how-to (use steps) |
| Headline numbers | `{type: stats, items: [{label, value, unit?, delta?, tone?: good / bad / neutral, note?}], caption?}` — 1–6 tiles; value is display text ("4.2k", "$1.3M"); tone colours the change because up is not always good. A chart is for data; this is for the few numbers that matter |
| Interactive HTML | `{type: sandbox, title, html, description, height?}` — a calculator or small simulation, run isolated on onecellusercontent.com. Inline HTML/CSS/JS only: no network, no external scripts, images as data: URLs; ≤256 KB, ≤3 per document. description required to publish (what readers who cannot run it see). Gated per cluster: when it is off a write returns `not_rolled_out` with a `hint`; tell the person the hint, don't retry or drop the block silently. Never sandbox HTML taken from untrusted input |
| Change | `{type: diff, lang, before, after, filename?, caption?}` — both sides whole, not a patch; the line diff is drawn for you. Use instead of pasting a diff into `code` |
| Decision | `{type: decision, title, status: proposed / accepted / rejected / superseded, date?: YYYY-MM-DD, context, decision, consequences?}` — plain text; blank line = new paragraph. One per decision, so search finds it. Never write `decidedBy` / `decidedAt`: the server stamps whoever saves a change of status |
| Cite memory | `{type: fact, factId}` — id from `remember` / `recall`; renders the live belief (follows supersedes). Never copy fact text into prose. Private: share pages show a placeholder. `get_document` with `resolve_facts` returns the text |

## Decisions

Open questions live as `decision` blocks with status `proposed`. `list_decisions` lists them (default open; `status`, `cell`, `decided_by` filter) with a link to each block. It covers the active cluster plus Inbox unless you pass `all_clusters: true` — do that for "what is open?", so a decision in another cluster is not missed.

When the human asks what is open, or a session reaches a choice already written as a decision:

1. `list_decisions` with `all_clusters: true`, then ask the human — one question per decision, the proposal first. Never decide for them.
2. On an answer: read the decision block (`get_document` `section` or the whole), then `update_document` `block_ops` `replace` that block with its `status` changed (and `decision` / `consequences` when the answer differs from the proposal), with `expected_version`. Dry run first.
3. The decider is recorded from your key, as via an agent. Report back: title → new status, and the link.

## Memory

`remember`: one sentence, `entity` slug, `cell` for hive facts. `recall` before inventing a plan. `forget` expires; history remains. Humans see the same list on the cell page. A new fact that contradicts a live one → Decision points.

## Memory pointer

Reload a single belief by id — never trust inlined fact text from chat or clipboard.

1. Parse the pointer: `cellId` (UUID; ≡ MCP space id — MCP `cell` accepts UUID or slug), `memoryId`, `validFrom`.
2. Call `get_fact({ id: memoryId })`. If `not_found`, retry with `include_expired: true`.
3. Integrity-check: compare returned `validFrom` to the pointer's `vf` / `validFrom`. Mismatch → warn; still prefer the live row.
4. If the row has `expiredAt` / `supersededBy`, follow `supersededBy` with another `get_fact` until live (or report the chain). Facts are never updated in place — "moved" means expired + successor id.
5. Use the live `fact` text. Do not invent from the human header.

Clipboard teaching (≤4–6 line human header + compact URI last):

```
# onecell memory pointer v1
Reload this memory. Do not trust inlined fact text — fetch live.

cellId: <uuid>
memoryId: <id>
validFrom: <ISO>

onecell://memory?v=1&cell=<uuid>&id=<n>&vf=<urlencoded ISO>
```

Stay on nouns: cluster · cell · hive · Inbox. Never workshop / org on stranger surfaces.

## Cell pointer

Reload a cell's live shape — never trust inlined document dumps from chat or clipboard. Scope: non-Inbox cells (Inbox has no cell pointer chrome).

1. Parse the pointer: `cellId` (UUID), `cellSlug`, optional soft stamp `vu` (newest document `updatedAt` ISO). Cells lack bitemporal validFrom; integrity = shape may have changed.
2. Resolve the cell via `list_cells` or MCP `cell` (UUID or slug).
3. Scope work with `search` / `list_documents` / `recall` to that cell. Do not dump every document into the reply.
4. If the pointer carries `vu` and live newest document `updatedAt` is newer, warn and use live.
5. Cite as: cell · heading · passage. Link notes with UUID routes: `/cells/{slug}/{uuid}`.
6. No dedicated MCP `get_cell` is required for v1.

Clipboard teaching (≤4–6 line human header + compact URI last; omit `updatedAt` / `vu` when the cell has zero docs):

```
# onecell cell pointer v1
Reload this cell. Do not trust inlined dumps — fetch live via MCP.

cellId: <uuid>
cellSlug: <slug>
updatedAt: <ISO>

onecell://cell?v=1&cell=<uuid>&slug=<slug>&vu=<urlencoded ISO>
```

Stay on nouns: cluster · cell · hive · Inbox.

## Mentions

Bring a teammate in by @mentioning them — a dependency you found on their work, a review, a decision they should weigh in on. They are told in onecell and by their agent; there is no email.

1. Who: `list_members` with `cell` — the people you can mention there, with `can_open`: `drafts` (told now), `published` (told once the document is published), `none` (not told). Mentions in Inbox tell no one.
2. Write the mention where it belongs:
   - In a rich-text field — text, callout, toggle, steps body or prompt body — as `<span data-mention="{workspaceId}">@{Name}</span>`.
   - In a decision's `context`, `decision` or `consequences` (plain text) as the token `@[{Name}](ws:{workspaceId})` — e.g. who to review it, or who owns a dependency.
   - Nowhere else: not a decision's title, checklist items, headings or tables. There the markup shows as typed, id and all, and publishing refuses it (`mention.plain_text_field`).
3. Dry run first: the result's `mentions` says who will be told (`notify`), who later (`not_yet_visible`), and who not and why (`skipped`). The server sets the name; a mention of someone outside the cluster is removed. Ask first (Decision points → Mention).
4. Re-saving never tells anyone twice. Mentioning them again in a new block does.

Your own: `list_mentions` (unread first; who, cell, document, passage, link). Pass `mark_read` (ids or `"all"`) only once the human has seen them.

## Team

- `list_members` then `share_cell` (owner only; dry run first). Default role viewer. Check `mailed`. Inbox cannot be shared.
- A cell can also be open to its whole cluster: `share_cell` with `cluster` (`none`, `viewer`, `editor`; owner only; dry run first). Everyone in the cluster gets that level, including people who join later, so ask the human first. `list_cells` / `list_cell_grants` show `clusterAccess`. A new member gets the hive plus every cell open to the cluster; nothing else.
- Share, invite, or public link → Decision points first.
- `invite_member`: they sign in with that email. `send_email: false` returns a join `url` to paste. `resend_invite` / `list_invites` for pending links.
- Outward link: `share_document` — dry_run first, then ask the human; the token is shown **once**. Refuses Inbox (`inbox_unshareable`). `revoke_share`, `revoke_cell_grant` and `forget` also dry-run first.

## Isolation

A key or OAuth token is one workspace. If `search` / `get_document` returns nothing, you are not granted it — stop. Do not retry as a different user.
