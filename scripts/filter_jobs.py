TARGET_LOCATIONS = [
    "gurgaon",
    "gurugram",
    "delhi",
    "noida",
    "mumbai",
    "remote",
    "worldwide"
]

def keep_job(job):

    location = job["location"].lower()

    return any(
        loc in location
        for loc in TARGET_LOCATIONS
    )
