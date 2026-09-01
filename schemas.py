"""
Pydantic models for the REST API (OpenAPI / Swagger).
"""

from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class ScrapeRequest(BaseModel):
    keyword: str = Field(
        ...,
        min_length=1,
        description="Google Maps search query",
        examples=["barber shops in Dindigul"],
    )
    max_scrolls: int = Field(
        default=50,
        ge=1,
        le=100,
        description="How many times to scroll the results feed to load more listings",
    )
    headless: bool = Field(
        default=True,
        description="Run Chrome without a visible window",
    )
    save_excel: bool = Field(
        default=True,
        description="Write results to the configured Excel output file",
    )


class Business(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    business_name: str = Field(default="", alias="Business Name")
    category: str = Field(default="", alias="Category")
    rating: Union[float, str] = Field(default="", alias="Rating")
    reviews: Union[int, str] = Field(default="", alias="Reviews")
    address: str = Field(default="", alias="Address")
    phone: str = Field(default="", alias="Phone")
    website: str = Field(default="", alias="Website")
    working_hours: str = Field(default="", alias="Working Hours")
    latitude: str = Field(default="", alias="Latitude")
    longitude: str = Field(default="", alias="Longitude")
    maps_url: str = Field(default="", alias="Maps URL")


class ScrapeResponse(BaseModel):
    keyword: str
    count: int
    excel_file: Optional[str] = Field(
        default=None,
        description="Path of the saved Excel file, if save_excel was true",
    )
    businesses: List[Business]


class HealthResponse(BaseModel):
    status: str
    service: str
