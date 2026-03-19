from playwright.sync_api import sync_playwright
import time
import os

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto('http://localhost:8000/dashboard.html')
    # Set local storage using evaluation
    page.evaluate("localStorage.setItem('user_id', 'test_user')")
    page.evaluate("localStorage.setItem('user_grade', 'grade6')")

    page.goto('http://localhost:8000/subjects.html')
    time.sleep(2)

    page.screenshot(path='subjects_page_g6.png')

    # click the Mathematics button
    page.click("button:has-text('Mathematics')")
    time.sleep(1)

    page.screenshot(path='subjects_expanded_g6.png')
    browser.close()
