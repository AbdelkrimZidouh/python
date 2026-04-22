from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime = Field(...)
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    try:
        station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.fromisoformat("2024-01-15T10:30:00"),
            is_operational=True,
            notes="All systems nominal"
        )
        print("Valid station created:")
        print(f"ID: {station.station_id}")
        print(f"Name: {station.name}")
        print(f"Crew: {station.crew_size} people")
        print(f"Power: {station.power_level}%")
        print(f"Oxygen: {station.oxygen_level}%")
        print(
            f"  Status: "
            f"{'Operational' if station.is_operational else 'Offline'}"
        )
        print()
    except ValidationError as e:
        print(f"Unexpected error: {e}")

    print("=" * 40)
    print("Expected validation error:")

    try:
        invalid_station = SpaceStation(
            station_id="BAD001",
            name="Overcrewed Station",
            crew_size=25,  # Invalid!
            power_level=90.0,
            oxygen_level=95.0,
            last_maintenance=datetime.fromisoformat("2024-01-15T10:30:00")
        )
        print(f"ERROR: Should have failed but got: {invalid_station}")
    except ValidationError as e:
        for error in e.errors():
            if error['loc'] == ('crew_size',):
                print(f"{error['msg']}")


if __name__ == "__main__":
    main()
