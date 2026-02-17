from playwright.sync_api import Page, expect
from tests.helpers.shopping_helpers import (
    add_to_cart_by_item_number, 
    go_to_cart, 
    check_cart_products_amount,
    get_cart_total_sum,
    navigate_to_checkout_info,
    fill_checkout_form,
    continue_to_checkout_overview
)
import pytest
import re


@pytest.mark.smoke
@pytest.mark.regression
def test_user_can_add_items_to_cart(page: Page, setup_shopping_page):
    add_to_cart_by_item_number(page, 3, 4)
    go_to_cart(page)
    
    check_cart_products_amount(page, 2)


@pytest.mark.smoke
@pytest.mark.regression
def test_user_can_remove_items_from_cart_on_shopping_page(page: Page, setup_shopping_page):
    add_to_cart_by_item_number(page, 3, 4)
    page.get_by_role("button", name=re.compile("remove", re.IGNORECASE)).nth(0).click()

    check_cart_products_amount(page, 1)


@pytest.mark.regression
def test_user_can_remove_items_from_cart_on_cart_page(page: Page, setup_shopping_page):
    add_to_cart_by_item_number(page, 3, 4)
    go_to_cart(page)
    page.get_by_role("button", name=re.compile("remove", re.IGNORECASE)).nth(0).click()
    # confirm the removal
    page.get_by_role("button", name=re.compile("remove", re.IGNORECASE)).click()

    check_cart_products_amount(page, 1)


# TODO: test_user_can_remove_items_from_cart_by_decreasing_quantity


@pytest.mark.regression
@pytest.mark.fragile
def test_user_can_increase_decrease_quantity_of_items_in_cart(page: Page, setup_shopping_page):
    add_to_cart_by_item_number(page, 3)
    go_to_cart(page)
    product_quantity = page.locator("div.flex.justify-center.items-center.gap-2 > span")
    initial_item_price = get_cart_total_sum(page)

    assert initial_item_price > 0, f"Expected initial item price > 0"
    assert product_quantity.inner_text() == "1"

    plus_button = page.get_by_role("button", name="+")
    plus_button.click()

    assert product_quantity.inner_text() == "2"
    assert get_cart_total_sum(page) == initial_item_price * 2

    minus_button = page.get_by_role("button", name="-")
    minus_button.click()

    assert product_quantity.inner_text() == "1"
    assert get_cart_total_sum(page) == initial_item_price


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.fragile
def test_user_can_checkout(page: Page, setup_shopping_page):
    # Setup: Add items and go to cart
    add_to_cart_by_item_number(page, 3, 4)
    go_to_cart(page)
    cart_total = get_cart_total_sum(page)
    
    # Step 1: Navigate to checkout info page
    navigate_to_checkout_info(page)
    
    # Step 2: Verify form fields are present (quick check)
    # NOTE <label> tags are not associated with the <input> fields, so we need to use the placeholder text. Consider reporting it to be fixed
    first_name_field = page.get_by_placeholder(re.compile(".*john.*", re.IGNORECASE))
    last_name_field = page.get_by_placeholder(re.compile(".*doe.*", re.IGNORECASE))
    zip_code_field = page.locator('input[value="1207"]')
    expect(first_name_field).to_be_visible()
    expect(last_name_field).to_be_visible()
    expect(zip_code_field).to_be_visible()
    
    # Step 3: Fill form and continue
    fill_checkout_form(page)
    continue_to_checkout_overview(page)
    
    # Step 4: Verify navigation to overview and totals match
    total_before_tax_text = page.get_by_text(re.compile(".*item total.*", re.IGNORECASE)).inner_text()
    checkout_overview_item_total_before_tax = float(re.sub(r'[^\d.]', '', total_before_tax_text))
    assert abs(cart_total - checkout_overview_item_total_before_tax) < 0.01, \
        f"Cart total (${cart_total:.2f}) doesn't match checkout overview total (${checkout_overview_item_total_before_tax:.2f})"

    # Step 5: Complete checkout
    page.get_by_role("button", name="Finish").click()
    expect(page).to_have_url(re.compile(".*checkout.complete.*"))


@pytest.mark.regression
def test_user_can_cancel_checkout_on_info_page(page: Page, setup_shopping_page):
    # 1. Setup: Add items and go to cart
    add_to_cart_by_item_number(page, 3, 4)
    go_to_cart(page)
    initial_cart_items = page.get_by_role("button", name=re.compile("remove", re.IGNORECASE)).count()
    
    # 2. Navigate to checkout info page
    navigate_to_checkout_info(page)
    
    # 3. Cancel the checkout
    cancel_button = page.get_by_role("button", name=re.compile("cancel", re.IGNORECASE))
    cancel_button.click()
    
    # 4. Verify we're back on the cart page and items are still there
    expect(page).to_have_url(re.compile(".*cart.*"))
    check_cart_products_amount(page, initial_cart_items)


@pytest.mark.regression
def test_user_can_cancel_checkout_on_overview_page(page: Page, setup_shopping_page):
    # 1. Setup: Add items and go to cart
    add_to_cart_by_item_number(page, 3, 4)
    go_to_cart(page)
    
    # 2. Navigate through checkout info to overview
    navigate_to_checkout_info(page)
    fill_checkout_form(page)
    continue_to_checkout_overview(page)
    
    # 3. Cancel the checkout from overview page
    cancel_button = page.get_by_role("button", name=re.compile("cancel", re.IGNORECASE))
    cancel_button.click()
    
    # 4. Verify we're back on the checkout-info page
    expect(page).to_have_url(re.compile(".*checkout.info.*"))


# TODO: test_user_can_sort_items_in_cart
