import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")


def search_jobs(role: str, location: str = ""):

    url = (
    f"https://api.adzuna.com/v1/api/jobs/in/search/1"
    f"?app_id={APP_ID}"
    f"&app_key={APP_KEY}"
    f"&what={role}"
    f"&results_per_page=20"
    )

    if location:
        url += f"&where={location}"

    response = requests.get(url)

    data = response.json()

    jobs = []

    for item in data.get("results", []):

        jobs.append(
            {
                "company": item.get(
                    "company",
                    {}
                ).get(
                    "display_name",
                    "Unknown"
                ),

                "role": item.get(
                    "title",
                    "Unknown"
                ),

                "location": item.get(
                    "location",
                    {}
                ).get(
                    "display_name",
                    "Unknown"
                ),

                "url": item.get(
                    "redirect_url",
                    "#"
                )
            }
        )

    return jobs