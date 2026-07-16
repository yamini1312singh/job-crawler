import requests

from indeed_jobs import get_indeed_jobs
from linkedin_jobs import get_linkedin_jobs
from naukri_jobs import get_naukri_jobs

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

            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

            response = requests.get(url, timeout=15)

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
# LEVER (placeholder)
# -------------------------

def get_lever_jobs():

    jobs = []

    return jobs


# -------------------------
# INDEED
# -------------------------

def get_indeed_jobs_wrapper():

    return get_indeed_jobs()


# -------------------------
# LINKEDIN
# -------------------------

def get_linkedin_jobs_wrapper():

    return get_linkedin_jobs()


# -------------------------
# NAUKRI (placeholder)
# -------------------------

def get_naukri_jobs():

    jobs = []

    return jobs


# -------------------------
# INSTAHYRE (placeholder)
# -------------------------

def get_instahyre_jobs():

    jobs = []

    return jobs


# -------------------------
# IIMJOBS (placeholder)
# -------------------------

def get_iimjobs_jobs():

    jobs = []

    return jobs


# -------------------------
# MASTER FUNCTION
# -------------------------

def get_sample_jobs():

    jobs = []

    jobs.extend(get_greenhouse_jobs())
    jobs.extend(get_lever_jobs())
    jobs.extend(get_indeed_jobs_wrapper())
    jobs.extend(get_linkedin_jobs_wrapper())
    jobs.extend(get_naukri_jobs())
    jobs.extend(get_instahyre_jobs())
    jobs.extend(get_iimjobs_jobs())

    print(f"TOTAL JOBS COLLECTED: {len(jobs)}")

    return jobs
