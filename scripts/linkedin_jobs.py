import requests
from bs4 import BeautifulSoup


def get_linkedin_jobs():

    jobs = []

    with open("config/linkedin_search_terms.txt") as f:
        search_terms = [
            line.strip()
            for line in f
            if line.strip()
        ]

    print("LinkedIn source loaded")

    for term in search_terms:

        try:

            keyword = term.replace(" ", "%20")

            url = (
                "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
                f"?keywords={keyword}"
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

            soup = BeautifulSoup(
                response.text,
                "lxml"
            )

            cards = soup.find_all("li")

            print(
                f"{term}: {len(cards)} cards found"
            )

            for card in cards:

                try:

                    title = card.find("h3")
                    company = card.find("h4")
                    location = card.find(
                        "span",
                        class_="job-search-card__location"
                    )
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

        except Exception as e:

            print(
                f"LinkedIn error for {term}: {e}"
            )

    print(
        f"LinkedIn jobs extracted: {len(jobs)}"
    )

    return jobs
