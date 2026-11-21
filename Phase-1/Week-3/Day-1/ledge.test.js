const { Builder, By, until, Key } = require('selenium-webdriver');
const assert = require('assert').strict;

describe('MakeMyTrip Tests', function () {
  this.timeout(30000);
  let driver;

  beforeEach(async () => {
    driver = await new Builder().forBrowser('chrome').build();
  });

  afterEach(async () => {
    await driver.quit();
  });

  // TC-001: Search flights with valid origin, destination and date
  it('TC-001: Search flights with valid origin, destination and date', async () => {
    await driver.get('https://www.makemytrip.com/');

    // Click the origin/destination selector
    const odBtn = await driver.findElement(
      By.css('div > div > div:nth-of-type(2) > div:nth-of-type(1)')
    );
    await odBtn.click();

    // TODO: verify origin and destination fields show BLR and CCU (locator not captured)

    // Click the departure date button
    const depBtn = await driver.findElement(
      By.css('div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(3) > label')
    );
    await depBtn.click();

    // TODO: verify selected date is highlighted (locator not captured)

    // Click the SEARCH button
    const searchBtn = await driver.findElement(
      By.css('div > div:nth-of-type(2) > p > button')
    );
    await searchBtn.click();

    // Wait for results page to load
    await driver.wait(until.urlContains('/flight/search'), 10000);

    // TODO: assert that flight listings are displayed (locator not captured)
  });

  // TC-002: Apply filters and search
  it('TC-002: Apply filters and search', async () => {
    // Precondition: results page is displayed
    await driver.get(
      'https://www.makemytrip.com/flight/search?itinerary=BLR-CCU-24/11/2026&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&lang=eng'
    );

    // Check "Non Stop"
    const nonStopChk = await driver.findElement(
      By.id('newGroupFilter_07103e2e-e5aa-11f1-9663-0a58a9feac10_0')
    );
    if (!(await nonStopChk.isSelected())) await nonStopChk.click();
    assert.ok(await nonStopChk.isSelected(), 'Non Stop checkbox should be selected');

    // Check "Air India"
    const airIndiaChk = await driver.findElement(
      By.id('newGroupFilter_07103dc1-e5aa-11f1-9663-0a58a9feac10_AI')
    );
    if (!(await airIndiaChk.isSelected())) await airIndiaChk.click();
    assert.ok(await airIndiaChk.isSelected(), 'Air India checkbox should be selected');

    // Enter preference text
    const prefTextarea = await driver.findElement(
      By.css('textarea[data-test="component-smartFilterSearchInput"]')
    );
    await prefTextarea.clear();
    await prefTextarea.sendKeys('Window seat');
    assert.strictEqual(
      await prefTextarea.getAttribute('value'),
      'Window seat',
      'Preference textarea should contain entered text'
    );

    // Click SEARCH
    const searchBtn = await driver.findElement(
      By.css('div > div:nth-of-type(2) > p > button')
    );
    await searchBtn.click();

    // TODO: verify that results are refreshed with only non‑stop Air India flights (locator not captured)
  });

  // TC-003: Navigate dates using Next and Previous buttons
  it('TC-003: Navigate dates using Next and Previous buttons', async () => {
    await driver.get('https://www.makemytrip.com/');

    // TODO: open the date picker (locator not captured)

    // Click "Next dates"
    const nextBtn = await driver.findElement(
      By.css('button[aria-label="Next dates"]')
    );
    await nextBtn.click();

    // TODO: verify calendar moved to the next month (locator not captured)

    // Click "Previous dates"
    const prevBtn = await driver.findElement(
      By.css('button[aria-label="Previous dates"]')
    );
    await prevBtn.click();

    // TODO: verify calendar returned to the original month (locator not captured)
  });

  // TC-004: Search with missing origin
  it('TC-004: Search with missing origin', async () => {
    await driver.get('https://www.makemytrip.com/');

    // TODO: clear the origin field (locator not captured)

    // Select destination using the button
    const destBtn = await driver.findElement(
      By.css('div > div > div:nth-of-type(2) > div:nth-of-type(1)')
    );
    await destBtn.click();

    // TODO: verify destination is set to CCU (locator not captured)

    // Click SEARCH
    const searchBtn = await driver.findElement(
      By.css('div > div:nth-of-type(2) > p > button')
    );
    await searchBtn.click();

    // TODO: assert validation message for missing origin (locator not captured)
  });

  // TC-005: Search with past departure date
  it('TC-005: Search with past departure date', async () => {
    await driver.get('https://www.makemytrip.com/');

    // TODO: set origin to BLR (locator not captured)
    // TODO: set destination to CCU (locator not captured)

    // Enter past date via date picker
    // TODO: locate the date input field (selector not captured) and send the past date
    // Example placeholder (replace with real locator when available):
    // const dateInput = await driver.findElement(By.css('...'));
    // await dateInput.clear();
    // await dateInput.sendKeys('01/01/2020');

    // Click SEARCH
    const searchBtn = await driver.findElement(
      By.css('div > div:nth-of-type(2) > p > button')
    );
    await searchBtn.click();

    // TODO: verify error message about past date (locator not captured)
  });

  // TC-006: Enter excessively long text in flight preference
  it('TC-006: Enter excessively long text in flight preference', async () => {
    await driver.get(
      'https://www.makemytrip.com/flight/search?itinerary=BLR-CCU-24/11/2026&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&lang=eng'
    );

    const prefTextarea = await driver.findElement(
      By.css('textarea[data-test="component-smartFilterSearchInput"]')
    );
    const longText = 'A'.repeat(2000);
    await prefTextarea.clear();
    await prefTextarea.sendKeys(longText);

    const entered = await prefTextarea.getAttribute('value');
    assert.ok(
      entered.length <= 2000,
      'Textarea should not exceed 2000 characters'
    );

    const searchBtn = await driver.findElement(
      By.css('div > div:nth-of-type(2) > p > button')
    );
    await searchBtn.click();

    // TODO: verify truncation or validation warning (locator not captured)
  });

  // TC-007: XSS attempt via flight preference textarea
  it('TC-007: XSS attempt via flight preference textarea', async () => {
    await driver.get(
      'https://www.makemytrip.com/flight/search?itinerary=BLR-CCU-24/11/2026&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&lang=eng'
    );

    const prefTextarea = await driver.findElement(
      By.css('textarea[data-test="component-smartFilterSearchInput"]')
    );
    const xss = "<script>alert('XSS')</script>";
    await prefTextarea.clear();
    await prefTextarea.sendKeys(xss);
    const value = await prefTextarea.getAttribute('value');
    assert.strictEqual(value, xss, 'Textarea should contain the raw XSS string');

    const searchBtn = await driver.findElement(
      By.css('div > div:nth-of-type(2) > p > button')
    );
    await searchBtn.click();

    // TODO: ensure no script execution occurs (e.g., no alert) (locator not captured)
  });

  // TC-008: SQL injection pattern in flight preference
  it('TC-008: SQL injection pattern in flight preference', async () => {
    await driver.get(
      'https://www.makemytrip.com/flight/search?itinerary=BLR-CCU-24/11/2026&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&lang=eng'
    );

    const prefTextarea = await driver.findElement(
      By.css('textarea[data-test="component-smartFilterSearchInput"]')
    );
    const sql = "' OR '1'='1";
    await prefTextarea.clear();
    await prefTextarea.sendKeys(sql);
    const value = await prefTextarea.getAttribute('value');
    assert.strictEqual(value, sql, 'Textarea should contain the raw SQL string');

    const searchBtn = await driver.findElement(
      By.css('div > div:nth-of-type(2) > p > button')
    );
    await searchBtn.click();

    // TODO: verify search completes without database error or unauthorized data (locator not captured)
  });

  // TC-009: Keyboard‑only navigation to perform search
  it('TC-009: Keyboard‑only navigation to perform search', async () => {
    await driver.get('https://www.makemytrip.com/');

    // Press Tab repeatedly to land on the SEARCH button
    for (let i = 0; i < 10; i++) {
      await driver.actions().sendKeys(Key.TAB).perform();
    }

    // Verify focus is on the SEARCH button
    const active = await driver.switchTo().activeElement();
    // TODO: confirm that the active element is the SEARCH button (locator not captured)

    // Press Enter to submit
    await driver.actions().sendKeys(Key.ENTER).perform();

    // Wait for results page
    await driver.wait(until.urlContains('/flight/search'), 10000);
  });

  // TC-010: Verify label‑checkbox association and focus order for filters
  it('TC-010: Verify label‑checkbox association and focus order for filters', async () => {
    await driver.get(
      'https://www.makemytrip.com/flight/search?itinerary=BLR-CCU-24/11/2026&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&lang=eng'
    );

    // Tab to first filter checkbox (expected "Non Stop")
    for (let i = 0; i < 5; i++) {
      await driver.actions().sendKeys(Key.TAB).perform();
    }
    const active1 = await driver.switchTo().activeElement();
    const id1 = await active1.getAttribute('id');
    assert.strictEqual(
      id1,
      'newGroupFilter_07103e2e-e5aa-11f1-9663-0a58a9feac10_0',
      'First focused checkbox should be "Non Stop"'
    );

    // Tab through airline checkboxes
    for (let i = 0; i < 5; i++) {
      await driver.actions().sendKeys(Key.TAB).perform();
    }
    const active2 = await driver.switchTo().activeElement();
    // TODO: verify that each checkbox receives focus in logical order and that its label is correctly announced (accessibility tree not available)
  });
});
