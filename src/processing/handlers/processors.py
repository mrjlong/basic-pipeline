import os
import pandas as pd
import json
import boto3


def dataframe_to_csv(dataframe, file_name, columns=None, save_to_s3=False, s3_bucket='jlong-simple-etl'):
    if columns is not None:
        dataframe = dataframe[columns]
    
    output_dir = 'data-output'
    os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist
    file_path = os.path.join(output_dir, file_name)

    try:
        # Write DataFrame to CSV
        dataframe.to_csv(file_path, index=False)
        print(f"Data successfully written to {file_path}")

        if save_to_s3:
            # Upload to S3
            s3 = boto3.client('s3')
            s3.upload_file(file_path, s3_bucket, file_name)
            print(f"File successfully uploaded to S3 bucket '{s3_bucket}'")

    except Exception as e:
        print(f"An error occurred: {e}")





def read_config():
    config_path = 'processing/config/config.json'
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            return config.get('dataframe_columns', {}).get('include', [])
    except FileNotFoundError:
        print(f"Config file not found at {config_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error parsing the config file at {config_path}")
        return []



def convert_to_dataframe(works):
    included_columns = read_config()
    processed_data = []

    for work in works:
        work_data = work.copy()

        # Handling the list of authors
        if 'authors' in work_data:
            work_data['author_keys'] = ', '.join([author.get('key', '') for author in work_data['authors']])
            work_data['author_names'] = ', '.join([author.get('name', '') for author in work_data['authors']])
            del work_data['authors']  # Removing the original 'authors' field

        # Handling other list fields like 'subject' and 'ia_collection'
        for list_field in ['subject', 'ia_collection']:
            if list_field in work_data:
                work_data[list_field] = ', '.join(work_data[list_field])

        # Handling nested dictionary fields like 'availability'
        if 'availability' in work_data:
            for key, value in work_data['availability'].items():
                work_data[f'availability_{key}'] = value
            del work_data['availability']  # Removing the original 'availability' field

        processed_data.append(work_data)

    df = pd.DataFrame(processed_data)

    # Filter the DataFrame based on the included columns from the config
    if included_columns:
        df = df[included_columns]
    
    return df



def save_as_json(data, filename="sports_data_2.json"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"An error occurred while writing to file: {e}")