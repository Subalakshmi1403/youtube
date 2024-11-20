import os
import browser_cookie3

# Set the environment variable for Chrome's user data directory (replace <YourUsername>)
os.environ['CHROME_USER_DATA_DIR'] = r"C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data"

# Now use the browser_cookie3 to get cookies
cookies = browser_cookie3.chrome()

# Print cookies for a specific domain
for cookie in cookies:
    print(cookie)
