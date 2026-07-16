# scripts/naukri_jobs.py

import requests

def get_naukri_jobs():

    jobs = []

    try:

        response = requests.get(
            "https://www.naukri.com",
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )
            },
            timeout=20
        )

        print(
            f"Naukri status: "
            f"{response.status_code}"
        )

        print(
            f"Naukri response length: "
            f"{len(response.text)}"
        )

    except Exception as e:

        print(
            f"Naukri error: {e}"
        )

    return jobs
