from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


SEARCH_TERMS_FILE = Path("config/linkedin_search_terms.txt")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
}


def text_or_unknown(element):
    if element:
        text = element.get_text(" ", strip=True)

        if text:
            return text

    return "Unknown"


def get_naukri_jobs():
    jobs = []

    with open(SEARCH_TERMS_FILE, encoding="utf-8") as file:
        search_terms = [
            line.strip()
            for line in file
            if line.strip()
        ]

    print("Naukri source loaded")

    for term in search_terms:
        slug = term.lower().replace(" ", "-")

        url = (
            f"https://www.naukri.com/"
            f"{slug}-jobs-in-india"
        )

        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=20
            )

            print(
                f"Naukri | {term} | "
                f"status={response.status_code}"
            )

            if response.status_code != 200:
                continue

            soup = BeautifulSoup(
                response.text,
                "lxml"
            )

            cards = soup.select(
                "div.cust-job-tuple, "
                "div.srp-jobtuple-wrapper, "
                "article.jobTuple"
            )

            print(
                f"Naukri | {term} | "
                f"cards={len(cards)}"
            )

            for card in cards:
                title_element = card.select_one(
                    "a.title, "
                    "a.titleEllipsis, "
                    "a.jobTitle"
                )

                if not title_element:
                    continue

                company_element = card.select_one(
                    "a.comp-name, "
                    "a.compName, "
                    "a.subTitle"
                )

                location_element = card.select_one(
                    "span.locWdth, "
                    "span.location, "
                    "li.location"
                )

                link = title_element.get("href", "").strip()

                if not link:
                    continue

                jobs.append(
                    {
                        "company": text_or_unknown(
                            company_element
                        ),
                        "role": text_or_unknown(
                            title_element
                        ),
                        "location": text
