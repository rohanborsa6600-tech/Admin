
from playwright.sync_api import sync_playwright

def verify_mobile_layout():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)

        # Create a mobile context
        context = browser.new_context(
            viewport={'width': 375, 'height': 812},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
        )
        page = context.new_page()

        # Verify GEETA BHASHY.html
        print("Verifying GEETA BHASHY.html...")
        page.goto("http://localhost:8000/GEETA BHASHY.html")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="verification_geeta.png")

        # Verify STHALPOTHI.html
        print("Verifying STHALPOTHI.html...")
        page.goto("http://localhost:8000/STHALPOTHI.html")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="verification_sthalpothi.png")

        # Verify SUMANMALA.html
        print("Verifying SUMANMALA.html...")
        page.goto("http://localhost:8000/SUMANMALA.html")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="verification_sumanmala.png")

        # Verify SUTRAPATH.html
        print("Verifying SUTRAPATH.html...")
        page.goto("http://localhost:8000/SUTRAPATH.html")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="verification_sutrapath.png")

        browser.close()

if __name__ == "__main__":
    verify_mobile_layout()
