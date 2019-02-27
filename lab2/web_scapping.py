import time

from selenium import webdriver
from selenium.common.exceptions import\
    NoSuchElementException,\
    StaleElementReferenceException,\
    ElementNotVisibleException


class ShopItem:
    def __init__(self, raw_element):
        self.brand = raw_element\
            .find_element_by_class_name(name='productdescriptionbrand')\
            .get_attribute('innerHTML')

        self.name = raw_element\
            .find_element_by_class_name('productdescriptionname')\
            .get_attribute('innerHTML')

        self.price = raw_element\
            .find_element_by_class_name('CurrencySizeLarge') \
            .get_attribute('innerHTML')

    def __str__(self):
        return '{0}: {1} for {2}'.format(self.brand, self.name, self.price)


# Close the sportsdirect add that pops up.
def close_add(driver):
    popup = driver.find_element_by_id('advertPopup')
    popup.find_element_by_class_name('close').click()


# Extract all the items from the current page
def extract_items_from_page(driver):
    elements_list = driver.find_element_by_id('navlist')
    elements_meat = elements_list.find_elements_by_class_name('s-productthumbtext')

    items = []
    for element in elements_meat:
        item = ShopItem(element)
        items.append(item)
        print(item)

    return items


# Wait for certain condition
def wait_for(condition_function, timeout=3, interval=0.1):
    start_time = time.time()
    while time.time() < start_time + timeout:
        if condition_function():
            return True
        else:
            time.sleep(interval)
    raise Exception('Timeout waiting for {}'.format(condition_function.__name__))


# Click to go to the next page. If no such button was found, return -1
def click_on_next(driver):
    try:
        btn = driver.find_element_by_class_name('swipeNextClick')
    except NoSuchElementException:
        return -1

    btn.click()

    def link_has_gone_stale():
        try:
            btn.find_elements_by_id('whatever')
            return False
        except StaleElementReferenceException:
            return True

    wait_for(link_has_gone_stale, 10)
    return 0


def print_results(items):
    if len(items) == 0:
        print('No items were found')
        return

    print('{0} element{1} were found'.format(
        len(items),
        's' if len(items) == 1 else ''
    ))
    print('The smallest item:', items[0])

    i = 1
    for item in items:
        print('{0}) {1}'.format(i, item))
        i += 1


base_url = 'https://md.sportsdirect.com/SearchResults?DescriptionFilter={0}&dppp=100&OrderBy=price_asc'
item_to_search = 'pants'
base_url = base_url.format(item_to_search)


if __name__ == '__main__':
    scraped_data = []

    with webdriver.Chrome() as driver:
        driver.get(base_url)

        try:
            close_add(driver)
        except ElementNotVisibleException:
            print("No add was found")

        while True:
            try:
                scraped_data.extend(extract_items_from_page(driver))
            except Exception:
                break

            if click_on_next(driver) == -1:
                break

            print('Going to the next page. Total elements {0}'.format(len(scraped_data)))

    print_results(scraped_data)
