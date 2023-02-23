import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# GOOGLE FORM FIELDS X_PATH ARE SAME EXCEPT one div
X_PATH_START = f'//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
X_PATH_END = ']/div/div/div[2]/div/div[1]/div/div[1]/input'

# uploading data on Google form
def upload_data(space_flight, GOOGLE_FORM_URL):
    print("\nPlease wait while data is being uploaded through Google Form.")
    # creating Selenium driver
    driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    # loop though each address of house
    for i, space_craft_name_list in enumerate(space_flight.space_craft_name_list):
        # accessing Google form
        driver.get(GOOGLE_FORM_URL)
        # wait until first element is clickable
        WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.XPATH, f"{X_PATH_START}1{X_PATH_END}")))

        # uploading data for each question on Google form
        driver.find_element(By.XPATH, f'{X_PATH_START}1{X_PATH_END}').send_keys(space_craft_name_list if space_craft_name_list else "")
        driver.find_element(By.XPATH, f'{X_PATH_START}2{X_PATH_END}').send_keys(space_flight.card_header_list[i] if space_flight.card_header_list[i] else "")
        driver.find_element(By.XPATH, f'{X_PATH_START}3{X_PATH_END}').send_keys(space_flight.launching_location_list[i] if space_flight.launching_location_list[i] else "")
        driver.find_element(By.XPATH, f'{X_PATH_START}4{X_PATH_END}').send_keys(space_flight.next_space_fight_time_list[i] if space_flight.next_space_fight_time_list[i] else "")
        # clicking on submit button
        driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span').click()
        # time.sleep(random.choice([0.1, 0.12, 0.15, 0.13]))
    time.sleep(5)