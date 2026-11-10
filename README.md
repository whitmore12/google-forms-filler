# Google Forms Filler

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
it just submits however many you asked for.

## Files

- `form_filler.py` — your form's URL, entry IDs, and answer generator. Edit this.
- `run.py` — the runner (count + gap settings). Don't need to edit this.
