# Demo Testing for Job

Submit demo responses to a Google Form, spaced out so the timestamps
don't all land at once. No browser, no Selenium — plain Python posting
straight to the form's submit endpoint.

## Quick start

1. Clone this repo and `cd` into it. You only need Python 3, nothing to install.
2. Open `form_filler.py` — that is the **only file you edit**. It has 3 things to replace:
   - **TODO 1 — `FORM_URL`:** your form's responder link with `/viewform` swapped for `/formResponse`.
   - **TODO 2 — `E` (entry IDs):** in the form editor, go to the three dots > **Get prefilled link**, fill in one dummy answer for every question, and copy the `entry.123456789` numbers from that link, in question order.
   - **TODO 3 — `gen_row()`:** rewrite it for your questions. Multiple choice / Likert answers go in `pick()` with the **exact option text** from your form (Google rejects anything that doesn't match exactly) and realistic weights. Paragraph answers go in `PARAGRAPH_POOL` — messy, lowercase, typos, and sometimes blank.
3. Run it:

```bash
python3 run.py 10
```

## How many, and how spaced out

You pick both when you run it — no code changes needed:

```bash
python3 run.py 20 --min-gap 300 --max-gap 3600
```

- First number = **how many responses** to submit.
- `--min-gap` / `--max-gap` = shortest / longest wait between submissions, **in seconds**.
  - Defaults are 240 (4 min) to 7200 (2 hrs).
  - Cheat sheet: 1 min = 60, 5 min = 300, 15 min = 900, 30 min = 1800, 1 hr = 3600, 2 hrs = 7200.

So `python3 run.py 5 --min-gap 60 --max-gap 300` submits 5 responses,
1 to 5 minutes apart. Each run logs to `fill_log.txt`.

## Checking your total

In the form editor, go to **Responses** — that count is the truth.
Don't run more than your target: the script doesn't know your target,
it just submits however many you asked for. The log's `ok=X/N` line
counts submissions where the confirmation page was actually seen —
if `ok` is lower than what you asked for, something failed; check the
log lines for that submission.

## Multi-page forms

If your form has more than one page (it says "Page 1 of N" at the
bottom), a plain submit only records the **first page** — every later
question comes back blank. In `form_filler.py`, set `PAGE_HISTORY`
to `"0,1,2,..."` up to N-1 (for example `"0,1,2,3"` for a 4-page form)
and the script handles the rest. Leave it as `""` for single-page forms.

## If answers land blank

Two usual causes, in order:

1. **Wrong entry IDs.** The ID must be the number after `entry.` in the
   prefilled link — not the question's own ID. If in doubt, open the
   live form, view the page source, and search for `entry.` to compare.
2. **Multi-page form without `PAGE_HISTORY`** — see above.

## Files

- `form_filler.py` — your form's URL, entry IDs, and answer generator. Edit this.
- `run.py` — the runner (count + gap settings). Don't need to edit this.
