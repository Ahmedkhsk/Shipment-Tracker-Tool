from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def wait_for_loader_and_results(driver, loader_xpath, result_xpath, timeout=40):
    try:
        print("Waiting for loader to appear...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(("xpath", loader_xpath))
        )
        print("Loader appeared.")
    except TimeoutException:
        print("Loader did not appear, maybe already loaded.")

    try:
        print("Waiting for loader to disappear...")
        WebDriverWait(driver, timeout).until_not(
            EC.presence_of_element_located(("xpath", loader_xpath))
        )
        print("Loader disappeared.")
    except TimeoutException:
        print("Loader did not disappear in time.")

    print("Waiting for results to appear...")
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(("xpath", result_xpath))
    )
    print("Results appeared.")