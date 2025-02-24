import os
import requests
import json
import argparse
from datetime import datetime
import csv

def get_api_credentials():
    """Get API credentials from environment variables or command line arguments"""
    parser = argparse.ArgumentParser(description='Cloud One Computer Management Script')
    parser.add_argument('--api-key', help='Cloud One API Key')
    parser.add_argument('--region', help='Cloud One Region (default: us-1)', default='us-1')
    parser.add_argument('--csv-file', help='Path to CSV file with computer metadata', default='computer_metadata.csv')
    
    args = parser.parse_args()
    
    # Check for API key in args first, then environment
    api_key = args.api_key or os.getenv('API_KEY')
    if not api_key:
        raise ValueError("API key must be provided either as --api-key argument or set as API_KEY environment variable")
    
    # Check for region in args first, then environment, then default
    region = args.region or os.getenv('REGION', 'us-1')
    
    return {
        'api_key': api_key,
        'region': region,
        'csv_file': args.csv_file
    }

def get_api_data(api_url, api_key=None):
    # Check if the API key is provided as a parameter, otherwise look for it in environment variables
    if api_key is None:
        api_key = os.getenv('API_KEY')
    
    if not api_key:
        raise ValueError("API key must be provided either as a parameter or set as an environment variable 'API_KEY'.")

    headers = {
        "api-version": "v1",
        "Content-Type": "application/json",
        "api-secret-key": api_key
    }

    try:
        print(f"Requesting URL: {api_url}")
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        # Parse the response
        data = response.json()
        
        # Extract computer IDs, hostnames, and display names
        computers_info = []
        for computer in data.get('computers', []):
            computers_info.append({
                'ID': computer.get('ID'),
                'hostName': computer.get('hostName'),
                'displayName': computer.get('displayName')
            })
        
        # Get current timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save the simplified data to a JSON file
        filename = f"computer_ids_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(computers_info, f, indent=4)
        print(f"Data saved to {filename}")
        
        # Print the information to console
        print("\nComputer Information:")
        for computer in computers_info:
            print(f"ID: {computer['ID']}, Hostname: {computer['hostName']}, Display Name: {computer['displayName']}")
        
        return computers_info
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_computer_data(api_url, api_key):
    """Get list of computers from Cloud One"""
    headers = {
        "api-version": "v1",
        "Content-Type": "application/json", 
        "api-secret-key": api_key
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json().get('computers', [])
    except requests.exceptions.RequestException as e:
        print(f"Error getting computer data: {e}")
        return None

def read_metadata_csv(csv_file):
    """Read computer metadata from CSV file"""
    computer_metadata = {}
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Use hostname as key and application_name as description
            computer_metadata[row['hostname']] = {
                'description': row['application_name']
            }
    return computer_metadata

def update_computer(computer_id, description, api_url, api_key):
    """Update single computer description"""
    headers = {
        "api-version": "v1",
        "Content-Type": "application/json",
        "api-secret-key": api_key
    }
    
    payload = {
        "description": description
    }
    
    update_url = f"{api_url}/{computer_id}"
    try:
        print(f"Updating computer ID {computer_id} with description: {description}")
        response = requests.post(update_url, headers=headers, json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error updating computer {computer_id}: {e}")
        return False

def main():
    try:
        # Get credentials and configuration
        credentials = get_api_credentials()
        
        # Set up API URL
        api_url = f"https://workload.{credentials['region']}.cloudone.trendmicro.com/api/computers"
        
        # Get current computer data
        computers = get_computer_data(api_url, credentials['api_key'])
        if not computers:
            return
        
        # Read metadata from CSV
        metadata = read_metadata_csv(credentials['csv_file'])
        
        # Match and update computers
        for computer in computers:
            hostname = computer.get('hostName')
            if hostname in metadata:
                print(f"Found matching computer {hostname} (ID: {computer['ID']})")
                success = update_computer(
                    computer['ID'],
                    metadata[hostname]['description'],
                    api_url,
                    credentials['api_key']
                )
                if success:
                    print(f"Successfully updated {hostname}")
                else:
                    print(f"Failed to update {hostname}")

    except Exception as e:
        print(f"An error occurred: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())