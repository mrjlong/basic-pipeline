import logging
from api.api_handler import fetch_subject_data
from processing.handlers.processors import *
from processing.aggs.calc_handler import *
#from .database.snowflake_connector import send_data_to_snowflake
#from database.databricks_connector import send_data_to_databricks
from utils.config import *  # If using the utils module
from tests.test_dblogin import *


# Constants - for testing purposes to limit the number of calls
#TOTAL_BATCHES = 3



def main():
    setup_logging()
    initialize_aws_profile()
    add_project_path()
    config = read_config()
    offset = config['offset']
    all_works = []

    logging.info("Starting data fetch process...")
    batch_count = 0
    while True:
        works = fetch_subject_data(config, offset)
        if not works:  # Break the loop if no data is returned
            break
    
        batch_count += 1
        logging.info(f"Batch {batch_count} fetched, processing...")
        all_works.extend(works)
        offset += config['limit']

    logging.info("Data fetch process completed. Starting data conversion...")

    # Process your 'all_works' data here
    my_df = convert_to_dataframe(all_works)

    logging.info("Data conversion completed. Starting CSV export...")

    # Exporting data to CSV locally and to s3
    dataframe_to_csv(my_df, 'authors', ['author_names'], save_to_s3=True)
    dataframe_to_csv(my_df, 'books', ['title'], save_to_s3=True)
    dataframe_to_csv(my_df, 'books_and_authors',['title','author_names'], save_to_s3=True)
    dataframe_to_csv(average_books_per_year_by_author(my_df), 'avg_per_year', save_to_s3=True)
    dataframe_to_csv(books_per_year_by_author(my_df), 'count_per_year', save_to_s3=True)

    logging.info("CSV export completed.")

    # Test retrieval of Snowflake credentials
    test_ssm_parameters()


    # Test connection to Snowflake
        # Code to add data to a Snowflake table

if __name__ == "__main__":
    main()