import requests

from linkedin_jobs import get_linkedin_jobs
from naukri_jobs import get_naukri_jobs

# from indeed_jobs import get_indeed_jobs


# -------------------------
# GREENHOUSE
# -------------------------

def get_greenhouse_jobs():

    jobs = []

    with open("config/greenhouse_companies.txt") as f:

        companies = [
            line.strip()
            for line in f
            if line.strip()
        ]

    for company in companies:

        try:

            url = (
                f"https://boards-api.greenhouse.io/"
                f"v1/boards/{company}/jobs"
            )

            response = requests.get(
                url,
                timeout=15
            )

            if response.status_code != 200:

                print(
                    f"FAILED -> {company} -> "
                    f"Status Code: {response.status_code}"
                )

                continue

            data = response.json()

            print(
                f"SUCCESS -> {company} -> "
                f"{len(data['jobs'])} jobs found"
            )

            for job in data["jobs"]:

                jobs.append({
                    "company": company.title(),
                    "role": job["title"],
                    "location": job["location"]["name"],
                    "link": job["absolute_url"],
                    "source": "GREENHOUSE"
                })

        except Exception as e:

            print(
                f"ERROR -> {company} -> {e}"
            )

    return jobs


# -------------------------
# MASTER FUNCTION
# -------------------------

def get_sample_jobs():

    jobs = []

    jobs.extend(get_greenhouse_jobs())

    # Temporarily disabled
    # jobs.extend(get_indeed_jobs())

    jobs.extend(get_linkedin_jobs())

    jobs.extend(get_naukri_jobs())

    print(
        f"TOTAL JOBS COLLECTED: {len(jobs)}"
    )

    return jobs
