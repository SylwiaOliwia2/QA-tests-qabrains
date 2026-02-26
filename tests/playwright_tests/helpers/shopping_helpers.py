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


def navigate_to_checkout_info(page: Page):
    page.get_by_role("button", name=re.compile("checkout", re.IGNORECASE)).click()
    expect(page).to_have_url(re.compile(".*checkout.info.*"))


def fill_checkout_form(page: Page, first_name: str = "Anna", last_name: str = "Fabulous", zip_code: str = "12345"):
    """
    Fill the checkout form with provided information.
    
    Args:
        first_name: First name to fill in
        last_name: Last name to fill in
        zip_code: Zip code to fill in
    """
    first_name_field = page.get_by_placeholder(re.compile(".*john.*", re.IGNORECASE))
    last_name_field = page.get_by_placeholder(re.compile(".*doe.*", re.IGNORECASE))
    zip_code_field = page.locator('input[value="1207"]')
    
    first_name_field.fill(first_name)
    last_name_field.fill(last_name)
    zip_code_field.fill(zip_code)


def continue_to_checkout_overview(page: Page):
    page.get_by_role("button", name="Continue").click()
    expect(page).to_have_url(re.compile(".*checkout.overview.*"), timeout=30000)