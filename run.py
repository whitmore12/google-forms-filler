#!/usr/bin/env python3
"""Run the filler. No editing needed here, edit form_filler.py instead.

Usage:
    python3 run.py 10
    python3 run.py 20 --min-gap 300 --max-gap 3600
    python3 run.py 5 --min-gap 240 --max-gap 7200

Arguments:
    count       how many responses to submit (default 5)
    --min-gap   shortest wait between submissions, in seconds (default 240 = 4 min)
    --max-gap   longest wait between submissions, in seconds (default 7200 = 2 hrs)

Gap cheat sheet (seconds):
    1 min = 60, 5 min = 300, 15 min = 900, 30 min = 1800,
    1 hr = 3600, 2 hrs = 7200

Each run logs to fill_log.txt in this folder.
"""
import argparse, datetime, random, sys, time

sys.path.insert(0, ".")
from form_filler import gen_row, submit

parser = argparse.ArgumentParser(description="Submit demo responses to a Google Form.")
parser.add_argument("count", nargs="?", type=int, default=5, help="how many responses to submit")
parser.add_argument("--min-gap", type=int, default=240, help="shortest gap between submissions, seconds")
parser.add_argument("--max-gap", type=int, default=7200, help="longest gap between submissions, seconds")
args = parser.parse_args()

if args.count < 1:
    parser.error("count must be at least 1")
if args.min_gap < 0 or args.max_gap < args.min_gap:
    parser.error("need 0 <= --min-gap <= --max-gap")

log_path = "fill_log.txt"


def log(msg):
    line = f"{datetime.datetime.now().isoformat()} {msg}"
    with open(log_path, "a") as f:
        f.write(line + "\n")
    print(line, flush=True)


log(f"RUN start count={args.count} gap={args.min_gap}-{args.max_gap}s")
random.seed()
ok = 0
for i in range(args.count):
    row = gen_row()
    status, info = submit(row)
    log(f"RUN submit {i + 1}/{args.count} status={status} info={info}")
    if status in (200, 302) and info[0]:
        ok += 1
    if i < args.count - 1:
        gap = random.uniform(args.min_gap, args.max_gap)
        log(f"RUN sleeping {gap:.0f}s before next submission")
        time.sleep(gap)
log(f"RUN done ok={ok}/{args.count} (ok = confirmation page seen)")
