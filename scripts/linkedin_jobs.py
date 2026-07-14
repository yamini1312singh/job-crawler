def get_linkedin_jobs():

    jobs = []

    with open("config/linkedin_search_terms.txt") as f:

        search_terms = [
            line.strip()
            for line in f
            if line.strip()
        ]

    with open("config/linkedin_locations.txt") as f:

        locations = [
            line.strip()
            for line in f
            if line.strip()
        ]

    print("LinkedIn source loaded")

    print(
        f"Loaded {len(search_terms)} search terms"
    )

    print(
        f"Loaded {len(locations)} locations"
    )

    return jobs
