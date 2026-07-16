import pandas as pd
from datetime import datetime

from job_sources import get_sample_jobs
from filter_jobs import keep_job

all_jobs = get_sample_jobs()
raw_df = pd.DataFrame(all_jobs)

raw_df.to_csv(
    "data/raw_jobs.csv",
    index=False
)

print(
    f"Saved {len(all_jobs)} raw jobs"
)
jobs = [
    job
    for job in all_jobs
    if keep_job(job)
]

for job in jobs:
    job["date"] = str(datetime.now().date())

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

df.to_csv("data/jobs.csv", index=False)

print(f"Downloaded {len(all_jobs)} jobs")
print(f"Filtered to {len(jobs)} jobs")

print("\nMATCHING JOBS:\n")

for job in jobs:
    print(
        f"{job['company']} | "
        f"{job['role']} | "
        f"{job['location']}"
    )

df.to_csv("data/jobs.csv", index=False)

print("CSV updated successfully")
