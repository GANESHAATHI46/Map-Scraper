"""
REST API with interactive Swagger UI at /api/docs.
"""

import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse

import config
from schemas import Business, HealthResponse, ScrapeRequest, ScrapeResponse

app = FastAPI(
    title="Google Maps Scraper API",
    description=(
        "Extract business listings from Google Maps via Selenium and return them as JSON. "
        "Interactive docs: **Swagger UI** (`/api/docs`) and ReDoc (`/api/redoc`)."
    ),
    version="1.0.0",
    contact={"name": "Map-Scraper"},
    license_info={"name": "Educational use"},
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    tags_metadata=[
        {"name": "Health", "description": "Service availability"},
        {"name": "Scraper", "description": "Run a Maps search and download results"},
    ],
)


@app.get("/", include_in_schema=False)
@app.get("/docs", include_in_schema=False)
def swagger_redirect():
    return RedirectResponse(url="/api/docs")


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check",
)
def health():
    return HealthResponse(status="ok", service="google-maps-scraper")


@app.post(
    "/scrape",
    response_model=ScrapeResponse,
    tags=["Scraper"],
    summary="Scrape Google Maps listings",
    responses={
        400: {"description": "Invalid request or no results feed"},
        500: {"description": "Scraper or browser error"},
    },
)
def scrape(body: ScrapeRequest):
    """
    Opens Chrome, searches Google Maps for `keyword`, scrolls the results list,
    visits each listing, and returns structured business data.

    This call is **synchronous** and can take several minutes depending on
    `max_scrolls` and how many listings are found.
    """
    from excel import ExcelManager
    from scraper import BusinessScraper

    config.MAX_SCROLL = body.max_scrolls

    scraper = BusinessScraper(headless=body.headless)
    try:
        scraper.start()
        records = scraper.search(body.keyword)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    finally:
        scraper.close()

    excel_file = None
    if body.save_excel:
        excel = ExcelManager(config.OUTPUT_FILE)
        excel.save(records)
        excel_file = config.OUTPUT_FILE

    businesses = [Business.model_validate(row) for row in records]
    return ScrapeResponse(
        keyword=body.keyword,
        count=len(businesses),
        excel_file=excel_file,
        businesses=businesses,
    )


@app.get(
    "/export",
    tags=["Scraper"],
    summary="Download the last Excel export",
    responses={
        200: {
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {}
            }
        },
        404: {"description": "No Excel file has been generated yet"},
    },
)
def export_excel():
    path = config.OUTPUT_FILE
    if not os.path.isfile(path):
        raise HTTPException(
            status_code=404,
            detail="No Excel file found. Run POST /scrape with save_excel=true first.",
        )
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="google_maps_data.xlsx",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
