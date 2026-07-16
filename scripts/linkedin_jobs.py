import requests


def get_linkedin_jobs():

    jobs = []

    print("LinkedIn source loaded")

    try:

        url = (
            "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
            "?keywords=Product%20Manager"
            "&location=India"
        )

        response = requests.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )
            },
            timeout=20
        )

        print(
            f"LinkedIn status code: "
            f"{response.status_code}"
        )

        print(
            f"LinkedIn response length: "
            f"{len(response.text)}"
        )

    except Exception as e:

        print(
            f"LinkedIn error: {e}"
        )

    return jobs
