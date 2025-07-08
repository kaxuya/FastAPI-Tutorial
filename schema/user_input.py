from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from config.city_tier import tier_1_cities, tier_2_cities


# pydantic model to validate incoming data
class UserInput(BaseModel):
    age: Annotated[
        int, Field(..., gt=0, lt=120, description="Age of the user", examples=[28])
    ]
    weight: Annotated[
        float, Field(..., gt=0, description="Weight of the user in kg", examples=[85])
    ]
    height: Annotated[
        float,
        Field(
            ..., gt=0, lt=3, description="Height of the user in meters", examples=[1.75]
        ),
    ]
    income_lpa: Annotated[
        float,
        Field(
            ...,
            gt=0,
            description="Income of the user in lakhs per annum",
            examples=[24.6],
        ),
    ]
    smoker: Annotated[
        bool,
        Field(..., description="Is user a smoker", examples=["False"]),
    ]
    city: Annotated[
        str, Field(..., description="City of the user", examples=["Guwahati"])
    ]
    occupation: Annotated[
        Literal[
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job",
        ],
        Field(..., description="Occupation of the user", examples=["private_job"]),
    ]

    @field_validator("city")
    @classmethod
    def normalize_city(cls, v):
        return v.strip().title()

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height * self.height)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
