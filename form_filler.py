"""
Your form's config. THIS IS THE ONLY FILE YOU NEED TO EDIT.

Fill in the 3 TODOs below, then run it with run.py.
Nothing in run.py needs changing.
"""

import random, urllib.request, urllib.parse

# TODO 1: your form's submit URL
# Open your form, copy the responder link, e.g.
#   https://docs.google.com/forms/d/e/XXXX/viewform
# Replace /viewform with /formResponse and paste it here.
FORM_URL = "https://docs.google.com/forms/d/e/PASTE_YOUR_FORM_ID_HERE/formResponse"

# TODO 2: your entry IDs, in question order
# In the form editor: three dots > Get prefilled link.
# Fill in one dummy answer for every question, click Get link.
# That link contains entry.123456789 for each question, in order.
# q1 = first question, q2 = second, etc. Add/remove lines to match your form.
E = {
    "q1": "PASTE_ENTRY_ID_1",
    "q2": "PASTE_ENTRY_ID_2",
    "q3": "PASTE_ENTRY_ID_3",
    # "q4": "PASTE_ENTRY_ID_4",
}


def pick(opts_weights):
    opts, ws = zip(*opts_weights)
    return random.choices(opts, weights=ws, k=1)[0]


# TODO 3: rewrite gen_row() for YOUR questions.
# - Multiple choice / Likert: use pick() with the EXACT option text
#   from your form, and weights that look realistic (not all equal).
#   The numbers are just relative weights, e.g. 30 vs 50 means
#   the second option shows up more often.
# - Paragraph / short answer: use a pool of messy, realistic answers
#   like below, and sometimes leave it blank (questions are not required).
# - The keys (q1, q2...) must match E above, and the values must match
#   your form's option text EXACTLY, or Google will reject that answer.
PARAGRAPH_POOL = [
    "example messy answer in lowercase",
    "another realistic answer with a typo",
    "a longer rambling one that goes on a bit",
]


def gen_row():
    row = {}
    # Example: a multiple-choice question
    row["q1"] = pick([("Option A", 30), ("Option B", 50), ("Option C", 20)])
    # Example: a Likert question
    row["q2"] = pick([
        ("Strongly disagree", 5), ("Disagree", 15), ("Neutral", 25),
        ("Agree", 35), ("Strongly agree", 20),
    ])
    # Example: a paragraph question, ~15% blank
    row["q3"] = "" if random.random() < 0.15 else random.choice(PARAGRAPH_POOL)
    return row


def submit(row):
    data = {}
    for k, v in row.items():
        if v == "":
            continue
        data[f"entry.{E[k]}"] = v
    data["submit"] = "Submit"
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(FORM_URL, data=encoded, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read().decode(errors="ignore")
            return r.status, ("Thank you" in body or "recorded" in body or "Your response" in body, len(body))
    except Exception as e:
        return None, (str(e), 0)
