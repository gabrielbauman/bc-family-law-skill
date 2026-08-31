# Evidence

Primary source files: message exports, emails, letters, financial
records, screenshots. **Nothing in this folder is ever modified,
renamed, or "cleaned up"** — extraction happens *from* here into
`research/`. Files change only when the user adds new source material.

(If you're the human reading this: you don't have to file things here
yourself. Drop new material into `inbox/` — or anywhere — and it will
be identified, filed here with a proper handler, and recorded.)

## Organization

One subfolder per source or source type, each with its own `README.md`
handler describing the format, how to query it, and the citation format
(see the skill's `references/document-handling.md` for handler
contents):

```
evidence/
├── messages/        # e.g. chat export: messages.json + README.md with jq queries
├── email/           # .eml files named YYYY-MM-DD_HHMM_Sender_to_Recipient_Subject.eml
├── letters/
├── paystubs/
├── tax_forms/
└── screenshots/     # descriptive names including capture dates
```

## Naming

Filenames are citations — make them carry date, parties, and subject
wherever the format allows. A folder of `IMG_4032.png` is evidence
nobody can cite; `browser-history-2023-10-04-apartment-search.png` cites
itself.

## Provenance

Record where each source came from (export date, device, account) in
the source's README. Provenance questions come up at trial ("when was
this export made? is it complete?") and the time to capture the answer
is when the file arrives.
