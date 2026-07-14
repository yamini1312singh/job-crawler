import pandas as pd
from datetime import datetime
from scripts.job_sources import get_sample_jobs

jobs = get_sample_jobs()

for job in jobs:
    job["date"] = str(datetime.now().date())

df = pd.DataFrame(jobs)

df.to_csv("data/jobs.csv", index=False)

print(f"Saved {len(df)} jobs")
