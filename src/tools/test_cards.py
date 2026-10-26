#!/usr/bin/env python3
"""Headless click-test for the FUT cards: open all 8, verify the modal, close with Esc."""
import sys
from playwright.sync_api import sync_playwright

URL = 'http://localhost:8000/preview_home.html'

def run():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={'width':1440,'height':900})
        page = ctx.new_page()
        page.goto(URL, wait_until='domcontentloaded')
        page.wait_for_selector('.nine-open', state='visible', timeout=10000)

        cards = page.query_selector_all('.nine-open')
        print(f'Found {len(cards)} cards')
        results = []
        for i, card in enumerate(cards):
            name = (card.get_attribute('aria-label') or '').split(',')[0]
            card.scroll_into_view_if_needed()
            card.click()
            # Wait for modal to appear + show title
            try:
                page.wait_for_selector('.nine-modal:not([hidden]) #nineMTitle', timeout=4000)
                title = page.text_content('.nine-modal:not([hidden]) #nineMTitle') or ''
                ok = name.strip().lower() in title.lower()
                results.append((i, name, title.strip(), ok))
                print(f'  [{i}] {name!r:35}  modal={title.strip()!r}  ok={ok}')
            except Exception as e:
                results.append((i, name, None, False))
                print(f'  [{i}] {name!r} FAILED: {e}')
                page.screenshot(path=f'/tmp/card-fail-{i}.png')
            # Close with Esc
            page.keyboard.press('Escape')
            try:
                page.wait_for_selector('.nine-modal[hidden]', timeout=2000)
            except Exception:
                print(f'  [{i}] WARN: modal did not close')

        total = len(results); ok = sum(1 for r in results if r[3])
        print(f'\n{ok}/{total} cards passed')
        browser.close()
        return 0 if ok == total else 1

if __name__ == '__main__':
    sys.exit(run())
