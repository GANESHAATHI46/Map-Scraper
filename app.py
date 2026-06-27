import streamlit as st
import pandas as pd
import os
from scraper import BusinessScraper
from excel import ExcelManager
import config

# Set page layout and title
st.set_page_config(page_title="Google Maps Scraper", page_icon="📍", layout="centered")
st.title("📍 Google Maps Business Scraper")
st.write("Extract business listings directly to Excel using a clean web interface.")

# UI Form for User Inputs
with st.form("scraper_form"):
    search_keyword = st.text_input("Search Keyword", value=config.SEARCH_KEYWORD)
    max_scrolls = st.slider("Max Scrolls (Pagination)", min_value=5, max_value=100, value=config.MAX_SCROLL)
    headless_mode = st.checkbox("Run in Background (Headless Mode)", value=config.HEADLESS)
    
    submitted = st.form_submit_button("Start Scraping")

# Execution Logic
if submitted:
    if not search_keyword:
        st.error("Please enter a search keyword.")
    else:
        st.info(f"Starting scraper for: **{search_keyword}**...")
        
        # Override config with UI inputs
        config.MAX_SCROLL = max_scrolls
        
        # Initialize Scraper
        scraper = BusinessScraper(headless=headless_mode)
        try:
            with st.spinner('Navigating Google Maps and extracting data... This may take a moment.'):
                scraper.start()
                businesses = scraper.search(search_keyword)
                
            if businesses:
                st.success(f"Successfully scraped {len(businesses)} businesses!")
                
                # Save Data
                excel = ExcelManager(config.OUTPUT_FILE)
                excel.save(businesses)
                
                # Display a preview of the data in the UI
                df = pd.DataFrame(businesses)
                st.dataframe(df)
                
                # Provide a download button for the Excel file
                with open(config.OUTPUT_FILE, "rb") as file:
                    st.download_button(
                        label="Download Excel File",
                        data=file,
                        file_name="google_maps_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.warning("No businesses found. Try adjusting your keyword or scroll limits.")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            scraper.close()