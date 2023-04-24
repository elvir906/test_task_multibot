from dateutil.parser import parse

from weather import requests


def get_all_exchange_rates_erapi(src):
    """Получаем данные с API"""
    url = f"https://open.er-api.com/v6/latest/{src}"
    data = requests.get(url).json()
    if data["result"] == "success":
        last_updated_datetime = parse(data["time_last_update_utc"])
        exchange_rates = data["rates"]
    return last_updated_datetime, exchange_rates


def convert_currency_erapi(amount, src, dst):
    """Метод для конвертации."""
    last_updated_datetime, exchange_rates = get_all_exchange_rates_erapi(src)
    return last_updated_datetime, exchange_rates[dst] * amount
