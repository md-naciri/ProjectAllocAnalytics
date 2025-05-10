# Project Allocation Analytics

A Python application that analyzes resource allocation data and generates detailed resource summaries from Excel files. This tool helps in tracking project resource allocation, calculating theoretical charges, and identifying variances in resource utilization.

## Features

- Excel-based resource allocation analysis
- Automatic calculation of person-days (JH) from submitted hours
- Project connection level and phase consideration
- Theoretical charge calculations
- Variance analysis between actual and theoretical charges
- Interactive command-line interface
- Automated Excel report generation
- One-click output file opening

## Prerequisites

- Python 3.12 or higher
- Required Python packages:
  - pandas
  - openpyxl

## Installation

1. Clone or download this repository to your local machine
2. Install the required Python packages:

```powershell
pip install pandas openpyxl
```

## Usage

1. Run the application:
```powershell
python main.py
```

2. When prompted:
   - Provide the path to your resource data Excel file
   - Provide the path to your deployments Excel file
   - Optionally specify a custom output file location
   - Choose whether to automatically open the generated report

## Input File Requirements

### Resource Data File
Must include these columns:
- `Ressource`: Name of the resource/person
- `Projet`: Project name
- `Soumise (h)`: Hours submitted

### Deployments File
Must include these columns:
- `Nom`: Project name
- `Niveau de connexion`: Connection level for the project
- `Phase du projet`: Current project phase

## Output

The application generates an Excel file containing:
- Resource and project hierarchical view
- Actual charge in person-days (calculated as hours/8)
- Project connection levels and phases
- Theoretical charge calculations
- Variance analysis with formatting:
  - Positive variances (where actual < theoretical)
  - Negative variances (where actual > theoretical)

## Project Structure

```
ProjectAllocAnalytics/
├── main.py                  # Main application entry point
├── config/
│   └── rules.py            # Configuration for theoretical charge rules
├── core/
│   ├── data_processor.py   # Data processing and calculations
│   └── excel_handler.py    # Excel file operations
└── utils/
    └── helpers.py          # Utility functions for file handling
```

## Error Handling

- Validates required columns in input files
- Provides clear error messages for missing data
- Handles file path validation
- Includes detailed error traceback for troubleshooting
