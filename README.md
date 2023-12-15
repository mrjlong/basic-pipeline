# Basic Pipeline Project

## Overview
This project is an ETL pipeline that fetches, processes, and stores data from the Open Library API.

## Structure
- `src`: Source code for the project.
  - `api`: Module for API interactions.
  - `database`: (Future implementation) Database interactions.
  - `processing`: Data processing modules.
  - `utils`: Utility functions and configurations.
  - `main.py`: Main script to run the ETL job.
- `tests`: (Future implementation) Unit tests for the project.

## Setup
1. Install required Python packages: `pandas`, `requests`, etc.
2. Set up AWS credentials for accessing Parameter Store.
3. (Optional) Modify configurations as needed in the `config.json`.

## Running the Pipeline
Execute the pipeline by running `python src/main.py`.

## Dependencies
- Python 3.x
- Pandas
- Requests
- Boto3 (for AWS Parameter Store)

