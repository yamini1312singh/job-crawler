import pandas as pd
from datetime import datetime

from job_sources import get_sample_jobs
from filter_jobs import keep_job

all_jobs = get_sample_jobs()

jobs = [
    job
    for job in all_jobs
    if keep_job(job)
]

for job in jobs:
    job["date"] = str(datetime.now().date())

df = pd.DataFrame(jobs)

df.to_csv("data/jobs.csv", index=False)

print(f"Downloaded {len(all_jobs)} jobs")
print(f"Filtered to {len(jobs)} jobs")

df.to_csv("data/jobs.csv", index=False)

print("CSV updated successfully")
