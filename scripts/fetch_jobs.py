from datetime import datetime

print("Reading company list...")

with open("config/companies.txt", "r") as f:
    companies = [line.strip() for line in f if line.strip()]

print(f"Found {len(companies)} companies")

with open("data/jobs.csv", "a") as f:
    for company in companies:
        f.write(
            f"{datetime.now().date()},{company},TEST_ROLE,Gurgaon,https://example.com,TEST\n"
        )

print("Jobs written successfully")
