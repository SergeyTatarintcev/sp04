from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

# Настройка драйвера
options = webdriver.FirefoxOptions()
options.add_argument("--headless")  # убрать, если хочешь видеть браузер
driver = webdriver.Firefox(options=options)

def open_article(topic):
    url = f"https://ru.wikipedia.org/wiki/{topic.replace(' ', '_')}"
    driver.get(url)
    time.sleep(2)
    return url

def get_paragraphs():
    content = driver.find_element(By.ID, "mw-content-text")
    paragraphs = content.find_elements(By.TAG_NAME, "p")
    return [p.text.strip() for p in paragraphs if p.text.strip()]

def get_links():
    content = driver.find_element(By.ID, "mw-content-text")
    links = content.find_elements(By.TAG_NAME, "a")
    filtered = []
    for link in links:
        href = link.get_attribute("href")
        if href and href.startswith("https://ru.wikipedia.org/wiki/") and ":" not in href:
            title = link.text.strip()
            if title:
                filtered.append((title, href))
    return filtered[:10]  # Покажем максимум 10

def main():
    print("🟦 Википедия-консоль 🌐")
    topic = input("Введите тему для поиска: ")
    open_article(topic)

    while True:
        print("\nЧто вы хотите сделать?")
        print("1. Читать параграфы статьи")
        print("2. Перейти на связанную статью")
        print("3. Выйти")
        choice = input("Ваш выбор (1/2/3): ")

        if choice == "1":
            paragraphs = get_paragraphs()
            if not paragraphs:
                print("Нет параграфов для отображения.")
                continue

            for i, p in enumerate(paragraphs):
                print(f"\n--- Параграф {i+1} ---")
                print(p)
                next_step = input("Нажмите Enter для следующего параграфа или введите 'q' для выхода: ")
                if next_step.lower() == 'q':
                    break

        elif choice == "2":
            links = get_links()
            if not links:
                print("Связанных статей не найдено.")
                continue

            print("\nДоступные внутренние ссылки:")
            for idx, (title, _) in enumerate(links, 1):
                print(f"{idx}. {title}")

            try:
                num = int(input("Введите номер статьи для перехода: "))
                if 1 <= num <= len(links):
                    driver.get(links[num-1][1])
                    time.sleep(2)
                else:
                    print("Неверный номер.")
            except ValueError:
                print("Нужно ввести число.")

        elif choice == "3":
            print("👋 Выход из программы.")
            break
        else:
            print("Некорректный выбор.")

    driver.quit()

if __name__ == "__main__":
    main()
