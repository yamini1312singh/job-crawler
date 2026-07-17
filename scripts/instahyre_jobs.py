import time

import requests

# -------------------------
# INSTAHYRE
# -------------------------
#
# Instahyre renders jobs client-side (AngularJS) and its listings come
# from an internal JSON API rather than the HTML. Free-text keyword
# search is not honoured server-side, but filtering by "job function"
# id is, so we pull by function id and let filter_jobs.keep_job() do
# the final role + location precision filtering downstream.
#
# Page size is capped by the server at 35 results, so we paginate a
# small number of pages per function to catch the most recent postings
# without hammering the endpoint.

SEARCH_URL = "https://www.instahyre.com/api/v1/job_search"
PRIME_URL = "https://www.instahyre.com/search-jobs/"

PAGE_SIZE = 35
PAGES_PER_FUNCTION = 3

# Seconds to wait between requests, and the longer cooldown to use
# when the server returns 429 (Too Many Requests).
REQUEST_DELAY = 2
RATE_LIMIT_COOLDOWN = 15

USER_AGENT = (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)


def load_function_ids():

    ids = []

    with open("config/instahyre_functions.txt") as f:

        for line in f:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            # Supports "11" or "11  # Product Management"
            first_token = line.split()[0]

            if first_token.isdigit():
                ids.append(first_token)

    return ids


def get_instahyre_jobs():

    jobs = []
    seen_ids = set()

    function_ids = load_function_ids()

    print("Instahyre source loaded")

    session = requests.Session()

    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Referer": PRIME_URL,
    })

    # Prime the session so we pick up the csrftoken cookie the same
    # way a browser would before hitting the API.
    try:
        session.get(PRIME_URL, timeout=20)
    except Exception as e:
        print(f"Instahyre prime failed: {e}")

    for function_id in function_ids:

        for page in range(PAGES_PER_FUNCTION):

            offset = page * PAGE_SIZE

            try:

                response = session.get(
                    SEARCH_URL,
                    params={
                        "limit": PAGE_SIZE,
                        "offset": offset,
                        "job_functions": function_id,
                    },
                    timeout=30
                )

                # If rate limited, cool down and retry once. If it is
                # still limited, stop the whole crawl and keep what we
                # already have rather than hammering the server.
                if response.status_code == 429:

                    print(
                        f"RATE LIMITED -> function {function_id} "
                        f"offset {offset} -> waiting {RATE_LIMIT_COOLDOWN}s"
                    )

                    time.sleep(RATE_LIMIT_COOLDOWN)

                    response = session.get(
                        SEARCH_URL,
                        params={
                            "limit": PAGE_SIZE,
                            "offset": offset,
                            "job_functions": function_id,
                        },
                        timeout=30
                    )

                    if response.status_code == 429:

                        print(
                            "Still rate limited; stopping Instahyre "
                            "crawl early."
                        )

                        return jobs

                if response.status_code != 200:

                    print(
                        f"FAILED -> function {function_id} "
                        f"offset {offset} -> "
                        f"Status Code: {response.status_code}"
                    )

                    break

                objects = response.json().get("objects", [])

                print(
                    f"function {function_id} | offset={offset} | "
                    f"results={len(objects)}"
                )

                if not objects:
                    break

                for job in objects:

                    job_id = job.get("id")

                    if job_id in seen_ids:
                        continue

                    seen_ids.add(job_id)

                    employer = job.get("employer") or {}

                    if isinstance(employer, dict):
                        company = employer.get("company_name", "Unknown")
                    else:
                        company = str(employer)

                    jobs.append({
                        "company": company or "Unknown",
                        "role": job.get("title", ""),
                        "location": job.get("locations") or "Unknown",
                        "link": job.get("public_url", ""),
                        "source": "INSTAHYRE"
                    })

                # Be polite between requests.
                time.sleep(REQUEST_DELAY)

            except Exception as e:

                print(
                    f"ERROR -> function {function_id} "
                    f"offset {offset} -> {e}"
                )

                break

    print(f"Instahyre jobs extracted: {len(jobs)}")

    return jobs
