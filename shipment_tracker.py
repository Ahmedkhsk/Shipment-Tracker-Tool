import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

def wait_for_loader_and_results(driver, loader_xpath, result_xpath, timeout=40):
    try:
        print("Waiting for loader to appear...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, loader_xpath))
        )
        print("Loader appeared.")
    except TimeoutException:
        print("Loader did not appear, maybe already loaded.")

    try:
        print("Waiting for loader to disappear...")
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located((By.XPATH, loader_xpath))
        )
        print("Loader disappeared.")
    except TimeoutException:
        print("Loader did not disappear in time.")

    print("Waiting for results to appear...")
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, result_xpath))
    )
    print("Results appeared.")

class AdvancedShipmentTracker:
    def __init__(self):
        self.tracking_strategies = {
            'MSC': {
                'url': 'https://www.msc.com/en/track-a-shipment',
                'input_locators': [
                    ('id', 'trackingNumber'),
                    ('xpath', "//input[@placeholder='Enter a Container/Bill of Lading Number']"),
                    ('name', 'trackingNumber'),
                    ('xpath', "//input[contains(@placeholder, 'Container')]"),
                    ('xpath', "//input[contains(@placeholder, 'Bill of Lading')]"),
                ],
                'result_indicators': [
                    ('class_name', 'msc-flow-tracking__wrapper'),
                ],
                'eta_patterns': [
                    r'Price Calculation Date\*[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})',
                    r'Price Calculation Date\s*\*?\s*[:\-]?\s*([0-9]{2}/[0-9]{2}/[0-9]{4})',
                    r'POD ETA[:\s]*(\d{2}/\d{2}/\d{4})',
                    r'Estimated Time of Arrival[:\s]*(\d{2}/\d{2}/\d{4})',
                    r'ETA[:\s]*(\d{2}/\d{2}/\d{4})',
                ]
            },
        }

    def close_cookie_popup(self, driver):
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept All')]"))
            ).click()
            print("Cookie popup closed (Accept All).")
        except Exception:
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Accept')]"))
                ).click()
                print("Cookie popup closed (Accept).")
            except Exception:
                print("No cookie popup found or could not close it.")

    def find_and_interact(self, driver, locator_type, locator_value, action, input_text=None):
        try:
            if locator_type == "id":
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, locator_value)))
            elif locator_type == "name":
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, locator_value)))
            elif locator_type == "xpath":
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, locator_value)))
            elif locator_type == "css_selector":
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, locator_value)))
            elif locator_type == "class_name":
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, locator_value)))
            else:
                raise ValueError("Unsupported locator type")

            print(f"Element found for {action}: {locator_type}={locator_value}")

            if action == "send_keys":
                element.clear()
                element.send_keys(input_text)
                time.sleep(1)
                element.send_keys(Keys.ENTER)
                print("ENTER key sent after typing tracking number.")
            elif action == "click":
                WebDriverWait(driver, 10).until(lambda d: element.is_enabled())
                element.click()
            return True
        except Exception as e:
            print(f"Error in find_and_interact ({action}):", e)
            return False

    def extract_eta_from_page(self, text, eta_patterns):
        for pattern in eta_patterns:
            match = re.search(pattern, text)
            if match:
                print(f"ETA found: {match.group(1)}")
                return match.group(1)
        print("ETA not found in results text. Here is a snippet:")
        print(text[:1000])  
        return None

    def track_shipment_with_strategy(self, container_number, strategy_name, strategy_config):
        print("Starting shipment tracking on website...")
        options = Options()

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(strategy_config['url'])
            print("Website loaded.")
            self.close_cookie_popup(driver)
            found_input = False
            for locator_type, locator_value in strategy_config['input_locators']:
                if self.find_and_interact(driver, locator_type, locator_value, "send_keys", container_number):
                    found_input = True
                    print("Tracking number entered and ENTER sent.")
                    break
            if not found_input:
                print("Could not find input field for tracking number.")
                return None

            loader_xpath = "//div[contains(@class, 'msc-loader')]"
            result_xpath = "//div[contains(@class, 'msc-flow-tracking__wrapper')]"
            wait_for_loader_and_results(driver, loader_xpath, result_xpath)

            try:
                results_div = driver.find_element(By.XPATH, result_xpath)
                results_text = results_div.text
                print("Results text snippet:", results_text[:1000])
                eta = self.extract_eta_from_page(results_text, strategy_config['eta_patterns'])
            except Exception as e:
                print("Error extracting results text:", e)
                eta = None

            return eta
        except Exception as e:
            print("Tracking error:", e)
            return None
        finally:
            driver.quit()

    def determine_shipping_company(self, container_number):
        container_number = container_number.upper()
        if container_number.startswith(('MSDU', 'MEDU', 'MSKU')):
            return 'MSC'
        elif container_number.startswith(('MAEU', 'MWCU', 'MRKU')):
            return 'MAERSK'
        elif container_number.startswith(('COSU', 'OOLU', 'CXDU')):
            return 'COSCO'
        else:
            return None

    def track_shipment(self, container_number):
        company = self.determine_shipping_company(container_number)
        if company and company in self.tracking_strategies:
            print(f"Shipping company detected: {company}")
            eta = self.track_shipment_with_strategy(container_number, company, self.tracking_strategies[company])
            if eta:
                return eta
            else:
                print("ETA not found on website.")
        else:
            print("Shipping company not supported or not detected.")
        return None