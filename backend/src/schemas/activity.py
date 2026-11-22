from datetime import date as DateType

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ActivityBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1, max_length=450)
    date: DateType
    image_url: str | None = None
    slug: str = Field(min_length=1, max_length=200, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    sent: bool = False


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1, max_length=450)
    date: DateType | None = None
    image_url: str | None = None
    slug: str | None = Field(default=None, min_length=1, max_length=200, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    sent: bool | None = None

    @model_validator(mode="after")
    def reject_null_required_fields(self):
        for field in self.model_fields_set - {"image_url"}:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class ActivityRead(BaseModel):
    id: int
    title: str
    description: str
    date: DateType
    image_url: str | None = None
    slug: str
    sent: bool
    model_config = ConfigDict(from_attributes=True)
