import requests

def get_sample_jobs():

    jobs = []

    try:
        url = "https://boards-api.greenhouse.io/v1/boards/postman/jobs"

        response = requests.get(url)

        data = response.json()

        for job in data["jobs"]:

            jobs.append({
                "company": "Postman",
                "role": job["title"],
                "location": job["location"]["name"],
                "link": job["absolute_url"],
                "source": "GREENHOUSE"
            })

    except Exception as e:
        print(e)

    return jobs
