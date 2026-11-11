"""
Your form's config. THIS IS THE ONLY FILE YOU NEED TO EDIT.

Fill in the 3 TODOs below, then run it with run.py.
Nothing in run.py needs changing.
"""

import random, re, http.cookiejar, urllib.request, urllib.parse

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
# TIP: the entry ID is the number AFTER "entry." — not the question's
# own ID. If your answers land blank, you almost certainly used the
# wrong one. Check it against the form page: view the form, search the
# page source for "entry." and compare.
E = {
    "q1": "PASTE_ENTRY_ID_1",
    "q2": "PASTE_ENTRY_ID_2",
    "q3": "PASTE_ENTRY_ID_3",
    # "q4": "PASTE_ENTRY_ID_4",
}

# TODO 4 (only if your form has MORE THAN ONE PAGE):
# Open your form and look at the bottom: it says "Page 1 of N".
# Set PAGE_HISTORY to "0,1,2,..." up to N-1, e.g. "0,1,2,3" for 4 pages.
# Leave it as "" for a single-page form.
# WHY: on a multi-page form a plain POST only records the FIRST page's
# answers — every later question comes back blank. With PAGE_HISTORY set,
# submit() first loads the form for a fresh token, then posts everything
# at once with all pages marked visited.
PAGE_HISTORY = ""

# What counts as "it worked": a phrase from your form's confirmation page.
# Google's default is "Your response has been recorded". Some forms have
# a custom message instead — submit one response by hand, read the
# confirmation page, and paste a distinctive phrase from it here.
# NEVER use a bare "Thank you": form descriptions often contain those
# words, so that check passes even when nothing was recorded.
CONFIRM_TEXT = "Your response has been recorded"


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
# - Checkbox ("select all that apply"): return a LIST of options, e.g.
#   row["q4"] = ["Option A", "Option C"] — submit() sends one value per item.
# - Keep answers CONSISTENT with each other: a 25-34-year-old respondent
#   is usually a grad student or working, not a college freshman; a
#   "Never" user shouldn't also list three apps they use daily.
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


_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


def submit(row):
    pairs = []
    for k, v in row.items():
        if v == "" or v is None:
            continue
        if isinstance(v, list):  # checkbox question: one pair per option
            for item in v:
                pairs.append((f"entry.{E[k]}", item))
        else:
            pairs.append((f"entry.{E[k]}", v))
    try:
        if PAGE_HISTORY:
            # Multi-page form: load the form for a fresh fbzx +
            # partialResponse token, then post everything with all
            # pages marked visited. Without this, only page 1 records.
            jar = http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
            view_url = FORM_URL.replace("/formResponse", "/viewform")
            html = opener.open(urllib.request.Request(view_url, headers={"User-Agent": _UA}), timeout=20).read().decode(errors="ignore")
            fbzx = re.search(r'fbzx" value="([0-9-]+)', html).group(1)
            pr = re.search(r'partialResponse" value="([^"]+)"', html).group(1).replace('&quot;', '"')
            pairs += [("fvv", "1"), ("partialResponse", pr), ("pageHistory", PAGE_HISTORY),
                      ("fbzx", fbzx), ("submissionTimestamp", "-1"), ("submit", "Submit")]
            req = urllib.request.Request(FORM_URL, data=urllib.parse.urlencode(pairs).encode(), headers={
                "User-Agent": _UA,
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": view_url,
            })
            with opener.open(req, timeout=20) as r:
                body = r.read().decode(errors="ignore")
                return r.status, (CONFIRM_TEXT in body, len(body))
        pairs.append(("submit", "Submit"))
        encoded = urllib.parse.urlencode(pairs).encode()
        req = urllib.request.Request(FORM_URL, data=encoded, headers={
            "User-Agent": _UA,
            "Content-Type": "application/x-www-form-urlencoded",
        })
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read().decode(errors="ignore")
            return r.status, (CONFIRM_TEXT in body, len(body))
    except Exception as e:
        return None, (str(e), 0)
