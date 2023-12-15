import boto3
from utils.config import get_snowflake_credentials

def test_ssm_parameters():
    try:
        # Fetch credentials
        credentials = get_snowflake_credentials()
        
        # Test: Check if credentials are retrieved
        # Note: Avoid printing sensitive data like passwords
        if all(credentials.values()):
            print("Successfully retrieved credentials from Parameter Store.")
            print(f"User: {credentials['user']}")
            print(f"Account: {credentials['account']}")
            # Add more print statements as necessary but avoid printing the password
        else:
            print("Failed to retrieve some or all credentials.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_ssm_parameters()
