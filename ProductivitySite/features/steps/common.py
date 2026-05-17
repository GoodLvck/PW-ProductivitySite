from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _wait(context, timeout=10):
    return WebDriverWait(context.browser.driver, timeout)


def _click_button(context, text):
    label = text.strip().lower()
    driver = context.browser.driver

    aliases = {
        "new subject": "create subject",
        "sign in": "log in",
    }
    label = aliases.get(label, label)

    # Elementos del menú flotante
    if label in ("edit", "delete"):
        # Solo abre el toggle si el menú no está ya visible
        menu = driver.find_elements(By.CSS_SELECTOR, "#floating-actions-menu")
        menu_visible = menu and menu[0].is_displayed()

        if not menu_visible:
            toggle = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".floating-actions-toggle"))
            )
            toggle.click()


        if label == "edit":
            el = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     "//*[contains(@class, 'floating-actions-item')][.//span[normalize-space(text())='Edit']]")
                )
            )
            el.click()
            return

        el = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 f"//*[contains(@class, 'floating-actions-item')][.//span[normalize-space(text())='{label.title()}']]")
            )
        )
        el.click()
        return

    # Busca botones y enlaces
    try:
        el = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//*[self::button or self::a][normalize-space(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))='{label}']")
            )
        )
        el.click()
        return
    except Exception:
        pass

    # Fallback: submit button
    try:
        el = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        el.click()
    except Exception as e:
        raise AssertionError(f"Could not find button or link '{text}': {e}")