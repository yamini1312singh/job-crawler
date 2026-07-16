import requests


def get_naukri_jobs():

    jobs = []

    try:

        response = requests.get(
            "https://www.naukri.com/product-manager-jobs",
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

        html = response.text

        checks = [
            "__NEXT_DATA__",
            "__INITIAL_STATE__",
            "jobDetails",
            '"jobId"',
            '"companyName"',
            '"title"',
            '"jdURL"',
            '"company"',
        ]

        print("----- NAUKRI CHECK -----")

        for c in checks:
            print(f"{c}: {c in html}")

        print("----- END CHECK -----")

    except Exception as e:

        print(
            f"Naukri error: {e}"
        )

    return jobs
