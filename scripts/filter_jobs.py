TARGET_ROLES = [
    "product manager",
    "associate product manager",
    "senior product manager",
    "group product manager",
    "lead product manager",
    "growth product manager",
    "product marketing manager",
    "brand manager",
    "senior brand manager",
    "strategy manager",
    "consultant",
    "senior consultant",
    "business consultant",
    "program manager"
]

TARGET_LOCATIONS = [
    "gurgaon",
    "gurugram",
    "new delhi",
    "delhi",
    "noida",
    "mumbai",
    "remote"
]

def keep_job(job):

    role = job["role"].lower()
    location = job["location"].lower()

    role_match = any(
        target in role
        for target in TARGET_ROLES
    )

    location_match = any(
        target in location
        for target in TARGET_LOCATIONS
    )

    return role_match and location_match
