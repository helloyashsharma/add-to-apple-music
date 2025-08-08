from playwright.sync_api import sync_playwright
import keyboard
import os

profile_path = os.path.abspath("chrome_profile")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=profile_path, 
        channel='chrome', 
        headless=False
        )
    page = browser.new_page()
    page.goto('https://music.apple.com/in/home')
    print(page.title())
    keyboard.wait('ctrl+space')
    browser.close()