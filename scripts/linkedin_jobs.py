import requests
from bs4 import BeautifulSoup


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

        print(f"LinkedIn status code: {response.status_code}")

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        cards = soup.find_all("li")

        print(f"LinkedIn cards found: {len(cards)}")

        for card in cards:

            try:

                title = card.find("h3")
                company = card.find("h4")
                location = card.find("span", class_="job-search-card__location")
                link = card.find("a")

                if not title:
                    continue

                jobs.append({
                    "company": company.get_text(strip=True) if company else "Unknown",
                    "role": title.get_text(strip=True),
                    "location": location.get_text(strip=True) if location else "Unknown",
                    "link": link["href"] if link else "",
                    "source": "LINKEDIN"
                })

            except Exception:
                continue

        print(f"LinkedIn jobs extracted: {len(jobs)}")

    except Exception as e:

        print(f"LinkedIn error: {e}")

    return jobs
