# excel.py
"""
excel.py
--------------------------
Handles saving business data to Excel.
"""

import os
import pandas as pd


class ExcelManager:

    def __init__(self, output_file):
        self.output_file = output_file

        # Create output directory if it doesn't exist
        folder = os.path.dirname(output_file)

        if folder and not os.path.exists(folder):
            os.makedirs(folder)

    def save(self, businesses):
        """
        Save list of business dictionaries to Excel.

        Example:
        [
            {
                "Business Name": "Hotel ABC",
                "Category": "Hotel",
                "Rating": "4.5",
                ...
            }
        ]
        """

        if not businesses:
            print("No data available.")
            return

        df = pd.DataFrame(businesses)

        df.to_excel(
            self.output_file,
            index=False
        )

        print(f"\nSaved {len(df)} records")
        print(f"Excel File : {self.output_file}")

    def append(self, businesses):
        """
        Append new data if Excel already exists.
        """

        if not businesses:
            return

        new_df = pd.DataFrame(businesses)

        if os.path.exists(self.output_file):

            old_df = pd.read_excel(self.output_file)

            final_df = pd.concat(
                [old_df, new_df],
                ignore_index=True
            )

            # Remove duplicate rows
            final_df.drop_duplicates(inplace=True)

        else:
            final_df = new_df

        final_df.to_excel(
            self.output_file,
            index=False
        )

        print(f"Total Records : {len(final_df)}")