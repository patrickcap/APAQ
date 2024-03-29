from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from src.types import Airport


@dataclass
class DataConverter:
    raw_data: dict[str, list[Airport]]
    airports_df: pd.DataFrame = field(init=False)
    runways: pd.DataFrame = field(init=False)
    flights: pd.DataFrame = field(init=False)
    air_quality: pd.DataFrame = field(init=False)

    def __post_init__(self) -> None:
        self.airports_df = pd.DataFrame(self.raw_data['airports'])
        self.flights = self.airports_df[['flights']]
        self.runways = self.airports_df[['runways']]
        self.air_quality = self.airports_df[['air_quality']]
        self.airports_df = self.airports_df.drop(['flights', 'runways'], axis=1)

    def save_runways_to_csv(self, path: str) -> None:
        self.runways.to_csv(Path(path) / 'runways.csv', sep=',', index=False, encoding='utf-8')

    def save_flights_to_csv(self, path: str) -> None:
        self.flights.to_csv(Path(path) / 'flights.csv', sep=',', index=False, encoding='utf-8')

    def save_aq_to_csv(self, path: str) -> None:
        self.air_quality.to_csv(Path(path) / 'aq.csv', sep=',', index=False, encoding='utf-8')

    def save_airports_to_csv(self, path: str) -> None:
        self.airports_df.to_csv(Path(path) / 'airports.csv', sep=',', index=False, encoding='utf-8')
