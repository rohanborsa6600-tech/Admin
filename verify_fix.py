
from playwright.sync_api import sync_playwright, expect
import os
import json
import re
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Mock Firebase calls
    def handle_route(route):
        url = route.request.url
        print(f"Intercepted: {url}")
        if "/users/TEST_USER.json" in url:
            route.fulfill(status=200, body=json.dumps({"granted": True, "isBlocked": False, "name": "Test User"}))
        elif "/users/TEST_USER/access.json" in url:
            # Grant access to all books
            perms = {
                "Geeta Bhashy": True,
                "Sthalpothi": True,
                "Sumanmala": True,
                "Sutrapath": True,
                "Vachan Sambandh": True,
                "Vichar Sthal": True
            }
            route.fulfill(status=200, body=json.dumps(perms))
        elif "library_catalog.json" in url:
            route.fulfill(status=200, body="{}")
        else:
            route.continue_()

    page.route("**/*", handle_route)

    # 1. Load the page
    page.goto("http://localhost:8000")

    # 2. Simulate login state
    page.evaluate("localStorage.setItem('bv_uid', 'TEST_USER')")
    page.evaluate("localStorage.setItem('bv_name', 'Test User')")

    # 3. Reload to trigger checkAccess and dashboard load
    page.reload()

    # 4. Wait for dashboard and verify book list
    print("Waiting for dashboard...")
    expect(page.locator("#dashboard-screen")).to_have_class(re.compile(r"active"))

    # Wait for book list to be populated
    expect(page.locator("#book-list .book-item")).to_have_count(6)
    print("Book list verified.")
    page.screenshot(path="dashboard_with_books.png")

    # 5. Open a book (Geeta Bhashy)
    print("Opening Geeta Bhashy...")
    page.locator("text=Geeta Bhashy").click()

    # Wait for reader screen
    expect(page.locator("#reader-screen")).to_have_class(re.compile(r"active"))

    # Wait for content to load. Since we are injecting a full HTML, let's wait for a specific element from GEETA BHASHY.html
    # We know it has <div class="book-title">...</div>
    try:
        page.wait_for_selector(".book-title", timeout=5000)
        print("Book content loaded (found .book-title).")
    except:
        print("Warning: .book-title not found, checking if #book-content has children...")
        # Just check if #book-content is not empty
        content = page.locator("#book-content").inner_html()
        if len(content) > 100:
             print("Book content loaded (length > 100).")
        else:
             print(f"Book content seems empty or too short: {content[:100]}")
             # We might have failed to load the file if the server is not serving it correctly?
             # But the intercept log showed it was requested.

    page.screenshot(path="reader_geeta.png")

    # 6. Go back
    print("Going back...")
    page.locator(".fa-arrow-left").click()

    # Wait for dashboard
    expect(page.locator("#dashboard-screen")).to_have_class(re.compile(r"active"))

    # 7. Verify #book-content is empty
    # We need to give it a moment as the innerHTML = "" happens in the same tick as class switching, but let's be sure.
    time.sleep(0.5)
    content = page.locator("#book-content").inner_html()
    print(f"Book content after back: '{content}'")
    if content == "":
        print("PASS: Book content cleared.")
    else:
        print("FAIL: Book content NOT cleared.")

    page.screenshot(path="dashboard_after_back.png")

    browser.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        run(p)
