import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="session")
def driver():
    # Инициализация ChromeDriver (убедитесь, что ChromeDriver установлен и добавлен в PATH)
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 60)

def test_search_product(driver, wait):
    """
    Тест 1: Поиск товара 'флешка'
    Шаги: Открыть Wildberries, ввести 'флешка' в поиск, нажать Enter, проверить, что карточки товаров отображаются.
    """
    driver.get("https://www.wildberries.ru/")
    search_field = wait.until(EC.visibility_of_element_located((By.ID, "searchInput")))
    search_field.clear()
    search_field.send_keys("флешка")
    search_field.send_keys(Keys.ENTER)
    
    product_cards = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, "#catalog > div > div.catalog-page__main.new-size > div.catalog-page__content > div.product-card-overflow > div")
))
    assert len(product_cards) > 0, "Карточки товаров не найдены"

def test_add_to_cart(driver, wait):
    """
    Тест 2: Добавление товара в корзину
    Шаги: Открыть Wildberries, найти товар 'флешка', перейти на карточку товара, нажать кнопку 'Добавить в корзину',
           перейти в корзину и проверить, что товар присутствует.
    """
    driver.get("https://www.wildberries.ru/")
    search_field = wait.until(EC.visibility_of_element_located((By.ID, "searchInput")))
    search_field.clear()
    search_field.send_keys("флешка")
    search_field.send_keys(Keys.ENTER)
    
    # Ожидаем загрузку карточек товаров
    product_cards = wait.until(EC.presence_of_all_elements_located(
    (By.CSS_SELECTOR, "#catalog > div > div.catalog-page__main.new-size > div.catalog-page__content > div.product-card-overflow > div")
))
    assert len(product_cards) > 0, "Карточки товаров не найдены"
    product_cards[0].click()
    
    # Ожидание и клик по кнопке "Добавить в корзину"
    add_to_cart = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".j-add-to-basket")))
    driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart)
    driver.execute_script("arguments[0].click();", add_to_cart)
    time.sleep(2)  # Задержка для обработки добавления товара
    
    # Переход в корзину
    basket_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "div.navbar-pc__item.j-item-basket a.navbar-pc__link")
    ))
    basket_button.click()
    
    # Проверка, что товар присутствует в корзине (поиск по названию товара)
    basket_item = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//span[contains(@class, 'good-info__good-name') and "
                   "contains(translate(., 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ', 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'), 'флешка')]")
    ))
    assert "флешка" in basket_item.text.lower(), "Товар не найден в корзине"

