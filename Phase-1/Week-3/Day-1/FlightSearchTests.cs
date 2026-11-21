using NUnit.Framework;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;
using System;

namespace MakeMyTripTests
{
    [TestFixture]
    public class FlightSearchTests
    {
        private IWebDriver driver;
        private WebDriverWait wait;
        private const string HomeUrl = "https://www.makemytrip.com/";
        private const string ResultsUrl = "https://www.makemytrip.com/flight/search?itinerary=BLR-CCU-24/11/2026&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&lang=eng";

        // Locators taken directly from the recorded actions / page snapshot
        private readonly By fromToButton = By.CssSelector("div > div > div:nth-of-type(2) > div:nth-of-type(1)");
        private readonly By departureButton = By.CssSelector("div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(3) > label");
        private readonly By searchButton = By.CssSelector("div > div:nth-of-type(2) > p > button");
        private readonly By flightCard = By.CssSelector("div[data-test=\"component-clusterSingleCardBody\"]");
        private readonly By nextDatesButton = By.CssSelector("button[aria-label=\"Next dates\"]");
        private readonly By previousDatesButton = By.CssSelector("button[aria-label=\"Previous dates\"]");
        private readonly By preferenceTextarea = By.CssSelector("textarea[data-test=\"component-smartFilterSearchInput\"]");
        // Checkboxes share the same selector; specific identification by label is not captured.
        private readonly By genericCheckbox = By.CssSelector("input[name=\"listingFilterCheckbox\"]");

        [SetUp]
        public void SetUp()
        {
            driver = new ChromeDriver();
            driver.Manage().Window.Maximize();
            wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
        }

        [TearDown]
        public void TearDown()
        {
            driver.Quit();
        }

        // TC-001: Search flights with valid origin, destination and date
        [Test]
        public void TC_001_SearchFlights_ValidData()
        {
            driver.Navigate().GoToUrl(HomeUrl);

            // Click the From/To button
            wait.Until(d => d.FindElement(fromToButton)).Click();

            // Click the departure date button
            wait.Until(d => d.FindElement(departureButton)).Click();

            // Click SEARCH
            wait.Until(d => d.FindElement(searchButton)).Click();

            // Verify that results page loads and a flight card is displayed
            wait.Until(d => d.Url.Contains("/flight/search"));
            wait.Until(d => d.FindElement(flightCard));
            Assert.IsTrue(driver.FindElements(flightCard).Count > 0, "No flight listings were found.");
        }

        // TC-002: Apply filters and search
        [Test]
        public void TC_002_ApplyFiltersAndSearch()
        {
            // Precondition: results page displayed
            driver.Navigate().GoToUrl(ResultsUrl);

            // Check "Non Stop" checkbox
            // TODO: locator not captured for the "Non Stop" checkbox (needs label-specific selector)
            // driver.FindElements(genericCheckbox)[?].Click();

            // Check "Air India" checkbox
            // TODO: locator not captured for the "Air India" checkbox (needs label-specific selector)
            // driver.FindElements(genericCheckbox)[?].Click();

            // Enter preference text
            var textarea = wait.Until(d => d.FindElement(preferenceTextarea));
            textarea.Clear();
            textarea.SendKeys("Window seat");

            // Click SEARCH
            wait.Until(d => d.FindElement(searchButton)).Click();

            // Verify that the textarea retains the entered text after refresh
            var refreshedTextarea = wait.Until(d => d.FindElement(preferenceTextarea));
            Assert.AreEqual("Window seat", refreshedTextarea.GetAttribute("value"));
        }

        // TC-003: Navigate dates using Next and Previous buttons
        [Test]
        public void TC_003_NavigateDates_NextPrevious()
        {
            driver.Navigate().GoToUrl(HomeUrl);

            // Open date picker (assumed already open via previous steps)
            // Click Next dates
            wait.Until(d => d.FindElement(nextDatesButton)).Click();

            // TODO: verify calendar moved to next month (no captured element to assert)

            // Click Previous dates
            wait.Until(d => d.FindElement(previousDatesButton)).Click();

            // TODO: verify calendar returned to original month (no captured element to assert)
        }

        // TC-004: Search with missing origin
        [Test]
        public void TC_004_SearchMissingOrigin()
        {
            driver.Navigate().GoToUrl(HomeUrl);

            // Clear origin field
            // TODO: locator not captured for the origin input field
            // var originInput = driver.FindElement(...);
            // originInput.Clear();

            // Select destination using the same From/To button (sets destination to CCU)
            wait.Until(d => d.FindElement(fromToButton)).Click();

            // Click SEARCH
            wait.Until(d => d.FindElement(searchButton)).Click();

            // TODO: verify validation message for missing origin (no locator captured)
        }

        // TC-005: Search with past departure date
        [Test]
        public void TC_005_SearchPastDepartureDate()
        {
            driver.Navigate().GoToUrl(HomeUrl);

            // Open date picker and enter past date
            // TODO: locator not captured for the date input field within the date picker
            // var dateInput = driver.FindElement(...);
            // dateInput.Clear();
            // dateInput.SendKeys("1 Jan 2020");

            // Click SEARCH
            wait.Until(d => d.FindElement(searchButton)).Click();

            // TODO: verify error message about past date (no locator captured)
        }

        // TC-007: XSS attempt via flight preference textarea
        [Test]
        public void TC_007_XssAttemptInPreference()
        {
            driver.Navigate().GoToUrl(ResultsUrl);

            var textarea = wait.Until(d => d.FindElement(preferenceTextarea));
            textarea.Clear();
            textarea.SendKeys("<script>alert('XSS')</script>");

            wait.Until(d => d.FindElement(searchButton)).Click();

            // TODO: verify that no script execution occurs (cannot capture alert or page change without a locator)
        }

        // TC-008: SQL injection pattern in flight preference
        [Test]
        public void TC_008_SqlInjectionInPreference()
        {
            driver.Navigate().GoToUrl(ResultsUrl);

            var textarea = wait.Until(d => d.FindElement(preferenceTextarea));
            textarea.Clear();
            textarea.SendKeys("' OR '1'='1");

            wait.Until(d => d.FindElement(searchButton)).Click();

            // TODO: verify that search completes without database error (no error element captured)
        }

        // TC-009: Keyboard‑only navigation to perform search
        [Test]
        public void TC_009_KeyboardOnlyNavigation()
        {
            driver.Navigate().GoToUrl(HomeUrl);

            // Tab until the SEARCH button receives focus
            IWebElement activeElement = null;
            for (int i = 0; i < 20; i++) // arbitrary limit to avoid infinite loop
            {
                driver.SwitchTo().ActiveElement();
                activeElement = driver.SwitchTo().ActiveElement();
                if (activeElement.TagName.Equals("button", StringComparison.OrdinalIgnoreCase) &&
                    activeElement.Text.Trim().Equals("SEARCH", StringComparison.OrdinalIgnoreCase))
                {
                    break;
                }
                activeElement.SendKeys(Keys.Tab);
            }

            Assert.IsTrue(activeElement != null && activeElement.Text.Trim().Equals("SEARCH", StringComparison.OrdinalIgnoreCase),
                "SEARCH button did not receive focus via keyboard navigation.");

            // Press Enter to submit
            activeElement.SendKeys(Keys.Enter);

            // Verify results page loads
            wait.Until(d => d.Url.Contains("/flight/search"));
            wait.Until(d => d.FindElement(flightCard));
            Assert.IsTrue(driver.FindElements(flightCard).Count > 0, "Search results were not displayed after keyboard submission.");
        }
    }
}
