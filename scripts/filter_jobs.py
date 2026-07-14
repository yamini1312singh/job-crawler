TARGET_ROLES = [
    "product",
    "brand",
    "strategy",
    "consultant",
    "growth",
    "product marketing",
    "program manager",
    "innovation"
]

TARGET_LOCATIONS = [
    "gurgaon",
    "gurugram",
    "delhi",
    "noida",
    "mumbai",
    "remote",
    "worldwide",
    "india"
]

def keep_job(job):

    role = job["role"].lower()
    location = job["location"].lower()

    role_match = any(
        keyword in role
        for keyword in TARGET_ROLES
    )

    location_match = any(
        keyword in location
        for keyword in TARGET_LOCATIONS
    )

    return role_match and location_match
