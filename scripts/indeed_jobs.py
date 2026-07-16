import requests
from bs4 import BeautifulSoup


def get_indeed_jobs():

    jobs = []

    with open("config/search_terms.txt") as f:
        search_terms = [
            line.strip()
            for line in f
            if line.strip()
        ]

    print("Indeed source loaded")

    for term in search_terms:

        try:

            keyword = term.replace(" ", "+")

            url = (
                f"https://in.indeed.com/jobs?q={keyword}"
            )

            response = requests.get(
                url,
                headers={
                    "User-Agent":
                    "Mozilla/5.0"
                },
                timeout=20
            )

            print(
                f"{term}: "
                f"status {response.status_code}"
            )

            soup = BeautifulSoup(
                response.text,
                "lxml"
            )

            cards = soup.find_all("a")

            print(
                f"{term}: "
                f"{len(cards)} links found"
            )

        except Exception as e:

            print(
                f"Indeed error for "
                f"{term}: {e}"
            )

    return jobs
