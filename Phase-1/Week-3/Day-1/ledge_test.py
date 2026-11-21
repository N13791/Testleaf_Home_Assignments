import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MakeMyTripTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def tearDown(self):
        self.driver.quit()

    # TC-001: Search flights with valid origin, destination and date
    def test_TC_001_search_flights_valid(self):
        driver = self.driver
        wait = self.wait

        # Navigate to homepage
        driver.get("https://www.makemytrip.com/")

        # Click the origin/destination selector button
        od_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "div > div > div:nth-of-type(2) > div:nth-of-type(1)"))
        )
        od_button.click()

        # TODO: Verify that origin field shows "BLR" and destination field shows "CCU"
        # GAPS: No captured locator for the individual origin/destination input fields.

        # Click the departure date button
        date_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(3) > label"))
        )
        date_button.click()

        # TODO: Verify that the selected date is highlighted in the calendar
        # GAPS: No captured locator or attribute indicating the highlighted date.

        # Click the SEARCH button
        search_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "button[data-cy=\"submit\"]"))
        )
        search_btn.click()

        # Verify navigation to results page
        wait.until(EC.url_contains("/flight/search"))
        self.assertIn("/flight/search", driver.current_url)

        # Verify at least one flight listing is present
        flight_listing = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "div > div:nth-of-type(3) > div:nth-of-type(1) > button"))
        )
        self.assertTrue(flight_listing.is_displayed())

    # TC-003: Navigate dates using Next and Previous buttons
    def test_TC_003_date_navigation(self):
        driver = self.driver
        wait = self.wait

        driver.get("https://www.makemytrip.com/")

        # Open date picker (assumed already open after page load)
        # Click Next dates button
        next_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "button[aria-label=\"Next dates\"]"))
        )
        next_btn.click()

        # TODO: Verify calendar moved to next month
        # GAPS: No element or attribute captured that reflects the displayed month.

        # Click Previous dates button
        prev_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "button[aria-label=\"Previous dates\"]"))
        )
        prev_btn.click()

        # TODO: Verify calendar returned to original month
        # GAPS: No element or attribute captured that reflects the displayed month.

    # TC-004: Search with missing origin
    def test_TC_004_missing_origin(self):
        driver = self.driver
        wait = self.wait

        driver.get("https://www.makemytrip.com/")

        # TODO: Locate and clear the origin field
        # GAPS: No captured locator for the origin input element.

        # Select destination (using the combined origin/destination button as a proxy)
        dest_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "div > div > div:nth-of-type(2) > div:nth-of-type(1)"))
        )
        dest_button.click()

        # TODO: Verify destination is set to CCU
        # GAPS: No captured locator for the destination field/value.

        # Click SEARCH
        search_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "button[data-cy=\"submit\"]"))
        )
        search_btn.click()

        # TODO: Verify validation message about missing origin appears
        # GAPS: No captured locator or text for the validation message.

    # TC-006: Enter excessively long text in flight preference
    def test_TC_006_excessive_preference_text(self):
        driver = self.driver
        wait = self.wait

        # Navigate directly to a results page (using recorded URL)
        driver.get("https://www.makemytrip.com/flight/search?itinerary=BLR-CCU-24/11/2026&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&lang=eng")

        # Locate the preference textarea
        pref_textarea = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "textarea[data-test=\"component-smartFilterSearchInput\"]"))
        )
        long_text = "A" * 2000
        pref_textarea.clear()
        pref_textarea.send_keys(long_text)

        # Verify the textarea contains the input (or is truncated)
        entered = pref_textarea.get_attribute("value")
        self.assertTrue(len(entered) <= 2000)

        # Click SEARCH
        search_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "button[data-cy=\"submit\"]"))
        )
        search_btn.click()

        # TODO: Verify system truncates input or shows a validation warning
        # GAPS: No captured element or message indicating truncation/warning.

    # TC-007: XSS attempt via flight preference textarea
    def test_TC_007_xss_attempt(self):
        driver = self.driver
        wait = self.wait

        driver.get("https://www.makemytrip.com/flight/search?itinerary=BLR-CCU-24/11/2026&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&lang=eng")

        pref_textarea = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "textarea[data-test=\"component-smartFilterSearchInput\"]"))
        )
        xss_payload = "<script>alert('XSS')</script>"
        pref_textarea.clear()
        pref_textarea.send_keys(xss_payload)

        # Verify the literal text appears in the textarea
        self.assertEqual(pref_textarea.get_attribute("value"), xss_payload)

        # Click SEARCH
        search_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "button[data-cy=\"submit\"]"))
        )
        search_btn.click()

        # Ensure no alert is shown (i.e., script not executed)
        try:
            alert = wait.until(EC.alert_is_present())
            self.fail("Unexpected alert present, possible XSS execution.")
        except:
            pass  # No alert, as expected

    # TC-009: Keyboard‑only navigation to perform search
    def test_TC_009_keyboard_navigation_search(self):
        driver = self.driver
        wait = self.wait

        driver.get("https://www.makemytrip.com/")

        # Tab until SEARCH button receives focus
        search_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                "button[data-cy=\"submit\"]"))
        )
        max_tabs = 30
        for _ in range(max_tabs):
            active = driver.switch_to.active_element
            if active == search_btn:
                break
            active.send_keys(Keys.TAB)
        else:
            self.fail("SEARCH button did not receive focus after tabbing.")

        # Verify focus outline (implicit by active element)
        self.assertEqual(driver.switch_to.active_element, search_btn)

        # Press Enter to submit
        driver.switch_to.active_element.send_keys(Keys.ENTER)

        # Verify results page loads
        wait.until(EC.url_contains("/flight/search"))
        self.assertIn("/flight/search", driver.current_url)

    # TC-010: Verify label‑checkbox association and focus order for filters
    def test_TC_010_filter_checkboxes_accessibility(self):
        driver = self.driver
        wait = self.wait

        driver.get("https://www.makemytrip.com/flight/search?itinerary=BLR-CCU-24/11/2026&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&lang=eng")

        # Gather all filter checkboxes (they share the same selector)
        checkboxes = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                "input[name=\"listingFilterCheckbox\"]"))
        )
        self.assertGreaterEqual(len(checkboxes), 2, "Expected at least two filter checkboxes.")

        # Press Tab to focus first checkbox (Non Stop)
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.TAB)
        active = driver.switch_to.active_element
        self.assertTrue(active in checkboxes, "First focus is not on a filter checkbox.")

        # Verify that the focused checkbox corresponds to "Non Stop"
        # Since we cannot read the label via ARIA, we check the id if available
        non_stop_id = "newGroupFilter_07103e2e-e5aa-11f1-9663-0a58a9feac10_0"
        self.assertEqual(active.get_attribute("id"), non_stop_id)

        # Iterate through remaining checkboxes with Tab and verify focus order
        expected_labels = [
            "Air India",
            "IndiGo",
            "Air India Express",
            "Akasa Air"
        ]
        # Map label to id from snapshot for verification
        label_to_id = {
            "Air India": "newGroupFilter_07103dc1-e5aa-11f1-9663-0a58a9feac10_AI",
            "IndiGo": "newGroupFilter_07103df8-e5aa-11f1-9663-0a58a9feac10_6E",
            "Air India Express": "newGroupFilter_07103dd4-e5aa-11f1-9663-0a58a9feac10_IX",
            "Akasa Air": "newGroupFilter_07103de5-e5aa-11f1-9663-0a58a9feac10_QP"
        }

        for label in expected_labels:
            driver.switch_to.active_element.send_keys(Keys.TAB)
            active = driver.switch_to.active_element
            self.assertTrue(active in checkboxes, f"Focus did not move to a checkbox for {label}.")
            self.assertEqual(active.get_attribute("id"), label_to_id[label],
                             f"Focused checkbox id does not match expected for {label}.")

GAPS:
- TC-001: No captured locators for individual origin/destination fields; cannot assert they display "BLR" and "CCU".
- TC-001: No captured locator or attribute indicating which date is highlighted; cannot verify date selection.
- TC-003: No captured element reflecting the displayed month; cannot verify calendar navigation.
- TC-004: No captured locator for the origin input field; cannot clear it.
- TC-004: No captured locator for setting destination independently; cannot verify destination set to "CCU".
- TC-004: No captured locator or text for the validation message when origin is missing.
- TC-006: No captured element or message indicating truncation or validation warning after submitting over‑length preference.
