import requests

def fetch_subject_data(config, offset):
    url = f"{config['base_url']}{config['subject']}.json"
    params = {
        'limit': config['limit'],
        'offset': offset,
        'details': str(config['details']).lower()
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        # Extracting only the 'works' key from the response
        return response.json().get('works', [])
    else:
        print(f"Failed to retrieve data: Status code {response.status_code}")
        return []