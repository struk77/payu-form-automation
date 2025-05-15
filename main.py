import yaml
import argparse

import requests
from bs4 import BeautifulSoup


def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def main(config, order_id, phone, user_id):
    url = config["url"]
    user = next((u for u in config["users"] if u["id"] == user_id), None)

    if not user:
        print(f"Користувач із ID {user_id} не знайдений!")
        return

    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = session.get(url, headers=headers)
    # Отримуємо токен із Set-Cookie (XSRF-TOKEN)
    xsrf_token = response.cookies.get("XSRF-TOKEN")
    if not xsrf_token:
        print("Не вдалося знайти XSRF-TOKEN у відповіді")
        return

    # Витягуємо hidden `_token` із HTML
    soup = BeautifulSoup(response.text, "html.parser")
    hidden_token = soup.find("input", {"name": "_token"})["value"]
    if not hidden_token:
        print("Не вдалося знайти _token у HTML")
        return

    # Встановлюємо токен у заголовок X-XSRF-TOKEN
    headers["X-XSRF-TOKEN"] = xsrf_token

    payload = user
    payload["_token"] = hidden_token
    payload["order"] = order_id
    payload["phone"] = phone

    response = session.post(url, headers=headers, data=payload)

    soup = BeautifulSoup(response.text, "html.parser")

    # Debug: Save HTML to file
    with open("response.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    success_message = soup.find("div", class_="alert-success")
    error_message = soup.find("div", class_="alert-danger")
    if success_message:
        return success_message.text.strip()
    elif error_message:
        return error_message.text.strip()
    else:
        return "Не вдалося знайти повідомлення про результат операції"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Автоматизована відправка форми PayU")
    parser.add_argument("order_id", help="Номер замовлення")
    parser.add_argument("phone", help="Номер телефону")
    parser.add_argument(
        "user_id",
        type=int,
        nargs="?",
        default=1,
        help="ID користувача (за замовчуванням 1)",
    )
    args = parser.parse_args()

    # Завантаження конфігу
    config_path = "config.yaml"
    config = load_config(config_path)
    result = main(config, args.order_id, args.phone, args.user_id)
    print(result)
