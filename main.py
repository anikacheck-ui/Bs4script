"""
====================================================================
PROJECT: HBX CyberVault Single-File Automation & Scraping Script
AUTHOR: Developer Hridoy
DESCRIPTION: Handles cloudscraper bypass, correct URL routing (?i=1),
             CSRF extraction, and single-file vault data scraping.
====================================================================
"""

import cloudscraper
from bs4 import BeautifulSoup

# Target Deployed URL with InfinityFree query parameter
TARGET_URL = "https://hbxcybervault.42web.io/?i=1"
BASE_URL = "https://hbxcybervault.42web.io/"

# Test Credentials List
CREDENTIALS_LIST = [
    {"username": "admin", "password": "WrongPassword123"},
    {"username": "root", "password": "SecretPassword@2026"},
    {"username": "admin", "password": "HBX@2026#Secure"}  # Valid credentials
]

def run_vault_automation():
    print("[*] Starting HBX CyberVault Single-File Automation...")
    
    valid_scraper = None
    successful_cred = None

    for idx, cred in enumerate(CREDENTIALS_LIST, 1):
        print(f"\n--- Attempt #{idx}: Testing Username '{cred['username']}' ---")
        
        # Create a fresh cloudscraper instance
        scraper = cloudscraper.create_scraper()

        try:
            # Step 1: GET request to fetch page and initialize cookies/CSRF
            response = scraper.get(TARGET_URL, timeout=15)
            if response.status_code != 200:
                print(f"[-] Failed to reach target page. Status: {response.status_code}")
                continue

            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            csrf_input = soup.find('input', {'id': 'csrf_token'})
            
            csrf_token = csrf_input.get('value') if csrf_input else ""
            print(f"[+] Dynamic CSRF Token Extracted: {csrf_token[:15]}...")

            # Prepare POST payload (Make sure keys match your HTML input 'name' attributes)
            payload = {
                'username': cred['username'],
                'password': cred['password'],
                'csrf_token': csrf_token
            }

            # Set headers to mimic a real browser submission
            headers = {
                'Referer': TARGET_URL,
                'Origin': BASE_URL.rstrip('/')
            }

            # Submit login request using cloudscraper (POST)
            login_response = scraper.post(BASE_URL, data=payload, headers=headers, allow_redirects=True)

            # Check if login succeeded by checking response content for vault table or dashboard indicators
            if "cyber-vault-table" in login_response.text or "Confidential" in login_response.text or "Asset" in login_response.text:
                print(f"[+] 🎉 SUCCESS! Valid Credentials Found -> User: {cred['username']} / Pass: {cred['password']}")
                valid_scraper = scraper
                successful_cred = cred
                break
            else:
                print(f"[-] ❌ Invalid credentials or authentication rejected.")

        except Exception as err:
            print(f"[-] Error during request: {err}")

    # Step 2: If valid session found, scrape the secret vault data from the single-file app
    if valid_scraper and successful_cred:
        print("\n================ ACQUIRING SECRET VAULT DATA ================")
        try:
            dash_res = valid_scraper.get(TARGET_URL, timeout=15)
            dash_soup = BeautifulSoup(dash_res.text, 'html.parser')

            vault_table = dash_soup.find('table', {'id': 'cyber-vault-table'})
            if not vault_table:
                vault_table = dash_soup.find('table')

            if vault_table:
                rows = vault_table.find_all('tr', class_='vault-row')
                if not rows:
                    rows = vault_table.find_all('tr')[1:] # Skip header if no class match
                
                for i, row in enumerate(rows, 1):
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        key_val = cols[0].get_text(strip=True)
                        data_val = cols[1].get_text(strip=True)
                        level_val = cols[2].get_text(strip=True)
                    else:
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
