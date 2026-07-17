import pandas as pd
from datetime import datetime
from pathlib import Path

from job_sources import get_sample_jobs
from filter_jobs import keep_job
from check_open import filter_open_jobs
from send_email import send_email


DATA_DIR = Path("data")
JOBS_FILE = DATA_DIR / "jobs.csv"
SEEN_JOBS_FILE = DATA_DIR / "seen_jobs.csv"


def normalise(value):
    return " ".join(str(value or "").lower().split())


def job_key(job):
    # We use job details rather than the full link because tracking
    # details in a link can change even when it is the same job.
    return "|".join(
        normalise(job.get(field))
        for field in ("company", "role", "location")
    )


def history_from_dataframe(dataframe, today):
    required_columns = {"company", "role", "location"}

    if dataframe.empty or not required_columns.issubset(dataframe.columns):
        return pd.DataFrame(
            columns=[
                "job_key",
                "company",
                "role",
                "location",
                "link",
                "first_seen"
            ]
        )

    history = dataframe.copy()

    history["job_key"] = history.apply(
        lambda row: job_key(row),
        axis=1
    )

    if "link" not in history.columns:
        history["link"] = ""

    if "date" in history.columns:
        history["first_seen"] = history["date"].fillna(today)
    else:
        history["first_seen"] = today

    return history[
        [
            "job_key",
            "company",
            "role",
            "location",
            "link",
            "first_seen"
        ]
    ].drop_duplicates(
        subset="job_key",
        keep="first"
    )


def load_seen_jobs(today):
    if SEEN_JOBS_FILE.exists():
        return pd.read_csv(SEEN_JOBS_FILE)

    # On the first run, use the previous daily results as the starting
    # history. Those jobs were already sent in today's successful test.
    if JOBS_FILE.exists():
        return history_from_dataframe(
            pd.read_csv(JOBS_FILE),
            today
        )

    return pd.DataFrame(
        columns=[
            "job_key",
            "company",
            "role",
            "location",
            "link",
            "first_seen"
        ]
    )


# -------------------------
# COLLECT ALL JOBS
# -------------------------
all_jobs = get_sample_jobs()

print(f"Downloaded {len(all_jobs)} jobs")

# -------------------------
# SAVE RAW JOBS
# -------------------------
DATA_DIR.mkdir(exist_ok=True)

pd.DataFrame(all_jobs).to_csv(
    DATA_DIR / "raw_jobs.csv",
    index=False
)

print(f"Saved {len(all_jobs)} raw jobs")

# -------------------------
# APPLY FILTERS AND REMOVE DUPLICATES
# -------------------------
filtered_jobs = [
    job
    for job in all_jobs
    if keep_job(job)
]

jobs = []
current_keys = set()

for job in filtered_jobs:
    key = job_key(job)

    if key and key not in current_keys:
        current_keys.add(key)
        jobs.append(job)

# -------------------------
# FIND JOBS NOT EMAILED BEFORE
# -------------------------
today = str(datetime.now().date())

seen_df = load_seen_jobs(today)

known_keys = set(
    seen_df["job_key"]
    .dropna()
    .astype(str)
)

new_jobs = [
    job
    for job in jobs
    if job_key(job) not in known_keys
]

# -------------------------
# SAVE CURRENT RESULTS
# -------------------------
for job in jobs:
    job["date"] = today

if jobs:
    pd.DataFrame(jobs).to_csv(
        JOBS_FILE,
        index=False
    )
else:
    pd.DataFrame(
        columns=[
            "company",
            "role",
            "location",
            "link",
            "source",
            "date"
        ]
    ).to_csv(
        JOBS_FILE,
        index=False
    )

# -------------------------
# SAVE PERMANENT HISTORY
# -------------------------
new_history_rows = [
    {
        "job_key": job_key(job),
        "company": job["company"],
        "role": job["role"],
        "location": job["location"],
        "link": job["link"],
        "first_seen": today
    }
    for job in new_jobs
]

if new_history_rows:
    seen_df = pd.concat(
        [
            seen_df,
            pd.DataFrame(new_history_rows)
        ],
        ignore_index=True
    )

seen_df = seen_df.drop_duplicates(
    subset="job_key",
    keep="first"
)

seen_df.to_csv(
    SEEN_JOBS_FILE,
    index=False
)

# -------------------------
# LOGS
# -------------------------
print(f"Filtered to {len(jobs)} unique jobs")
print(f"Found {len(new_jobs)} jobs not emailed before")

# -------------------------
# DROP JOBS THAT ARE ALREADY CLOSED
# -------------------------
# Only the new jobs are checked (small set), and the check fails open:
# anything we cannot confirm as closed is kept.
open_jobs = filter_open_jobs(new_jobs)

# -------------------------
# EMAIL ONLY NEW, OPEN JOBS
# -------------------------
if open_jobs:
    email_body = (
        f"Found {len(open_jobs)} new job matches\n\n"
    )

    for job in open_jobs:
        email_body += (
            f"{job['company']} | "
            f"{job['role']} | "
            f"{job['location']}\n"
            f"{job['link']}\n\n"
        )

    send_email(
        subject=f"{len(open_jobs)} New Job Matches",
        body=email_body
    )

    print("New-job email sent successfully")
else:
    print("No new open jobs found; no email sent")
