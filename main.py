from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time


def main():
    # Запрос у пользователя первоначального запроса
    query = input("Введите ваш запрос для поиска на Википедии: ")

    # Инициализация браузера (Firefox) с помощью менеджера драйверов
    browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    try:
        # Переход на сайт Википедии с первоначальным запросом
        browser.get(f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}")
        time.sleep(5)  # Задержка для загрузки страницы

        while True:
            # Предлагаем пользователю варианты действий
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти из программы")
            choice = input("Введите номер действия: ")

            if choice == "1":
                # Листаем параграфы статьи
                paragraphs = browser.find_elements(By.XPATH, '//p')
                for i, paragraph in enumerate(paragraphs):
                    print(f"\nПараграф {i + 1}: {paragraph.text}\n\n")
                    if i < len(paragraphs) - 1:
                        input("Нажмите Enter для перехода к следующему параграфу...")
                continue

            elif choice == "2":
                # Переход на одну из связанных страниц
                links = browser.find_elements(By.XPATH, '//a[@href]')
                print(f"\nНайдены {len(links)} связанных страниц. Вот несколько примеров:")
                for i, link in enumerate(links[:5]):  # Показать первые 5 ссылок
                    print(f"{i + 1}. {link.text}")

                link_choice = input("\nВведите номер ссылки, чтобы перейти (или '0' для выхода): ")
                if link_choice.isdigit() and 0 < int(link_choice) <= len(links):
                    new_link = links[int(link_choice) - 1].get_attribute('href')
                    browser.get(new_link)
                    time.sleep(5)  # Задержка для загрузки новой страницы
                continue

            elif choice == "3":
                print("Выход из программы...")
                break

            else:
                print("Некорректный ввод, попробуйте снова.")

    finally:
        browser.quit()  # Закрытие браузера


if __name__ == "__main__":
    main()