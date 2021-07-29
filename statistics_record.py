class StatisticsRecord:
    def __init__(self) -> None:
        self.people_vaccinated_per_hundred = None
        self.people_fully_vaccinated_per_hundred = None
        self.total_boosters_per_hundred = None
        self.new_cases = None
        self.new_deaths = None
        self.hosp_patients = None
        self.icu_patients = None
        self.last_updated_date = None
        self.positive_rate = None
        self.reproduction_rate = None

    def is_vaccination_data_complete(self) -> bool:
        return (
            self.people_vaccinated_per_hundred
            and self.people_fully_vaccinated_per_hundred
            and self.total_boosters_per_hundred
        )
