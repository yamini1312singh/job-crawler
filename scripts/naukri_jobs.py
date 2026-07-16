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

        keywords = [
            "__NEXT_DATA__",
            "jobDetails",
            "searchResult",
            "jobs",
            "companyName",
            "title"
        ]

        print("\n----- NAUKRI CHECK -----\n")

        for keyword in keywords:

            print(
                f"{keyword}: "
                f"{keyword in html}"
            )

        if "__NEXT_DATA__" in html:

            idx = html.find("__NEXT_DATA__")

            print("\n----- NEXT DATA SNIPPET -----\n")

            print(
                html[max(0, idx - 500): idx + 1500]
            )

            print("\n----- END SNIPPET -----\n")

    except Exception as e:

        print(
            f"Naukri error: {e}"
        )

    return jobs
