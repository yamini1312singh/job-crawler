import re
import time

import requests

# -------------------------
# OPEN-JOB VERIFICATION
# -------------------------
#
# Some scraped postings are already closed ("no longer accepting
# applications") by the time we would email them. This module checks
# each job's link and drops the ones we can CONFIRM are closed.
#
# Design principle: FAIL OPEN. If a check errors, times out, or is
# rate limited, we KEEP the job. It is far better to occasionally
# show a closed job than to hide a real opening. We only remove a job
# when the source explicitly tells us it is closed.
#
# Only run this on the small set of NEW jobs about to be emailed, not
# on the full scrape, so request volume (and rate-limit risk) stays low.

USER_AGENT = (
    "Mozilla/5.0 "
    "(Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)

# Polite pause between checks (seconds).
CHECK_DELAY = 2

# LinkedIn throttles hard after the scrape run, so the check retries
# on throttle (HTTP 429, and LinkedIn's signature 999) with backoff
# before giving up.
LINKEDIN_MAX_RETRIES = 3
LINKEDIN_BACKOFF = 12

# Phrases that indicate a posting is closed.
CLOSED_PHRASES = [
    "no longer accepting applications",
    "this job is no longer available",
    "position has been filled",
    "position has been closed",
    "applications are closed",
    "job is no longer active",
    "no longer available",
]


def _linkedin_job_id(link):
    match = re.search(r"-(\d{6,})(?:\?|/|$)", link)

    if match:
        return match.group(1)

    match = re.search(r"/view/(?:.*-)?(\d{6,})", link)

    return match.group(1) if match else None


def _is_greenhouse_open(session, link):
    # A taken-down Greenhouse job 404s on the API, and on the public
    # board it 302-bounces to the board root with "?error=true"
    # (dropping the "/jobs/<id>" path). A live job stays on its URL.
    response = session.get(link, timeout=20, allow_redirects=True)

    if response.status_code in (404, 410):
        return False

    final_url = response.url.lower()

    if "error=true" in final_url or "/jobs/" not in final_url:
        return False

    return True


def _linkedin_detail(session, job_id):
    url = (
        "https://www.linkedin.com/jobs-guest/jobs/api/"
        f"jobPosting/{job_id}"
    )

    response = None

    for attempt in range(LINKEDIN_MAX_RETRIES):

        response = session.get(url, timeout=20)

        # 429 and LinkedIn's 999 both mean "throttled" -> wait longer
        # and retry so we can get a real answer.
        if response.status_code in (429, 999):
            time.sleep(LINKEDIN_BACKOFF * (attempt + 1))
            continue

        return response

    return response


def _is_linkedin_open(session, link):
    job_id = _linkedin_job_id(link)

    if not job_id:
        return True  # can't verify -> keep

    response = _linkedin_detail(session, job_id)

    if response is None:
        return True

    # A removed job returns 404 -> definitely closed.
    if response.status_code in (404, 410):
        return False

    # Still throttled after all retries -> can't verify -> keep.
    if response.status_code != 200:
        return True

    text = response.text.lower()

    # Explicit closed signals.
    if any(phrase in text for phrase in CLOSED_PHRASES):
        return False

    if "closed-job__flavor--closed" in text:
        return False

    # An open posting always renders the apply CTA. On a fully loaded
    # page, its absence means the posting is closed.
    if "apply-button--default" not in text and len(text) > 2000:
        return False

    return True


def _is_generic_open(session, link):
    response = session.get(link, timeout=20)

    if response.status_code in (404, 410):
        return False

    if response.status_code != 200:
        return True  # can't verify -> keep

    text = response.text.lower()

    return not any(phrase in text for phrase in CLOSED_PHRASES)


def is_job_open(session, job):

    link = job.get("link", "")
    source = (job.get("source") or "").upper()

    if not link:
        return True

    try:

        if source == "GREENHOUSE" or "greenhouse.io" in link:
            return _is_greenhouse_open(session, link)

        if source == "LINKEDIN" or "linkedin.com" in link:
            return _is_linkedin_open(session, link)

        # Instahyre and anything else: generic page/phrase check.
        return _is_generic_open(session, link)

    except Exception as e:

        print(f"OPEN-CHECK error (keeping) -> {link[:60]} -> {e}")

        return True  # fail open


def filter_open_jobs(jobs):

    if not jobs:
        return jobs

    session = requests.Session()

    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept-Language": "en-US,en;q=0.9",
    })

    open_jobs = []
    dropped = 0

    print(f"Checking {len(jobs)} new jobs for open/closed status")

    for job in jobs:

        if is_job_open(session, job):
            open_jobs.append(job)
        else:
            dropped += 1
            print(
                f"CLOSED -> dropping: "
                f"{job.get('company')} | {job.get('role')}"
            )

        time.sleep(CHECK_DELAY)

    print(
        f"Open-check complete: {len(open_jobs)} open, "
        f"{dropped} closed and dropped"
    )

    return open_jobs
