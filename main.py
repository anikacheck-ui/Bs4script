"""
====================================================================
PROJECT: HBX CyberVault Automated Auth & Scraping Script
AUTHOR: Developer Hridoy
DESCRIPTION: Iterates through test credentials, handles dynamic CSRF 
             tokens, validates login, and scrapes secret vault data.
====================================================================
"""

import requests
from bs4 import BeautifulSoup

# Target Deployed URL
TARGET_URL = "https://hbxcybervault.42web.io/"

# Test Credentials List (Wrong ones first, correct one at the end or middle)
CREDENTIALS_LIST = [
    {"username": "admin", "password": "WrongPassword123"},
    {"username": "root", "password": "SecretPassword@2026"},
    {"username": "admin", "password": "HBX@2026#Secure"}  # Valid one
]

def run_vault_automation():
    print("[*] Starting HBX CyberVault Automated Testing...")
    
    valid_session = None
    successful_cred = None

    # Step 1: Loop through each credential pair
    for idx, cred in enumerate(CREDENTIALS_LIST, 1):
        print(f"\n--- Attempt #{idx}: Testing Username '{cred['username']}' ---")
        
        # Create a fresh session for each attempt to maintain clean cookies/state
        session = requests.Session()

        try:
            # GET login page to fetch the dynamic CSRF token
            response = session.get(TARGET_URL)
            if response.status_code != 200:
                print(f"[-] Failed to reach target page. Status: {response.status_code}")
                continue

            # Parse HTML with BeautifulSoup to find hidden CSRF token
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_input = soup.find('input', {'id': 'csrf_token'})
            
            csrf_token = csrf_input.get('value') if csrf_input else ""
            print(f"[+] Dynamic CSRF Token Extracted: {csrf_token[:15]}...")

            # Prepare POST payload
            payload = {
                'username': cred['username'],
                'password': cred['password'],
                'csrf_token': csrf_token
            }

            # Submit login request
            login_response = session.post(TARGET_URL, data=payload, allow_redirects=True)

            # Check if login succeeded (e.g., dashboard elements or vault table found in response)
            if "cyber-vault-table" in login_response.text or "Vault" in login_response.text or login_response.status_code == 200:
                # Double check if it's actually logged in by checking page content or url
                # Since it's a single-page app with JS view toggle, let's verify if response contains vault data or success indicator
                if "Confidential" in login_response.text or "Asset" in login_response.text:
                    print(f"[+] 🎉 SUCCESS! Valid Credentials Found -> User: {cred['username']} / Pass: {cred['password']}")
                    valid_session = session
                    successful_cred = cred
                    break
                else:
                    print(f"[-] ❌ Invalid credentials or authentication rejected.")
            else:
                print(f"[-] ❌ Login failed for {cred['username']}.")

        except Exception as err:
            print(f"[-] Error during request: {err}")

    # Step 2: If valid session found, proceed to scrape the secret vault data using BS4
    if valid_session and successful_cred:
        print("\n================ ACQUIRING SECRET VAULT DATA ================")
        try:
            # Fetch dashboard / main page content with active authenticated session
            dash_res = valid_session.get(TARGET_URL)
            dash_soup = BeautifulSoup(dash_res.text, 'html.parser')

            vault_table = dash_soup.find('table', {'id': 'cyber-vault-table'})
            if not vault_table:
                vault_table = dash_soup.find('table')

            if vault_table:
                rows = vault_table.find_all('tr', class_='vault-row')
                for i, row in enumerate(rows, 1):
                    asset = row.find('span', class_='asset-key')
                    payload_el = row.find('code', class_='secret-payload')
                    sec_level = row.find('span', class_='security-level')

                    key_val = asset.get_text(strip=True) if asset else "N/A"
                    data_val = payload_el.get_text(strip=True) if payload_el else "N/A"
                    level_val = sec_level.get_text(strip=True) if sec_level else "N/A"

                    print(f"[{i}] Asset: {key_val} | Payload: {data_val} | Security: {level_val}")
                print("=============================================================")
            else:
                print("[-] Vault table structure not found in the response.")
        except Exception as scrape_err:
            print(f"[-] Scraping Error: {scrape_err}")
    else:
        print("\n[-] ❌ All credential attempts failed. No valid session established.")

if __name__ == "__main__":
    run_vault_automation()
