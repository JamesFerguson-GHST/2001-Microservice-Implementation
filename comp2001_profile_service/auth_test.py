import requests

# Authenticator endpoint
auth_url = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

# Test user credentials (from coursework instructions)
email = "tim@plymouth.ac.uk"
password = "COMP2001!"

# JSON payload
credentials = {
    "email": email,
    "password": password
}

# Send POST request
response = requests.post(auth_url, json=credentials)

# Handle response
if response.status_code == 200:
    try:
        json_response = response.json()
        print("Authenticated successfully")
        print(json_response)
    except requests.JSONDecodeError:
        print("Authentication succeeded but response is not JSON")
        print(response.text)
else:
    print(f"Authentication failed with status code {response.status_code}")
    print("Response content:")
    print(response.text)