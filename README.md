# Vision One Workload Security Computer Management Script

This script interacts with Trend Micro's Vision One Workload Security API to manage computer descriptions. It retrieves computer information and updates computer descriptions based on metadata provided in a CSV file.

## Features

- Retrieves computer information from Vision One Workload Security
- Matches computers with metadata from a CSV file
- Updates computer descriptions via the Vision One Workload Security API
- Error handling and logging of operations
- Supports batch processing of multiple computers

## Prerequisites

- Python 3.10+ (recommended version, however any version that supports the requests library should work)
- Access to Vision One Workload Security
- Valid API Key with appropriate permissions
- Required Python packages:
  ```bash
  pip install requests
  ```

## Configuration

The script supports two methods for configuration:

### Environment Variables
```bash
export API_KEY="your-api-key-here"
export REGION="us-1"
```

### Command Line Arguments
```bash
python update_computer_description.py --api-key YOUR_API_KEY --region us-1 --csv-file path/to/metadata.csv
```

#### Available Arguments
- `--api-key`: Your Vision One Workload Security API key
- `--region`: Your Workload Security region (defaults to 'us-1')
- `--csv-file`: Path to your metadata CSV file (defaults to 'computer_metadata.csv')

## CSV File Format

The script expects a CSV file with the following format (see example CSV for reference):
```csv
hostname,application_name
dbserver02.example.com,Oracle Database (Finance)
appserver03.example.com,SAP ERP (Production)
```

### CSV Fields
- `hostname`: Must match the hostname in Vision One Workload Security
- `application_name`: Will be used as the description for the matching computer

### Example CSV

Attached is an example CSV that was used for testing purposes and as example of the expected format of data coming from another tool. This can be changed but this is the assumed format of the data.


## Usage

1. Prepare your computer metadata CSV file or generate a test file
2. Set your API key and region (via environment variables or command line) see above example of using command line arguments. This example below assumes the API key is set as an environment variable.
3. Run the script:
   ```bash
   python update_computer_description.py
   ```

The script will:
- Retrieve current computer information from Vision One Workload Security
- Read the metadata from your CSV file
- Match computers by hostname
- Update descriptions where matches are found
- Log the results of each update operation

## Output

The script provides:
- Console output showing matched computers and update status
- JSON file with current computer data (saved with timestamp)
- Success/failure messages for each update operation


## Error Handling

The script includes error handling for:
- API connection issues
- Invalid API responses
- CSV file reading errors
- Computer update failures

## API Documentation

For reference, the following API endpoints are used, below is the link to the API documentation for Vision One Workload Security.
- Search Computers: https://cloudone.trendmicro.com/docs/workload-security/api-reference/tag/Computers#operation/searchComputers
- Modify Computer: https://cloudone.trendmicro.com/docs/workload-security/api-reference/tag/Computers#operation/modifyComputer

## Notes

- Ensure your API key has appropriate permissions for reading and updating computers
- Back up your computer descriptions before running updates
- Test with a small subset of computers first
- The script only updates the description field