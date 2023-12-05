import requests

# Replace 'your_api_key' with your actual 2Captcha API key
API_KEY = 'your_api_key'

def solve_captcha(api_key, site_key, url):
    # 2Captcha API endpoint for solving reCAPTCHA
    captcha_api_url = f"https://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={site_key}&pageurl={url}&json=1"

    # Sending a request to solve the CAPTCHA
    response = requests.post(captcha_api_url)

    if response.status_code == 200:
        captcha_id = response.json()['request']
        # Polling 2Captcha until the CAPTCHA is solved
        captcha_result_url = f"https://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}&json=1"
        retries = 20
        while retries > 0:
            retries -= 1
            response = requests.get(captcha_result_url)
            if response.status_code == 200:
                result = response.json()
                if result['status'] == 1:
                    return result['request']
            time.sleep(5)  # Wait for 5 seconds before polling again
        return None
    else:
        return None

# Example usage
site_key = 'the_site_key'
url_to_scrape = 'https://www.example.com'

captcha_response = solve_captcha(API_KEY, site_key, url_to_scrape)

if captcha_response:
    # Use the obtained CAPTCHA response in your scraping process
    print(f"CAPTCHA response obtained: {captcha_response}")
else:
    print("Failed to solve CAPTCHA.")
