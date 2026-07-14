def get_indeed_jobs():

    jobs = []

    search_terms = [
        "product manager",
        "brand manager",
        "strategy manager",
        "consultant"
    ]

    print("Indeed source loaded")

    for term in search_terms:

        print(f"Searching Indeed for: {term}")

    return jobs
