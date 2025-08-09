from playwright.sync_api import sync_playwright
import keyboard
import os

profile_path = os.path.abspath("chrome_profile")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=profile_path, 
        channel='chrome', 
        headless=False, 
        viewport={"width": 1280, "height": 593}, 
        device_scale_factor=1.5, 
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36', 
        locale='en-IN', 
        timezone_id='Asia/Kolkata', 
        args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-infobars',
            '--disable-extensions'
        ]
    )

    page = browser.pages[0] if browser.pages else browser.new_page()

    # js
    page.add_init_script('''
        // webdriver
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

        // plugins
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });

        // languages
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });

        // permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) =>
            parameters.name === 'notifications'
                ? Promise.resolve({ state: Notification.permission })
                : originalQuery(parameters);
    ''')

    # page.goto('https://music.apple.com/in/home')
    page.goto('https://whatismyviewport.com/')
    print(page.title())
    keyboard.wait('ctrl+space')
    browser.close()