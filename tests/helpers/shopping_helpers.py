from playwright.sync_api import Page, expect
import re


def add_to_cart_by_item_number(page: Page, *item_numbers: str):
    for item_n in item_numbers:
        page.get_by_role("button", name="Add to cart").nth(item_n).click()


def go_to_cart(page: Page):
    cart_button = page.locator("span[role='button']").filter(has=page.locator("span.bg-qa-clr"))
    cart_button.click()
    expect(page).to_have_url(re.compile(".*cart.*"))


def check_cart_products_amount(page: Page, expected_amount: int):
    go_to_cart(page)

    # the amount of remove buttons should be the same as cart products
    remove_buttons = page.get_by_role("button", name=re.compile("remove", re.IGNORECASE))
    assert remove_buttons.count() == expected_amount


def get_cart_total_sum(page: Page) -> float:
    """
    Extract and sum all product totals from the cart page.
    Note: The structure is: <div class="w-[20%] text-center"><p>Total</p><p>$XX.XX</p></div>
    We find paragraphs with "Total" text and get their direct parent div to avoid matching ancestor divs.
    """
    total_labels = page.locator("p:has-text('Total')").all()
    
    total_sum = 0.0
    for label in total_labels:
        parent_div = label.locator("xpath=parent::div")
        
        price_paragraphs = parent_div.locator("p").all()
        for p in price_paragraphs:
            try:
                price_text = p.inner_text()
                if "$" in price_text and price_text.strip().lower() != "total":
                    price_value = float(re.sub(r'[^\d.]', '', price_text))
                    total_sum += price_value
                    break
            except Exception:
                continue
    
    return total_sum