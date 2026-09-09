# Worked Example: A Research Extraction

This is what a finished file in a case project's `research/` folder
looks like. It is a model, not a template to fill in — the point is the
shape: provenance at the top, quoted material in complete blocks with
stable IDs, gaps declared rather than elided, and analysis kept visibly
separate from evidence.

Read it alongside `document-handling.md` (which says when an extraction
is warranted and how the registry works) and `evidence-standards.md`
(which governs everything below the frontmatter). The example uses a
Telegram-style chat export; the same shape applies to transaction logs,
browser history, or a folder of emails.

Everything after the rule is the example file itself.

---

```markdown
---
purpose: Whether the parties treated the Kia as jointly owned after separation
source: evidence/messages/messages.json — jq keyword locate on "car|kia|insurance", then full ID ranges 8801-8809 and 8843-8847
primary_source: Telegram export (Sam ↔ Jordan)
extracted: 2026-03-14
---

# Vehicle ownership discussions, February 2022

## Scope of this extraction

Search covered the whole export (14,203 messages, 2019-06-02 to
2024-11-30). Located with a case-insensitive keyword pass on
`car|kia|insurance`, then widened to complete ID ranges so that replies
containing no keyword are included — see the note under Block 2.

Two conversations discuss the vehicle. Both are reproduced in full.
Nothing between them mentions it.

## Block 1 — 2022-02-03, insurance renewal

| ID | Timestamp | Sender | Message |
|----|-----------|--------|---------|
| 8801 | 2022-02-03T09:14:22 | Sam | insurance renewal came for the kia |
| 8802 | 2022-02-03T09:14:40 | Sam | do you want to keep it in your name or switch it |
| 8803 | 2022-02-03T09:51:03 | Jordan | leave it, easier |
| 8804 | 2022-02-03T09:51:19 | Jordan | i'll etransfer you half like last year |
| 8805 | 2022-02-03T09:52:44 | Sam | ok |
| 8806 | 2022-02-03T17:38:10 | Jordan | sent |
| 8807 | 2022-02-03T17:40:02 | Sam | got it thanks |
| 8808 | 2022-02-04T08:02:55 | Jordan | oh also the winter tires are still at my mums |
| 8809 | 2022-02-04T08:03:31 | Sam | no rush |

[No messages about the vehicle between 2022-02-04 and 2022-02-21.]

## Block 2 — 2022-02-21, use of the vehicle

| ID | Timestamp | Sender | Message |
|----|-----------|--------|---------|
| 8843 | 2022-02-21T18:22:07 | Jordan | can i take the car saturday, mums appointment |
| 8844 | 2022-02-21T18:29:55 | Sam | yeah thats fine |
| 8845 | 2022-02-21T18:30:12 | Sam | its half yours anyway lol |
| 8846 | 2022-02-21T18:31:40 | Jordan | ha |
| 8847 | 2022-02-21T18:31:58 | Jordan | thanks |

IDs 8846 and 8847 contain no keyword and would be dropped by a keyword
search. They are included because the rule against dropped messages
applies inside a quoted block, and because a reply of "ha" to 8845 is
part of how that message reads.

## What this establishes

- Both parties contributed to insurance on the vehicle in February 2022,
  after the separation date pleaded in the Notice to Resolve (IDs
  8803-8807).
- The vehicle was registered in Sam's name as of 2022-02-03 (ID 8802,
  and consistent with the registration at
  `evidence/vehicle/registration-2021-11-08.pdf`).

## What this suggests (inference, not fact)

Sam's message at ID 8845 ("its half yours anyway") is consistent with
the parties treating the vehicle as jointly owned after separation. It
is a casual remark in a text message, not a statement of legal position,
and Jordan's reply does not adopt it — so it supports the point without
settling it.

## Not established

- Whether the February 2022 e-transfer was in fact sent or received. ID
  8806 says "sent" and 8807 says "got it"; no bank record has been
  obtained. Requesting the February 2022 statement would move this from
  testimony to documented fact.
- Who paid for the vehicle originally, and in what proportions. Nothing
  in this export addresses it.
```
