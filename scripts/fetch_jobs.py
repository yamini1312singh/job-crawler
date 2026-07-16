import pandas as pd
from datetime import datetime

from job_sources import get_sample_jobs
from filter_jobs import keep_job
from send_email import send_email


# -------------------------
# COLLECT ALL JOBS
# -------------------------
all_jobs = get_sample_jobs()

print(
    f"Downloaded {len(all_jobs)} jobs"
)

# -------------------------
# SAVE RAW JOBS
# -------------------------
raw_df = pd.DataFrame(all_jobs)

raw_df.to_csv(
    "data/raw_jobs.csv",
    index=False
)

print(
    f"Saved {len(all_jobs)} raw jobs"
)

# -------------------------
# APPLY FILTERS
# -------------------------
jobs = [
    job
    for job in all_jobs
    if keep_job(job)
]

# -------------------------
# REMOVE DUPLICATES
# -------------------------
seen = set()

unique_jobs = []

for job in jobs:

    key = (
        job["company"],
        job["role"],
        job["location"]
    )

    if key not in seen:
        seen.add(key)
        unique_jobs.append(job)

jobs = unique_jobs

# -------------------------
# ADD DATE
# -------------------------
for job in jobs:

    job["date"] = str(
        datetime.now().date()
    )

# -------------------------
# SAVE FILTERED JOBS
# -------------------------
if jobs:

    df = pd.DataFrame(jobs)

else:

    df = pd.DataFrame(
        columns=[
            "company",
            "role",
            "location",
            "link",
            "source",
            "date"
        ]
    )

df.to_csv(
    "data/jobs.csv",
    index=False
)

# -------------------------
# LOGS
# -------------------------
print(
    f"Filtered to {len(jobs)} jobs"
)

print("\nMATCHING JOBS:\n")

for job in jobs:

    print(
        f"{job['company']} | "
        f"{job['role']} | "
        f"{job['location']}"
    )

print(
    "CSV updated successfully"
)

# -------------------------
# EMAIL RESULTS
# -------------------------
if jobs:

    email_body = (
        f"Found {len(jobs)} matching jobs\n\n"
    )

    for job in jobs:

        email_body += (
            f"{job['company']} | "
            f"{job['role']} | "
            f"{job['location']}\n"
            f"{job['link']}\n\n"
        )

    send_email(
        subject=f"{len(jobs)} New Job Matches",
        body=email_body
    )

    print(
        "Email sent successfully"
    )

else:

    send_email(
        subject="No New Job Matches",
        body="No matching jobs found today."
    )

    print(
        "No jobs found email sent"
    )
