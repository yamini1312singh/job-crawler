import pandas as pd
from datetime import datetime

jobs = []

sample_jobs = [
    {
        "date": str(datetime.now().date()),
        "company": "Razorpay",
        "role": "Product Manager",
        "location": "Bangalore",
        "link": "https://razorpay.com/careers/",
        "source": "CAREERS"
    },
    {
        "date": str(datetime.now().date()),
        "company": "Postman",
        "role": "Senior Product Manager",
        "location": "Remote",
        "link": "https://www.postman.com/company/careers/",
        "source": "CAREERS"
    }
]

df = pd.DataFrame(jobs + sample_jobs)

df.to_csv("data/jobs.csv", index=False)

print(f"Saved {len(df)} jobs")
