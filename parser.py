# parser.py
"""
parser.py
--------------------------------
Utility functions for parsing and cleaning
business information extracted from webpages.
"""

import re


class BusinessParser:

    @staticmethod
    def clean_text(text):
        """
        Remove extra spaces and line breaks.
        """
        if not text:
            return ""

        return " ".join(text.split())


    @staticmethod
    def parse_rating(text):
        """
        Examples:
            "4.5 stars"
            "Rated 4.3 out of 5"

        Returns:
            4.5
        """

        if not text:
            return ""

        match = re.search(r"\d+(\.\d+)?", text)

        if match:
            return float(match.group())

        return ""


    @staticmethod
    def parse_reviews(text):
        """
        Examples:
            "(1,245)"
            "1,245 reviews"

        Returns:
            1245
        """

        if not text:
            return ""

        numbers = re.findall(r"\d+", text.replace(",", ""))

        if numbers:
            return int("".join(numbers))

        return ""


    @staticmethod
    def parse_phone(text):
        """
        Keep only digits and '+'.
        """

        if not text:
            return ""

        return re.sub(r"[^\d+]", "", text)


    @staticmethod
    def parse_lat_long(url):
        """
        Extract latitude and longitude from a URL.

        Example:
        https://example.com/@10.3624,77.9695,17z
        """

        if not url:
            return "", ""

        match = re.search(
            r'@(-?\d+\.\d+),(-?\d+\.\d+)',
            url
        )

        if match:
            return match.group(1), match.group(2)

        return "", ""


    @staticmethod
    def build_record(
        name="",
        category="",
        rating="",
        reviews="",
        address="",
        phone="",
        website="",
        hours="",
        latitude="",
        longitude="",
        maps_url=""
    ):
        """
        Return a standard business dictionary.
        """

        return {
            "Business Name": name,
            "Category": category,
            "Rating": rating,
            "Reviews": reviews,
            "Address": address,
            "Phone": phone,
            "Website": website,
            "Working Hours": hours,
            "Latitude": latitude,
            "Longitude": longitude,
            "Maps URL": maps_url
        }