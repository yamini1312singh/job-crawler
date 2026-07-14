import requests

GREENHOUSE_COMPANIES = [
    "postman",
    "browserstack",
    "atlan"
]

def get_sample_jobs():

    jobs = []

    for company in GREENHOUSE_COMPANIES:

        try:

            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

            response = requests.get(url, timeout=15)

            if response.status_code != 200:
                continue

            data = response.json()

            for job in data["jobs"]:

                jobs.append({
                    "company": company.title(),
                    "role": job["title"],
                    "location": job["location"]["name"],
                    "link": job["absolute_url"],
                    "source": "GREENHOUSE"
                })

        except Exception as e:
            print(f"Error with {company}: {e}")

    return jobs
