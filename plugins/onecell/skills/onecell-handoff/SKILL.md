---
name: onecell-handoff
description: >
  Pass work in progress to a teammate, or pick up work a teammate passed to you, through
  onecell: the code pushed to a recorded commit, a handoff page they can open with what's
  done, decided, half-done and the first step, the ticket tied in, and a pickup that checks
  out the same commit, runs the checks and takes the ticket over. Trigger when someone is
  stopping and someone else will carry on ("hand this to Sam", "Priya's picking this up"),
  when someone wants to pick up a teammate's work ("pick up Sam's handoff", "what did Sam
  leave me?"), or when a session briefing or list_mentions shows a handoff addressed to
  them. Use with the onecell MCP tools and the onecell skill.
---

# onecell-handoff

Companion to `https://onecell.io/skills/onecell.md`, whose write rules apply here: dry run first,
`expected_version`, block ops rather than a whole-page `blocks` replace, drafts unless the
person publishes. Re-fetch this file from `https://onecell.io/skills/onecell-handoff.md` once per
session, with the others. If the team keeps a Delivery conventions page (tagged
`kind:delivery-conventions`, see `https://onecell.io/skills/onecell-delivery.md`), read it first for
the backlog cell, repos and ticket codes; without one, ask which cell the work belongs in.

One person has the baton at a time. A handoff page says who had it, who has it next, and
exactly which code they're picking up. Nothing reaches the teammate, and nothing is
committed or pushed, without the sender's yes.

## Hand off

### 1. Make the code reachable

A teammate can't pick up code that exists only on this machine. In the repo:

- `git status --short` and `git log --oneline @{u}..HEAD` (or against the base branch if
  there's no upstream): is there uncommitted or unpushed work?
- On the default branch with changes: stop. Offer to move them to a new branch named
  after the ticket (`<code>-<slug>`) first; never commit to the default branch.
- Uncommitted or unpushed work: ask once, showing the files, then commit everything that
  belongs to this work as `WIP: handoff to <name>` (a commit body listing what's
  half-done) and `git push -u origin <branch>`. Leave out what doesn't belong (local
  config, scratch files) and say what you left out. Never commit a secret: if a changed
  file looks like one (`.env`, keys, tokens), leave it out and say so.
- If they won't push: say plainly that the teammate can't pick up the code, only the notes,
  and carry on with the page.

Record the **Where**: remote repo (`owner/name`), branch, the pushed commit (full and short),
the base branch and the commit it branched from (`git merge-base`), a compare link
(`https://github.com/<owner>/<repo>/compare/<base>...<branch>`, or the host's equivalent),
and the files changed against the base. Never a home-directory path.

### 2. Write the handoff page

In the cell the work belongs in (the ticket's cell, or the one the person names), never
Inbox or Capture: a teammate can't open those. `create_document` as a draft, titled
`Handoff: <topic> → <name>`, tags `kind:handoff`, `handoff:open`, `repo:<name>`, and the
ticket's `project:` if it has one. Blocks, in this order:

- **Where** (a text block): repo, branch, commit, base, the compare link, files changed.
- **Done**: what's finished, with its commits or pull requests.
- **Decided**: each decision, cited as a link to where it lives (a decision block, a spec,
  a ticket). Don't restate it.
- **Half-done**: each unfinished piece, with the exact file and function, and what's left.
- **Next**: one first step, then at most three after it.
- **How to run and check it** (a code block): install, run, test commands; the names of
  env vars it needs (never values); seed data or fixtures. Say which checks passed at
  handoff and which didn't.
- **Links**: the ticket, the pull request if there is one, the session save if there was
  one, and the previous handoff if this work was handed on before.

### 3. Tie in the task

On the ticket: a line linking the handoff page (under its Status heading, or a text block
at the end), and keep it `work:doing`. Ownership doesn't move yet; the teammate takes it on
pickup. No ticket: the page stands alone.

### 4. Reach them

- `list_members` with the cell: can they open a draft (`can_open: drafts`)? If they see
  published pages only, say so and ask before publishing. If they can't open it at all,
  say so and ask whether to share the cell.
- Ask before the mention, then add a last text block **Over to you**:
  `<span data-mention="{workspaceId}">@{Name}</span>` and the first step in one line.
  The dry run's `mentions` says whether they're told now.
- Reply with the link, who it's for, whether they can open it now, and the commit.

## Pick up

### 1. Find it

`list_mentions` (unread first) for handoff pages, and `list_documents` with
`tags: ['kind:handoff', 'handoff:open']` in the cells this repo's work lives in. Offer
each as "<from> · <topic> · <repo> @ <branch> · <age>". In Claude Code, a question with up
to four options; elsewhere a numbered list. Wait for the choice. Don't mark mentions read
until the person has seen them.

### 2. Read it

`get_document`, then say in a few lines: what was going on, what's done, what's half-done,
the first step, and anything in **Decided** that constrains the work.

### 3. Get the same code

- Check this is the right repo (the remote matches the **Where** line); if not, say which
  repo to open.
- `git status --short`: local changes? Stop and ask. Never stash, reset, overwrite or
  delete unasked.
- `git fetch origin`, then `git switch <branch>` (tracking `origin/<branch>`). If the
  branch already exists locally and has diverged, say so and ask.
- Compare with the recorded commit: equal, good; ahead (`git log --oneline <commit>..HEAD`),
  say what was added since the handoff; the commit missing from the remote, say the push
  didn't happen or was rewritten, and stop.

### 4. Check it runs

Run the **How to run and check it** commands. Report each as passed or failed, against what
the handoff said. Name each env var it needs that isn't set (the name only). Don't fix
anything yet.

### 5. Take it over

After the person says they're taking it:

- On the handoff page: insert a callout at the start, "Picked up by <name>, <date>, at
  <commit>"; `tags_remove` `handoff:open`, `tags_add` `handoff:picked-up`; and @mention
  the sender in it (ask first, as for any mention).
- On the ticket: move its `owner:` tag to the person picking up (`tags_remove` the old,
  `tags_add` the new), keep `work:doing`. If the onecell-delivery skill is in use, its
  own-ticket rule now applies to them.
- Say the first step, and wait.

## Handing on again

The receiver hands off with this same skill. The new page links the one before under
**Links**, so the chain reads in order. One person has the baton: mention others for
information, not as the next owner.

## Never

- Commit to the default branch, force-push, or rewrite someone's commits.
- Commit, push, publish, share or mention without the person's yes.
- Write a secret's value anywhere: env vars by name only.
- Stash, reset or overwrite local work on pickup.
- Move a ticket's owner before the receiver says they're taking it.
