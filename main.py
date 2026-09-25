import json
from uuid import uuid4

from colorama import Fore, Style, init
import requests

import http_client

DOG_RANDOM_IMAGE_URL = "https://dog.ceo/api/breeds/image/random"
CAT_RANDOM_IMAGE_URL = "https://cataas.com/cat"
PRODUCT_FIELDS = ("title", "price", "description")
SEPARATOR = "─" * 80


def is_product_list(data):
    return (
        isinstance(data, list)
        and all(isinstance(item, dict) for item in data)
        and any(all(field in item for field in PRODUCT_FIELDS) for item in data)
    )


def print_products(products):
    print(f"{Fore.CYAN}{Style.BRIGHT}\nНайдено товаров: {len(products)}{Style.RESET_ALL}")

    for index, product in enumerate(products, start=1):
        title = product.get("title")
        price = product.get("price")
        description = product.get("description")

        print(f"\n{Fore.BLUE}{SEPARATOR}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}Товар #{index}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}title:{Style.RESET_ALL} {title}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}price:{Style.RESET_ALL} {price}")
        print(f"{Fore.CYAN}{Style.BRIGHT}description:{Style.RESET_ALL} {description}")

    print(f"{Fore.BLUE}{SEPARATOR}{Style.RESET_ALL}")


def print_response(response):
    status_color = Fore.GREEN if response.ok else Fore.RED
    print(f"\n{Style.BRIGHT}Status code:{Style.RESET_ALL} {status_color}{response.status_code}{Style.RESET_ALL}")

    print(f"\n{Style.BRIGHT}Body:{Style.RESET_ALL}")
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(response.text)
        return

    if is_product_list(data):
        print_products(data)
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))


def get_url_from_user():
    url = input("Введите URL: ").strip()

    if not url:
        print("URL не может быть пустым.")
        return None

    return url


def get_json_body_from_user():
    raw_body = input("Введите JSON для POST-запроса или оставьте пустым для {}: ").strip()

    if not raw_body:
        return {}

    try:
        return json.loads(raw_body)
    except json.JSONDecodeError as error:
        print(f"Некорректный JSON: {error}")
        return None


def send_get_request():
    url = get_url_from_user()

    if url is None:
        return

    response = http_client.get(url)
    print_response(response)


def send_post_request():
    url = get_url_from_user()

    if url is None:
        return

    body = get_json_body_from_user()

    if body is None:
        return

    response = http_client.post(url, json=body)
    print_response(response)


def get_random_dog():
    dog_image_url = get_random_dog_image_url()

    if not dog_image_url:
        print("Не удалось получить ссылку на картинку с собакой.")
        return

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Посмотри случайную собачку по ссылке:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{dog_image_url}{Style.RESET_ALL}")


def get_random_cat():
    cat_image_url = get_random_cat_image_url()

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Посмотри случайного котика по ссылке:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{cat_image_url}{Style.RESET_ALL}")


def get_random_dog_image_url():
    response = http_client.get(DOG_RANDOM_IMAGE_URL)
    data = response.json()

    return data.get("message")


def get_random_cat_image_url():
    response = http_client.get(CAT_RANDOM_IMAGE_URL, params={"cache": uuid4().hex})

    return response.url


def print_menu():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Тестер HTTP запросов{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1{Style.RESET_ALL} - Получить случайную собачку")
    print(f"{Fore.YELLOW}2{Style.RESET_ALL} - Получить случайного котика")


def main():
    init(autoreset=True)

    while True:
        print_menu()
        choice = input("Выберите пункт меню или введите q для выхода: ").strip().lower()

        try:
            if choice == "1":
                get_random_dog()
            elif choice == "2":
                get_random_cat()
            elif choice == "q":
                print("Завершение работы.")
                break
            else:
                print("Неизвестный пункт меню. Введите 1, 2 или q.")
        except requests.exceptions.RequestException as error:
            print(f"Ошибка запроса: {error}")


if __name__ == "__main__":
    main()
