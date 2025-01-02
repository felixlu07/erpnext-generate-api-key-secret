# ERPNext API Key Generator

This project automates the process of generating API keys and secrets for multiple ERPNext instances.

## Features
- Bulk generation of API keys and secrets for multiple ERPNext sites
- CSV-based input and output for easy management
- Automatic login and key generation
- Verification script to test generated keys

## Prerequisites
- Python 3.8 or higher
- Access to ERPNext instances with administrator privileges
- Input CSV file with site credentials

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd erpnext-generate-api-key-secret
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Create a CSV file named `creds.csv` with the following columns:
   - siteurl
   - username
   - password

   See `sample_creds.csv` for the expected format:
   ```csv
   siteurl,username,password
   demo.erpnext.example.com,administrator,dummy_password123
   test.erpnext.example.com,admin,sample_password456
   staging.erpnext.example.com,Administrator,test_password789
   ```

2. Run the key generation script:
```bash
python generate_keys.py
```

3. To verify the generated keys, run:
```bash
python test_api_keys.py
```

The script will create a new file `creds_updated.csv` containing the generated API keys and secrets.

## Security Notes
- The input and output CSV files containing credentials are automatically ignored by git
- Never commit credentials or API keys to the repository
- Always use HTTPS for API requests in production

## Project Structure
- `generate_keys.py`: Main script for generating API keys
- `test_api_keys.py`: Script to verify generated keys by creating test customers
- `requirements.txt`: Python package dependencies
- `sample_creds.csv`: Example CSV file showing the required format

## API Endpoints Used
- `/api/method/login`: Authentication
- `/api/method/frappe.core.doctype.user.user.generate_keys`: Key generation
- `/api/method/frappe.auth.get_logged_user`: User verification
- `/api/resource/User/{username}`: User details retrieval

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
