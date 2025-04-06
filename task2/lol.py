import requests
import json
from datetime import datetime, timedelta, date
import os

# Вказуємо діапазон дат ПРАЦЮЄ ЛИШЕ З НБУ
start_date = datetime(2025, 3, 1)
end_date = datetime(2025, 4, 5)

# Валюти для отримання курсів
currency_codes = ["usd", "eur", "pln"]
results = []

current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y%m%d")
    formatted_date = current_date.strftime("%d.%m.%Y")
    daily_rates = {"date": formatted_date}

    for code in currency_codes:
        url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={code}&date={date_str}&json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data:
                rate = data[0]["rate"]
                daily_rates[data[0]["cc"]] = rate
            else:
                print(f"Немає даних за {formatted_date} для {code.upper()}")
        else:
            print(f"Помилка при запиті {code.upper()} на {formatted_date}")
    
    results.append(daily_rates)
    current_date += timedelta(days=1)

script_dir = os.path.dirname(os.path.abspath(__file__))
file_name = f"exchange_rates_{start_date.strftime('%d.%m.%Y')}-{end_date.strftime('%d.%m.%Y')}.json"
full_path = os.path.join(script_dir, file_name)

# Записуємо JSON у файл
with open(full_path, "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

print(f"Курси валют збережено у файл: {full_path}")

privat_url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date.today().strftime('%d.%m.%Y')}"
response = requests.get(privat_url)
privat_data = {}

if response.status_code == 200:
    data = response.json()
    for code in currency_codes:
        for item in data.get("exchangeRate", []):
            if item.get("currency") == code.upper():
                privat_data[code.upper()] = {
                    "purchase": item.get("purchaseRate", None),
                    "sale": item.get("saleRate", None)
                }
else:
    print("Не вдалося отримати дані з ПриватБанку")

# Зберігаємо у файл
privat_file = os.path.join(script_dir, "exchange_rates_PrivatBank.json")
with open(privat_file, "w", encoding="utf-8") as file:
    json.dump(privat_data, file, indent=4, ensure_ascii=False)
print(f"Курси з ПриватБанку збережено: {privat_file}")

# --- Монобанк ---
mono_url = "https://api.monobank.ua/bank/currency"
response = requests.get(mono_url)
mono_data = {}
currency_map = {"usd": 840, "eur": 978, "pln": 985}

if response.status_code == 200:
    data = response.json()
    for item in data:
        for code, num in currency_map.items():
            if item.get("currencyCodeA") == num and item.get("currencyCodeB") == 980:
                mono_data[code.upper()] = {
                    "rateBuy": item.get("rateBuy", None),
                    "rateSell": item.get("rateSell", None)
                }
else:
    print("Не вдалося отримати дані з Монобанку")

# Зберігаємо у файл
mono_file = os.path.join(script_dir, "exchange_rates_Monobank.json")
with open(mono_file, "w", encoding="utf-8") as file:
    json.dump(mono_data, file, indent=4, ensure_ascii=False)
print(f"Курси з Монобанку збережено: {mono_file}")
