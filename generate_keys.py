import pandas as pd
import requests
import urllib3
from urllib.parse import urlparse
import time

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def format_site_url(url):
    """Ensure URL has https:// prefix and no trailing slash"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url.rstrip('/')

def login_and_generate_keys(site_url, username, password):
    """Login to ERPNext site and generate API key and secret"""
    session = requests.Session()
    
    # Format the URL
    base_url = format_site_url(site_url)
    
    try:
        # Login
        login_url = f"{base_url}/api/method/login"
        print(f"Attempting login to {login_url}")
        login_response = session.post(
            login_url,
            data={
                'usr': username,
                'pwd': password
            },
            verify=False
        )
        
        print(f"Login response: {login_response.status_code}")
        print(f"Login response text: {login_response.text}")
        
        if login_response.status_code != 200:
            print(f"Login failed for {site_url}: {login_response.text}")
            return None, None

        # Get user info to retrieve API key
        user_info_url = f"{base_url}/api/method/frappe.auth.get_logged_user"
        user_info_response = session.get(user_info_url, verify=False)
        print(f"User info response: {user_info_response.text}")

        # Generate keys
        generate_key_url = f"{base_url}/api/method/frappe.core.doctype.user.user.generate_keys"
        print(f"Attempting to generate keys at {generate_key_url}")
        key_response = session.post(
            generate_key_url,
            data={'user': username},
            verify=False
        )
        
        print(f"Key generation response: {key_response.status_code}")
        print(f"Key generation response text: {key_response.text}")
        
        if key_response.status_code != 200:
            print(f"Key generation failed for {site_url}: {key_response.text}")
            return None, None

        # Get user details to get the API key
        user_details_url = f"{base_url}/api/resource/User/{username}"
        user_details_response = session.get(user_details_url, verify=False)
        print(f"User details response: {user_details_response.text}")
        
        try:
            api_secret = key_response.json().get('message', {}).get('api_secret')
            user_data = user_details_response.json().get('data', {})
            api_key = user_data.get('api_key')
            
            if not api_key or not api_secret:
                print(f"Missing API key or secret for {site_url}")
                return None, None
                
            return api_key, api_secret
            
        except Exception as e:
            print(f"Error parsing response for {site_url}: {str(e)}")
            return None, None
        
    except Exception as e:
        print(f"Error processing {site_url}: {str(e)}")
        return None, None
    finally:
        session.close()

def main():
    # Read CSV file with string data types
    df = pd.read_csv('creds.csv', dtype=str)
    
    # Process all sites in the CSV
    for index, row in df.iterrows():
        print(f"\nProcessing site: {row['siteurl']}")
        
        api_key, api_secret = login_and_generate_keys(
            row['siteurl'],
            row['Username'],
            row['Password']
        )
        
        if api_key and api_secret:
            print(f"Successfully generated keys for {row['siteurl']}")
            df.at[index, 'api_key'] = api_key
            df.at[index, 'api_secret'] = api_secret
        
        # Wait a bit between requests
        time.sleep(2)
    
    # Save updated CSV
    df.to_csv('creds_updated.csv', index=False)
    print("\nProcess completed. Check creds_updated.csv for results.")

if __name__ == "__main__":
    main()
