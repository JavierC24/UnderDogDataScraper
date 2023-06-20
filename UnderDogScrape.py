import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

############################################################################

options = webdriver.ChromeOptions()

options.add_argument("--disable-blink-features=AutomationControlled")  # Disable Blink features detection
options.add_argument("--disable-extensions")  # Disable browser extensions
options.add_argument("--disable-popup-blocking")  # Disable popup blocking
options.add_argument("--disable-notifications")  # Disable notifications
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--enable-javascript")  # Enable JavaScript
options.add_argument("--enable-cookies")  # Enable cookies

# Set a user agent to mimic a real browser
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36")

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)
driver.maximize_window()  # Open the window in full screen mode

############################################################################

email = "user"
pw = "pw"

# Scraping Underdog
driver.get(
    "https://underdogfantasy.com/?gclid=CjwKCAjw-b-kBhB-EiwA4fvKrK5KqUeZP7XbLX5f6ouWcG_PX7ceNOejNSfKLg_vfPKUv4uILyIoWRoCBgkQAvD_BwE")
time.sleep(1)
button = driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/button")  # Corrected line
button.click()

time.sleep(1)
user_name = driver.find_element(By.XPATH,
                                "/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/form/div[1]/label/div[2]/input")
pw_in = driver.find_element(By.XPATH,
                            "/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/form/div[2]/label/div[2]/input")
user_name.send_keys(email)
pw_in.send_keys(pw)
time.sleep(1)
login_bt = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/form/button[2]")
login_bt.click()

time.sleep(3)
check_stat = driver.find_element(By.XPATH, "/html/body/div[1]/div/nav/div[1]/a[2]").click()
time.sleep(3)

# Find the parent div element
parent_element = driver.find_element(By.CSS_SELECTOR, "#root > div > div > div.styles__playerListCol__boy4v")
print(parent_element)



# Create an empty list to store the extracted data
data_list = []

# Process and store the extracted data as needed
over_under_cells = parent_element.find_elements(By.CSS_SELECTOR, "div.styles__overUnderCell__KgzNn")
for cell in over_under_cells:
    player_name = cell.find_element(By.CSS_SELECTOR,
        "div.styles__actualTopRow__qe0VJ > div.styles__playerWrapper__kv40v > div.styles__playerInfo__e6Lbk > h1").text
    player_name = player_name.split(' ')[1]  # Remove leading/trailing spaces

    stat_line = cell.find_elements(By.CLASS_NAME,
        "styles__overUnderCell__qdEk_")
    for stat in stat_line:
        final = stat.find_element(By.CSS_SELECTOR, "div.styles__statLineRow__ybjNF > div > p").text
        data_list.append([player_name, final])

# Create a pandas DataFrame from the extracted data list
df = pd.DataFrame(data_list, columns=["Player Name", "Stat Line"])

# Save the DataFrame as a CSV file
df.to_csv("data.csv", index=False)

# Print the DataFrame
print(df)

