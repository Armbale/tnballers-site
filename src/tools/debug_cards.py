#!/usr/bin/env python3
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True)
    page = browser.new_context(viewport={'width':1440,'height':900}).new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(('pageerror', str(e))))
    page.on('console', lambda m: errors.append(('console', m.type, m.text)))
    page.goto('http://localhost:8000/preview_home.html', wait_until='networkidle')
    page.wait_for_selector('.nine-open')
    print('--- JS errors / console ---')
    for e in errors[:30]:
        print(' ', e)
    print('--- modal before click ---')
    print(page.eval_on_selector('.nine-modal', 'el => ({hidden: el.hidden, display: getComputedStyle(el).display, hasOnClass: el.classList.contains("on")})') if page.query_selector('.nine-modal') else 'NO MODAL')
    print('--- click first card ---')
    page.click('.nine-open[data-i="0"]')
    page.wait_for_timeout(500)
    print(page.eval_on_selector('.nine-modal', 'el => ({hidden: el.hidden, display: getComputedStyle(el).display, hasOnClass: el.classList.contains("on"), opacity: getComputedStyle(el).opacity})'))
    print('--- recent errors ---')
    for e in errors[-10:]:
        print(' ', e)
    browser.close()
