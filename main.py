import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
ACCOUNT_EMAIL="ishuaggrawal@test.com"
ACCOUNT_PASSWORD="Ishu@1234"
ADMIN_ACCOUNT_EMAIL="admin@test.com"
ADMIN_ACCOUNT_PASSWORD="admin123"
chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
user_data_dir=os.path.join(os.getcwd(),"chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
wait=WebDriverWait(driver,2)
driver.get("https://appbrewery.github.io/gym/")
def retry(func,retries=20,description=None):
    for i in range(retries):
        print(f"Trying {description}. Attempt: {i+1}")
        try:
            return func()
        except TimeoutException:
            if i==retries-1:
                raise
# driver.find_element(By.ID,value="login-button").click()
# driver.implicitly_wait(2)
# email_input=driver.find_element(By.ID,value="email-input")
# email_input.send_keys(ADMIN_ACCOUNT_EMAIL)
# password_input=driver.find_element(By.ID,value="password-input")
# password_input.send_keys(ADMIN_ACCOUNT_PASSWORD)
# driver.find_element(By.ID,value="submit-button").click()
# driver.find_element(By.ID,"advance-3-days").click()
# driver.find_element(By.ID,"logout-button").click()
def login():
    driver.find_element(By.ID,value="login-button").click()
    driver.implicitly_wait(2)
    email_input=driver.find_element(By.ID,value="email-input")
    email_input.send_keys(ACCOUNT_EMAIL)
    password_input=driver.find_element(By.ID,value="password-input")
    password_input.send_keys(ACCOUNT_PASSWORD)
    driver.find_element(By.ID,value="submit-button").click()
    wait.until(ec.presence_of_element_located((By.ID,"schedule-page")))
retry(login,description="login")
class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")
already_booked_classes=0
waitlist_class=0
booked_class=0
processes_list=[]
def booking(booking_button,button_title):
    booking_button.click()
    wait.until(lambda d:booking_button.text==button_title)
for i in class_cards:
    day_group=i.find_element(By.XPATH,"./ancestor::div[contains(@id,'day-group-')]")
    day_title=day_group.find_element(By.TAG_NAME,"h2").text
    if "Wed" in day_title or "Thu" in day_title:
        time=i.find_element(By.CSS_SELECTOR,"p[id^='class-time-'").text
        if "6:00 PM" in time:
            name=i.find_element(By.CSS_SELECTOR,"h3[id^='class-name']").text
            button=i.find_element(By.CSS_SELECTOR,"button[id^='book-button-']")
            info=f"{name} on {day_title}"
            if button.text=="Booked":
                already_booked_classes+=1
                print(f"✓ Already booked: {name} on {day_title}")
                processes_list.append(f"[Booked] {info}")
            elif button.text=="Waitlisted":
                already_booked_classes += 1
                print(f"✓ Already on waitlist: {name} on {day_title}")
                processes_list.append(f"[Waitlisted] {info}")
            elif button.text=="Join Waitlist":
                waitlist_class+=1
                retry(lambda: booking(button,button_title="Waitlisted"),description="Waitlisting")
                print(f"✓ Joined waitlist for: {name} on {day_title}")
                processes_list.append(f"[New Waitlist] {info}")
            else:
                booked_class+=1
                retry(lambda: booking(button,button_title="Booked"),description="Booking")
                print(f"✓ Booked: {name} on {day_title}")
                processes_list.append(f"[New Booking] {info}")
total_bookings=already_booked_classes+waitlist_class+booked_class
# print(f"Classes Booked: {booked_class}")
# print(f"Waitlists Joined: {waitlist_class}")
# print(f"Already Booked/Waitlisted: {already_booked_classes}")
# print(f"Total Tuesday 6:00 PM  Classes Processed: {booked_class+waitlist_class+already_booked_classes}")
# for i in processes_list:
#     print(f" • {i}")
print(f"\n--- Total Wednesday/Thursday 6pm classes: {total_bookings} ---")
print(f"\n--- VERIFYING ON MY BOOKING PAGE ---")
def check_booking():
    driver.find_element(By.ID,"my-bookings-link").click()
    wait.until(ec.presence_of_element_located((By.ID,"my-bookings-page")))
    cards=driver.find_elements(By.CSS_SELECTOR,"div[id*='card-']")
    if not cards:
        raise TimeoutException("No booking cards found - page may not have loaded")
    return cards
verified=0
all_cards=retry(check_booking,description="Get my Bookings")
for i in all_cards:
    try:
        when_ref=i.find_element(By.XPATH,".//p[strong[text()='When:']]")
        when=when_ref.text
        if ("Wed" in when or "Thu" in when) and "6:00 PM" in when:
            class_name=i.find_element(By.TAG_NAME,"h3").text
            print(f"✓ Verified: {class_name}")
            verified+=1
    except NoSuchElementException:
        pass
print(f"\n--- VERIFICATION RESULTS ---")
print(f"Expected: {total_bookings}")
print(f"Found: {verified}")
if total_bookings==verified:
    print("✅ SUCCESS: All bookings verified!")
else:
    print(f"❌ MISMATCH: Missing {total_bookings-verified} bookings")
