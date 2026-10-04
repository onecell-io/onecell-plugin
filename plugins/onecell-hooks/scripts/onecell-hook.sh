#!/bin/sh
# onecell hook for Claude Code (the onecell-hooks plugin) and Codex.
#
# Reads the hook's JSON on stdin, forwards the event to onecell's hook_event tool over
# HTTPS, and prints what onecell answers, already in the shape both clients read. onecell
# decides whether to say anything; usually it says nothing, and so does this script. Turn
# the behaviours on in https://onecell.io/settings/agents#hooks.
#
# It talks to onecell itself, with its own key, so it works however onecell's MCP server
# is set up in the client (plugin, `claude mcp add`, or not at all).
#
# Needs: curl (7.55 or later), jq, and a key (an ic_… key from https://onecell.io/settings/agents; Drafts only is
# enough): CLAUDE_PLUGIN_OPTION_API_KEY, which Claude Code sets from the plugin's stored
# setting, or ONECELL_API_KEY. Never blocks a session: any failure prints nothing, exits 0.

# Filled in when served from https://onecell.io/agent-setup/hook.sh; ONECELL_URL overrides it.
ONECELL_DEFAULT_URL='https://onecell.io'
ONECELL_URL="${ONECELL_URL:-$ONECELL_DEFAULT_URL}"
ONECELL_API_KEY="${ONECELL_API_KEY:-$CLAUDE_PLUGIN_OPTION_API_KEY}"
[ -n "$ONECELL_API_KEY" ] || exit 0
command -v jq >/dev/null 2>&1 || exit 0

input=$(cat)
name=$(printf '%s' "$input" | jq -r '.hook_event_name // empty')
session=$(printf '%s' "$input" | jq -r '.session_id // "unknown"')

case "$name" in
  UserPromptSubmit) event=prompt ;;
  SessionStart)     event=session ;;
  Stop)
    # Already continuing because of a Stop hook: do not ask again.
    [ "$(printf '%s' "$input" | jq -r '.stop_hook_active // false')" = "true" ] && exit 0
    event=stop ;;
  *) exit 0 ;;
esac

client="codex"; [ -n "$CLAUDE_PLUGIN_OPTION_API_KEY" ] && client="claude-code"

# Neither the key nor the prompt goes on a command line, where any other user of this
# machine could read it with ps: the request body (which carries the prompt) is built from
# stdin into a file only this user can read, and the key reaches curl on stdin (-H @-).
umask 077
body_file=$(mktemp "${TMPDIR:-/tmp}/onecell-hook.XXXXXX") || exit 0
trap 'rm -f "$body_file"' EXIT
printf '%s' "$input" | jq -c --arg event "$event" --arg session "$session" --arg client "$client" '{
  jsonrpc: "2.0", id: 1, method: "tools/call",
  params: {name: "hook_event", arguments: ({
    event: $event, session_id: $session, client: $client,
    prompt: (.prompt // null), last_message: (.last_assistant_message // null), source: (.source // null)
  } | with_entries(select(.value != null)))}
}' > "$body_file" 2>/dev/null || exit 0

answer=$(printf 'Authorization: Bearer %s\n' "$ONECELL_API_KEY" | curl -sS --max-time 8 "$ONECELL_URL/api/mcp" \
  -H @- \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data-binary @"$body_file" 2>/dev/null | jq -r '.result.content[0].text // empty' 2>/dev/null)

# onecell answers in the hook shape Codex reads (hookSpecificOutput.additionalContext, or
# {"decision":"block",…} for a stop), so it goes out as is.
[ -n "$answer" ] && printf '%s\n' "$answer"
exit 0
