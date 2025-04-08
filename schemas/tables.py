from pydantic import BaseModel, Field, ConfigDict

class BaseTable(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IDTable(BaseTable):
    id: int = Field(description="ID столика")


class InfoTable(IDTable):
    name: str = Field(description="Название столика", examples=["Table 1"])
    seats: int = Field(description="Кол-во место", gt=0, examples=[2])
    location: str = Field(description="Местоположение столика", examples=["зал у окна", "терраса"])

class CreateTable(BaseTable):
    name: str = Field(description="Название столика", examples=["Table 1"])
    seats: int = Field(description="Кол-во место", gt=0, examples=[2])
    location: str = Field(description="Местоположение столика", examples=["зал у окна", "терраса"])
