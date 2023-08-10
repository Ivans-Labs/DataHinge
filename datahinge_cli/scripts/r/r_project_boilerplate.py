"""
Module Name: r_project_boilerplate

Description: This module generates boilerplate code for a data science project in R.

Author: Sudo-Ivan
"""

import os
import argparse
import sys

def create_project(project_name, code_type):
    """Generate boilerplate code for a data science project in R."""

    # Mapping of code types to scripts
    scripts = {
        "datascience": {
            "script_name": "example.R",
            "script_content": """
# Example R script for data science
library(tidyverse)

# TODO: Load data
data <- read.csv("path/to/data.csv")

# TODO: Preprocess data
data_cleaned <- data %>%
  # Data cleaning operations...

# TODO: Perform analysis
# Analysis code goes here...

# TODO: Generate results
# Result generation code goes here...
"""
        },
        "datacleaning": {
            "script_name": "data_cleaning.R",
            "script_content": """
# Data cleaning script
library(tidyverse)

# TODO: Load data
data <- read.csv("path/to/data.csv")

# TODO: Clean data
data_cleaned <- data %>%
  # Data cleaning operations...

# TODO: Handle missing values
# Missing value handling code goes here...

# TODO: Transform data
# Data transformation code goes here...

# TODO: Save cleaned data
write.csv(data_cleaned, "path/to/cleaned_data.csv", row.names = FALSE)
"""
        },
        "graphing": {
            "script_name": "graphing.R",
            "script_content": """
# Graphing script
library(ggplot2)

# TODO: Load data
data <- read.csv("path/to/data.csv")

# TODO: Prepare data for visualization
# Data preprocessing for visualization goes here...

# TODO: Create plots and visualizations
# Plotting code using ggplot2 goes here...

# TODO: Save visualizations
# Saving visualizations to files goes here...
"""
        }
    }

    if code_type not in scripts:
        print(f"Error: Invalid code type '{code_type}'. Available code types: {', '.join(scripts.keys())}")
        sys.exit(1)

    # Create the project directory
    project_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_dir, exist_ok=True)

    # Generate the project structure
    r_scripts_dir = os.path.join(project_dir, "scripts")
    os.makedirs(r_scripts_dir, exist_ok=True)

    data_dir = os.path.join(project_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    report_dir = os.path.join(project_dir, "reports")
    os.makedirs(report_dir, exist_ok=True)

    # Create the specified code type script
    script_name = scripts[code_type]["script_name"]
    script_content = scripts[code_type]["script_content"]
    script_path = os.path.join(r_scripts_dir, script_name)

    with open(script_path, "w") as f:
        f.write(script_content)

    print(f"Boilerplate code for the project '{project_name}' with code type '{code_type}' has been generated.")

def main(args):
    """Main function to handle command-line arguments and call appropriate functions."""
    parser = argparse.ArgumentParser(description="Generate boilerplate code for a data science project in R.")
    parser.add_argument("project_name", type=str, help="Name of the project")
    parser.add_argument("code_type", type=str, choices=["datascience", "datacleaning", "graphing"], help="Type of boilerplate code to generate")
    parsed_args = parser.parse_args(args)

    try:
        create_project(parsed_args.project_name, parsed_args.code_type)
    except OSError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])