import pandas as pd
import requests
import json
from datetime import datetime
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def format_site_url(url):
    """Ensure URL has https:// prefix and no trailing slash"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url.rstrip('/')

def test_api_key(site_url, api_key, api_secret):
    """Test API key by creating a test customer"""
    base_url = format_site_url(site_url)
    
    # Generate a unique customer name using timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    customer_name = f"Test Customer {timestamp}"
    
    # Prepare headers with API authentication
    headers = {
        'Authorization': f'token {api_key}:{api_secret}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Prepare customer data
    customer_data = {
        "doctype": "Customer",
        "customer_name": customer_name,
        "customer_type": "Individual",
        "customer_group": "All Customer Groups",
        "territory": "All Territories"
    }
    
    try:
        # Create customer using API
        create_url = f"{base_url}/api/resource/Customer"
        response = requests.post(
            create_url,
            headers=headers,
            data=json.dumps(customer_data),
            verify=False
        )
        
        print(f"\nTesting API key for {site_url}")
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 200:
            print(f"Success! Created customer: {customer_name}")
            
            # Try to fetch the created customer
            customer_name = response.json()['data']['name']
            get_url = f"{base_url}/api/resource/Customer/{customer_name}"
            get_response = requests.get(
                get_url,
                headers=headers,
                verify=False
            )
            
            if get_response.status_code == 200:
                print(f"Successfully retrieved created customer")
                return True
            else:
                print(f"Failed to retrieve created customer")
                return False
        else:
            print(f"Failed to create customer")
            return False
            
    except Exception as e:
        print(f"Error testing API key: {str(e)}")
        return False

def main():
    # Read the CSV file
    df = pd.read_csv('creds_updated.csv', dtype=str)
    
    # Test first 3 sites
    results = []
    for index in range(min(3, len(df))):
        row = df.iloc[index]
        success = test_api_key(
            row['siteurl'],
            row['api_key'],
            row['api_secret']
        )
        results.append({
            'site': row['siteurl'],
            'success': success
        })
    
    # Print summary
    print("\n=== Test Results Summary ===")
    for result in results:
        status = "Passed" if result['success'] else "Failed"
        print(f"{result['site']}: {status}")

if __name__ == "__main__":
    main()
