---
name: onecell-delivery
description: >
  Keep a team's delivery work in onecell honest: move tickets as work starts, goes to
  review and merges; file new tickets with the right tags and code; plan, check and
  close sprints; prepare a release; and answer when something will ship, what is in a
  sprint, or what is blocking a date, from the roadmap, the tickets and GitHub. Trigger
  when someone starts, opens a pull request for, merges or files a ticket, plans or
  reviews a sprint, prepares a release or milestone, or asks about a timeline, a sprint
  or what is blocked. Use with the onecell MCP tools and the onecell skill.
---

# onecell-delivery

Companion to `https://onecell.io/skills/onecell.md`, whose write rules apply here: dry run first,
`expected_version`, block ops rather than a whole-page `blocks` replace, drafts unless
the person publishes. Re-fetch this file from `https://onecell.io/skills/onecell-delivery.md`
once per session, with the others.

People own dates, sprint scope and what ships. You propose; they decide. The one
thing you change without asking is the status of the person's own tickets as their
work moves.

## 1. Find the team's conventions

Everything team-specific is on a **Delivery conventions** page in the team's cell,
tagged `kind:delivery-conventions`. Before anything else:

1. `list_documents` with `tag: "kind:delivery-conventions"` in the cell the person works
   in (or the cluster's cells, if unsure). Read it, and parse its JSON code block.
2. None? Say so and offer to draft one from what you can see: the backlog cell, the
   `stream:`, `project:` and `work:` tags in use, the repos the person works in, and any
   roadmap page. Write it as a draft and ask them to check it. Do nothing else until it
   exists.

The JSON block:

```json
{
  "backlog": "<cluster/cell>",
  "ticket_tags": ["ticket", "kind:ticket"],
  "status": { "tag": "work", "values": ["todo", "doing", "review", "done"] },
  "streams": [{ "tag": "stream:api", "repo": "owner/repo", "branch": "main", "title_filter": "" }],
  "codes": [{ "prefix": "CO", "project": "project:checkout" }],
  "cadence": { "sprint_days": 14, "first_sprint": "YYYY-MM-DD", "planning": "Monday", "close": "Friday" },
  "roadmap": { "document": "<id>", "block": "<block id>" },
  "dashboard": "<id>",
  "milestones": [{ "name": "…", "date": "YYYY-MM-DD", "ticket": "<id>" }],
  "summary_channel": "#…"
}
```

- **Tickets** are the documents in `backlog` carrying any of `ticket_tags`. List each tag
  and merge by id; never count one twice.
- **Status** is the `work:` tag. A ticket with an old `state:` tag instead: read it as the
  nearest value (`in-progress` doing, `in-review` review, `parked` todo) and, when you touch
  that ticket anyway, replace it with the `work:` tag.
- **Sprint n** runs `sprint_days` days from `first_sprint + (n-1) × sprint_days`. Its tag is
  `sprint:<year of its start>-s<n>`, for example `sprint:2026-s2`.

## 2. Day to day: a developer's own tickets

Match the work to a ticket by its code in the branch or pull request title, or by the
ticket the person names. Then, without asking, and saying what you changed in one line:

| When | Change |
|---|---|
| Work starts on it | `work:doing`; suggest a branch named `<code>-<short-slug>` |
| A pull request opens | `work:review`; the code in the PR title; add the PR link to the ticket (a line under its Status heading, or a new text block at the end) |
| The pull request merges | `work:done`, only once GitHub says merged. Closed without merging: back to `work:doing` and ask |
| Review sends it back | stays `work:review`; nothing to do |

- Someone else's ticket (another person in `owner:` or the ticket's history): ask first.
- Never write a `state:` tag. Never mark a ticket done because the code looks finished.
- No ticket matches? Ask which one, or offer to file one (below). Don't guess.

**Filing a ticket.** In `backlog`, as a draft: a title that starts with its code, a
one-sentence summary, a Problem, a Fix and an Acceptance checklist. Tags: the first of
`ticket_tags`, `work:todo`, its `stream:` tags (one per repo it touches), `area:` tags if
the team uses them, and its `project:` if it has one.

**Its code:** the prefix mapped to its `project:` in `codes`, and one more than the
highest number already used with that prefix in the backlog's titles, zero-padded as the
others are (`CO-07`). A ticket in no project gets no code; say so.

## 3. Timeline questions

"When will X ship?", "What's in Sprint 2?", "Will the 2.0 launch make 1 December?", "What did
the API stream ship this week?"

- Answer from the roadmap block, the tickets and GitHub, and cite each claim: the
  ticket, the roadmap bar, the pull request.
- A date on the roadmap is a **plan**. Say "planned for", not "will ship on", unless a
  milestone in the conventions is a commitment someone made.
- A ticket with no sprint and no roadmap bar is **not scheduled**. Say that; never make
  up an estimate.
- For "will we make date D": list what the milestone depends on, each one's status,
  open pull requests and their review and checks, and what is late against its bar.
  Then say what has to happen by when, not a yes or no you can't back.
- Shipped means merged. Say when something merged but may not be live yet.

## 4. Sprint planning

At the start of a sprint, or when asked. Read the backlog, the roadmap and the open
pull requests, then propose, on a draft page "Sprint <n> plan: <team>":

1. **Carry-over:** last sprint's tickets that aren't done, with why (from their history
   and pull requests, not guessed).
2. **Must:** what a milestone in the next two sprints depends on; blockers and high
   severity.
3. **Then:** by severity, then dependency order, then the team's order (ticket code
   order within a project).
4. **Left out,** with the reason for each.

Size it against what the team finished in the last sprint or two, and say how you
sized it. Nothing changes until the person approves. Then:

- Tag the sprint's tickets `sprint:<year>-s<n>`; a carried-over ticket swaps last
  sprint's tag for this one's.
- Place them on the roadmap block: one bar per ticket in its lane, spanning the sprint,
  status from its `work:` tag, linked to `/cells/<cell>/<id>`. Replace the block's whole
  `data` with only those items added or moved. Never move another bar's dates without
  asking.

## 5. Mid-sprint check

Read only. For the current sprint:

- **On track:** done and in review against what's left and the days left.
- **At risk:** not started with less than half the sprint left; in review for more than
  3 days with no review; failing checks; anything a milestone depends on that is behind.
- **Blocked:** what, and on whom.
- **Unplanned:** work merged this sprint against tickets not in it.

Suggest moves (drop, swap, ask for review), each with its reason. Make none of them.

## 6. Sprint close

On a draft page "Sprint <n> review: <team>":

- **Shipped:** each ticket with its merged pull requests.
- **Slipped:** each ticket not done, why (from its history and pull requests; "no
  activity" is a reason), and where it goes next.
- **Numbers:** planned, done, carried, added mid-sprint; merges, and how many named a
  ticket code.
- **Notes for next time:** at most three, from what actually happened.

Then offer to plan the next sprint.

## 7. Release prep

For a milestone in the conventions, or one the person names:

- **Left:** every ticket it depends on that isn't done, with owner, status and its pull
  request's review and checks.
- **At risk:** anything that, at its pace, lands after the date.
- **Go/no-go:** a checklist on a draft page for the people who decide: each must-have
  ticket merged, checks green, anything the team said must be true before release (from
  the milestone's ticket). You fill in what you can verify; they tick the rest.

## Never

- Change a date, a lane or a sprint's scope without the person's yes.
- Mark done without a merged pull request.
- Change another person's ticket status without asking.
- Write a `state:` tag, or replace a page's whole `blocks`.
- Answer a timeline question with an estimate you can't cite.
