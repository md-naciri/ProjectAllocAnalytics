import os
import sys
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

# Add project root to sys.path to allow importing from project modules
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from core.excel_handler import ExcelHandler
from core.data_processor import DataProcessor
from utils.helpers import get_user_file_path, get_default_output_path


def main():
    """Main entry point for the application."""
    print("\nExcel Resource Summary Generator")
    print("===============================")

    try:
        # Get input file path from user
        input_file = get_user_file_path("\nEnter the path to your Excel file with resource data: ")

        # Get deployments file path from user
        deployments_file = get_user_file_path("\nEnter the path to your deployments Excel file: ")

        # Read the input Excel files
        print(f"\nReading data from '{input_file}'...")
        df = ExcelHandler.read_excel(input_file)

        print(f"Reading deployments data from '{deployments_file}'...")
        deployments_df = ExcelHandler.read_excel(deployments_file)

        # Validate the required columns
        print("Validating input data...")
        required_columns = ['Ressource', 'Projet', 'Soumise (h)']
        is_valid, missing_columns = DataProcessor.validate_dataframe(df, required_columns)

        if not is_valid:
            print(f"Error: The following required columns are missing: {missing_columns}")
            print(f"Available columns: {df.columns.tolist()}")
            return

        # Fix column names if needed (Resource vs Ressource)
        if 'Ressource' not in df.columns and 'Resource' in df.columns:
            df.rename(columns={'Resource': 'Ressource'}, inplace=True)

        # Create lookup dictionaries
        print("Creating lookup tables for project information...")
        connection_dict = DataProcessor.create_connection_dict(deployments_df, 'Niveau de connexion')
        phase_dict = DataProcessor.create_connection_dict(deployments_df, 'Phase du projet')

        # Calculate Charge JH
        print("Calculating 'Charge JH' (Soumise (h) / 8)...")
        df = DataProcessor.calculate_charge_jh(df)

        # Create pivot table
        print("Creating pivot table...")
        pivot_df = ExcelHandler.create_pivot_table(df, 'Charge JH', ['Ressource', 'Projet'])

        # Format the resource summary with theoretical charge
        print("Formatting output data and calculating theoretical charges...")
        result_df = DataProcessor.format_resource_summary(pivot_df, connection_dict, phase_dict)

        # Get output file path
        default_output = get_default_output_path(input_file, "_resource_summary")
        output_file = get_user_file_path(
            f"\nEnter the path for the output file (or press Enter for default: {default_output}): ",
            must_exist=False
        )

        if not output_file.strip():
            output_file = default_output

        # Write to Excel
        print(f"\nWriting results to '{output_file}'...")
        ExcelHandler.write_excel(result_df, output_file, 'Resource Summary')

        print(f"\nSuccess! Results saved to {output_file}")

        # Ask if user wants to open the output file
        open_file = input("\nDo you want to open the output file? (y/n): ").lower()
        if open_file.startswith('y'):
            print("Opening output file...")
            ExcelHandler.open_file(output_file)

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()