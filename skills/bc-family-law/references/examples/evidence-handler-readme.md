# Worked Example: An Evidence Handler README

A handler is the `README.md` that sits beside an evidence source and
records how to read it. It is written the first time the source is
touched, so that six months later a different session — or a lawyer, or
the user — queries it the same way instead of rediscovering the format
and quietly getting it slightly wrong.

`document-handling.md` lists what a handler must contain. This is what
one looks like when it is finished, for the hardest and most common
case: a large chat export. For a single readable document the handler is
three or four lines — what it is, how to get text out of it, how to cite
it.

The **Participants** section is the part most easily skipped and most
often needed. An export does not say which display name belongs to the
user; getting it backwards silently reverses the meaning of every quote
drawn from it.

Everything after the rule is the example file itself, at
`evidence/messages/README.md`.

---

```markdown
# Handler: Telegram export (Sam ↔ Jordan)

## Summary

- File: `messages.json` (Telegram JSON export, 38 MB)
- 14,203 messages, 2019-06-02 to 2024-11-30
- Two participants, no group messages
- Exported 2026-03-02 from Sam's desktop Telegram client (per user)

## Participants

| Display name in export | Who this is |
|------------------------|-------------|
| Sam | the user |
| Jordan | the other party |

Confirmed with the user 2026-03-02. The export title ("Chat with
Jordan") implies it was taken from Sam's device, but that is inference —
the mapping above was asked, not deduced.

## Provenance

- Export date: 2026-03-02
- Device/account: Sam's desktop Telegram, own account
- Completeness: covers the full history of this chat as it existed on
  that device. **Not established:** whether any messages were deleted
  before the export, by either party. Telegram deletions are not
  recoverable from a client-side export, and the other party's copy may
  differ.

## Schema

One representative record, verbatim:

```json
{
  "id": 8801,
  "type": "message",
  "date": "2022-02-03T09:14:22",
  "from": "Sam",
  "from_id": "user44120933",
  "text": "insurance renewal came for the kia"
}
```

Notes on the shape, learned the hard way:

- `text` is a string for plain messages but an **array** of fragments
  when the message contains a link, mention, or formatting. Queries that
  assume a string silently skip those messages — always guard with
  `(.text | type == "string")` or normalise first (see below).
- Service messages (`"type": "service"` — joins, pins, calls) have no
  `text`. Filter them out or they surface as empty rows.
- `id` is stable across exports and is the citation key.
- `date` is local time with no offset. Treat displayed times as the
  device's local time and say so if a timing argument turns on it.

## Query templates

Tested against this file. `jq` is available; run from the project root.

```bash
# Normalise once: every message as {id, date, from, text} with array
# text flattened. Most queries below read better piped from this.
jq '[.messages[] | select(.type == "message")
     | {id, date, from, text: (if (.text|type)=="string" then .text
        else ([.text[] | if type=="string" then . else .text end] | join(""))
        end)}]' evidence/messages/messages.json > /tmp/msgs.json

# Keyword search, case-insensitive
jq '.[] | select(.text | test("insurance"; "i"))' /tmp/msgs.json

# Date range
jq '.[] | select(.date >= "2022-02-01" and .date < "2022-03-01")' /tmp/msgs.json

# Complete ID range — use this to widen a keyword hit into a full block
jq '.[] | select(.id >= 8801 and .id <= 8809)' /tmp/msgs.json

# By sender
jq '.[] | select(.from == "Jordan")' /tmp/msgs.json

# Sanity check: message count and date bounds
jq '{count: length, first: .[0].date, last: .[-1].date}' /tmp/msgs.json
```

Keyword searches locate a conversation; they never define its
boundaries. Widen every hit to a complete ID range before quoting —
replies like "ok" and "ha" carry no keyword and dropping them is what
cherry-picking looks like from the other side of a courtroom.

## Citation format

Message ID + full timestamp + sender:

> ID 8803, 2022-02-03T09:51:03, Jordan

See `evidence-standards.md` for the complete-sequence rules that govern
quoting from this file, and `examples/research-extraction.md` for a
finished extraction drawn from it.
```
