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

        print(f"Searching Indeed for: {term}")

    print("Indeed collection not implemented yet")

    return jobs
