from typing import Dict
import requests
import logging
from datetime import datetime, timedelta
from config import CASES_DATA_URL, VAX_DATA_URL
from statistics_record import StatisticsRecord

log = logging.getLogger(__name__)


def retrieve_latest_cases_stats() -> StatisticsRecord:
    response = requests.get(CASES_DATA_URL)

    if response.status_code != 200:
        log.error(
            "Invalid response [{}] retrieving data: {}".format(
                response.status_code, response.text
            )
        )

        return None

    data = response.json()
    cases_data = data["PRT"]

    response = requests.get(VAX_DATA_URL)

    if response.status_code != 200:
        log.error(
            "Invalid response [{}] retrieving data: {}".format(
                response.status_code, response.text
            )
        )

        return None

    data = response.json()

    for record in data:
        if record["country"] == "Portugal":
            pt_data = record
            break

    if not pt_data:
        return None

    vaccinations_data = parse_country_data(pt_data["data"])

    return generate_record(vaccinations_data, cases_data)


def generate_record(
    vaccinations_data: Dict[str, object], cases_data: object
) -> StatisticsRecord:
    dataset = StatisticsRecord()
    date_ptr = datetime.now()

    log.info("Generating record...")

    # Vaccination records.
    while not dataset.is_vaccination_data_complete():
        day_entry = vaccinations_data.get(date_ptr.strftime("%Y-%m-%d"))

        date_ptr = date_ptr - timedelta(days=1)

        if not day_entry:
            continue

        if "people_vaccinated_per_hundred" in day_entry:
            dataset.people_vaccinated_per_hundred = day_entry[
                "people_vaccinated_per_hundred"
            ]

        if "people_fully_vaccinated_per_hundred" in day_entry:
            dataset.people_fully_vaccinated_per_hundred = day_entry[
                "people_fully_vaccinated_per_hundred"
            ]

        if "total_boosters_per_hundred" in day_entry:
            dataset.total_boosters_per_hundred = day_entry["total_boosters_per_hundred"]

    # Cases data
    dataset.new_cases = cases_data["new_cases"]
    dataset.new_deaths = cases_data["new_deaths"]
    dataset.hosp_patients = cases_data["hosp_patients"]
    dataset.icu_patients = cases_data["icu_patients"]
    dataset.reproduction_rate = cases_data["reproduction_rate"]
    dataset.positive_rate = cases_data["positive_rate"]

    dataset.last_updated_date = cases_data["last_updated_date"]

    return dataset


def parse_country_data(country_data) -> Dict[str, object]:
    """Creates a dictionary of the country indexed by date."""
    log.info("Parsing country data")
    return {record["date"]: record for record in country_data}
