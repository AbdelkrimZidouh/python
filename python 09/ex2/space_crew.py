from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank = Field(...)
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime = Field(...)
    duration_days: int = Field(..., ge=1, le=3650)
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_mission_rules(self) -> 'SpaceMission':
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_leader = any(
            member.rank in [Rank.commander, Rank.captain]
            for member in self.crew
        )
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced_count = sum(
                1 for member in self.crew
                if member.years_experience >= 5
            )
            required_experienced = len(self.crew) * 0.5
            if experienced_count < required_experienced:
                raise ValueError(
                    f"Long missions (>{365} days) need at least 50% "
                    f"experienced crew (5+ years). "
                    f"Got {experienced_count}/{len(self.crew)}"
                )

        inactive_members = [
            member.name for member in self.crew
            if not member.is_active
        ]
        if inactive_members:
            raise ValueError(
                f"All crew members must be active. "
                f"Inactive: {', '.join(inactive_members)}"
            )

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 40)

    try:
        crew = [
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.commander,
                age=45,
                specialization="Mission Command",
                years_experience=20,
                is_active=True
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.lieutenant,
                age=38,
                specialization="Navigation",
                years_experience=12,
                is_active=True
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.officer,
                age=32,
                specialization="Engineering",
                years_experience=8,
                is_active=True
            )
        ]

        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.fromisoformat("2025-06-01T09:00:00"),
            duration_days=900,
            crew=crew,
            mission_status="planned",
            budget_millions=2500.0
        )

        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
        print("Crew members:")
        for member in mission.crew:
            print(f"- {member.name} ({member.rank.value}) - "
                  f"{member.specialization}")
        print()
    except ValidationError as e:
        print(f"Unexpected error: {e}")

    print("=" * 40)
    print("Expected validation error:")

    try:
        invalid_crew = [
            CrewMember(
                member_id="CM004",
                name="Bob Builder",
                rank=Rank.officer,
                age=30,
                specialization="Construction",
                years_experience=5,
                is_active=True
            )
        ]

        invalid_mission = SpaceMission(
            mission_id="M2024_FAIL",
            mission_name="Failed Mission",
            destination="Moon",
            launch_date=datetime.fromisoformat("2025-01-01T00:00:00"),
            duration_days=30,
            crew=invalid_crew,
            budget_millions=100.0
        )
        print(f"ERROR: Should have failed but got: {invalid_mission}")
    except ValidationError as e:
        for error in e.errors():
            msg = error['msg']
            if msg.startswith("Value error, "):
                msg = msg.replace("Value error, ", "")
            print(msg)


if __name__ == "__main__":
    main()
