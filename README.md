# Google Maps Scraper

A robust, Python-based web scraper built with Selenium to extract detailed business information from Google Maps. It automates the process of searching for a keyword, scrolling through the results, and extracting comprehensive data for each listing before saving it to an Excel file.

## Features

- **Automated Navigation & Extraction:** Uses Selenium WebDriver to navigate Google Maps and extract business details.
- **Deep Data Parsing:** Extracts Business Name, Category, Rating, Total Reviews, Address, Phone Number, Website, and Latitude/Longitude coordinates.
- **Auto-Scroll Capability:** Automatically scrolls through the results pane to load and capture maximum listings.
- **Headless Mode:** Can be run in the background without launching a visible browser window.
- **Excel Export:** Cleans, formats, and saves all extracted data into a neat Excel (`.xlsx`) sheet using Pandas. 
- **Duplicate Prevention:** Automatically removes duplicate entries when saving data.
- **REST API + Swagger:** FastAPI service with interactive OpenAPI docs at `/api/docs`.

## Project Structure

- `main.py`: The entry point of the application. It initializes the scraper, starts the search, and saves the data.
- `app.py`: Streamlit web UI for running a scrape from the browser.
- `api.py`: FastAPI REST API (Swagger UI at `/api/docs`, ReDoc at `/api/redoc`).
- `schemas.py`: Request and response models used by the API / OpenAPI spec.
- `scraper.py`: Contains the `BusinessScraper` class responsible for browser automation, scrolling, and extracting raw DOM elements.
- `parser.py`: Contains the `BusinessParser` utility class that cleans text and uses Regular Expressions to parse raw strings into actionable data (like extracting lat/long from a URL).
- `excel.py`: Contains the `ExcelManager` class which uses Pandas to store and append data to an Excel file.
- `config.py`: Centralized configuration file for easily tweaking scraper settings.
- `requirements.txt`: Python dependencies.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/GANESHAATHI46/Map-Scraper.git
   cd Map-Scraper/google_maps_scraper
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Ensure you have Google Chrome installed on your machine. The `webdriver-manager` package will automatically handle downloading the correct ChromeDriver version.*

## Configuration

Before running the script, you can adjust the settings in `config.py`:

```python
# Search keyword
SEARCH_KEYWORD = "barber shops in Dindigul"

# Browser Settings (True to hide browser, False to show it)
HEADLESS = False

# Number of scrolls to load more results
MAX_SCROLL = 50

# Output Excel file path
OUTPUT_FILE = "data/google_maps.xlsx"
```

## Usage

### CLI

Run the main script to start scraping:

```bash
python main.py
```

The script will:
1. Open Google Chrome.
2. Search for the keyword defined in `config.py`.
3. Scroll down the left panel to load more results.
4. Extract the details of each found business.
5. Save the output to `data/google_maps.xlsx`.

### REST API (Swagger)

Install dependencies, then start the API:

```bash
pip install -r requirements.txt
python api.py
```

Or:

```bash
uvicorn main:app --reload
```

Then open:

- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc
- **OpenAPI JSON:** http://localhost:8000/api/openapi.json

http://localhost:8000/ and `/docs` redirect to Swagger.

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/scrape` | Run a Maps scrape and return JSON |
| `GET` | `/export` | Download the last Excel file |

`POST /scrape` example body:

```json
{
  "keyword": "barber shops in Dindigul",
  "max_scrolls": 10,
  "headless": true,
  "save_excel": true
}
```

This request is synchronous and can take several minutes.

### Streamlit UI

```bash
streamlit run app.py
```

## Data Output

The generated Excel file will contain the following columns:
- Business Name
- Category
- Rating
- Reviews
- Address
- Phone
- Website
- Working Hours (if applicable)
- Latitude
- Longitude
- Maps URL

## Disclaimer

This scraper is for educational purposes. Web scraping Google Maps may violate Google's Terms of Service. Please use responsibly, adhere to rate limits, and respect the data privacy guidelines of your region.
