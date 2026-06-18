from playwright.sync_api import sync_playwright

def verify_leaderboard():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # In the context of tests, localStorage needs to have user_id to skip redirect
        page.goto("http://localhost:8000/global_leaderboard.html")
        page.evaluate('localStorage.setItem("user_id", "test_id");')
        page.goto("http://localhost:8000/global_leaderboard.html")

        page.wait_for_selector(".main-tab-btn")

        # Take screenshot of the initial view
        page.screenshot(path="verification_initial.png")

        # Click the Schools tab
        schools_tab = page.locator("button.main-tab-btn", has_text="Schools")
        schools_tab.click()

        # Wait for schools view to be visible
        page.wait_for_selector("#schools-view")

        # Take screenshot of the schools view
        page.screenshot(path="verification_schools.png")

        # Let's also check the signup page
        page.evaluate('localStorage.removeItem("user_id");')
        page.goto("http://localhost:8000/signup.html")
        page.wait_for_selector("#school")
        school_input = page.locator("#school")
        school_input.fill("Pretoria")

        # Take screenshot of signup
        page.screenshot(path="verification_signup.png")

        browser.close()

verify_leaderboard()
