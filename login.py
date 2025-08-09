from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import keyboard
import os

profile_path = os.path.abspath("chrome_profile")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=profile_path, 
        channel='chrome', 
        headless=False, 
        no_viewport=True, 
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36', 
        locale='en-IN', 
        timezone_id='Asia/Kolkata', 
        ignore_default_args=['--enable-automation', '--no-sandbox'], 
        args=[
            '--start-maximized'
        ]
    )

    page = browser.pages[0] if browser.pages else browser.new_page()
    stealth_sync(page)

    # page.goto('https://music.apple.com/in/home')
    page.goto('https://whatismyviewport.com/')
    print(page.title())
    keyboard.wait('ctrl+space')
    browser.close()