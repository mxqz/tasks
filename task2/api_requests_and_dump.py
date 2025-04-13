import requests
import json
import os
from datetime import datetime, timedelta, date
import tldextract as tld
import pandas as pd


def dump_json_shortcut(data: dict | list, file_name: str, script_dir: str = "", sort: bool = False) -> None:
    if not script_dir:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if not file_name.endswith(".json"):
        file_name += ".json"
    
    full_path = os.path.join(script_dir, file_name)

    print(full_path)

    with open(full_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, sort_keys=sort)
    
    print(f"Дані збережено у файл: {file_name}")


def gather_json_from(url: str):
    response = requests.get(url)

    if response.status_code != 200:
        domain = tld.extract(url).domain
        print(f"Не вдалося отримати дані {domain}")
    
    return response.json()


def gather_and_dump(url: str, script_dir: str ="") -> None:
    data = gather_json_from(url)
    if not isinstance(data, list):
        data = [data]
    domain = tld.extract(url).domain
    dump_json_shortcut(data, f"exchange_rates_{domain}", script_dir)


df_columns = ["bank", "date", "currency", "rate_buy", "rate_sell"]


def dataframe_bank(data: list, name: str = "bank") -> pd.DataFrame:
    rows = []

    for item in data:
        rows.append(dict(zip(df_columns, [
            name,
            item.get("exchangedate"),
            item.get("cc"),
            item.get("rate"),
            item.get("rate")
        ])))

    df = pd.DataFrame(rows)
    df.dropna(inplace=True)

    return df


def dataframe_monobank(data: list, name: str = "mono") -> pd.DataFrame:
    rows = []

    translation = json.load(open("config\\exchange_codes.json"))
    translation = dict(zip(translation.values(), translation.keys()))

    for item in data:
        if translation.get(item.get("currencyCodeB")) != "UAH":
            continue
        date = datetime.fromtimestamp(float(item.get("date"))).strftime("%d.%m.%Y")
        rows.append(dict(zip(df_columns, [
            name,
            date,
            translation.get(item.get("currencyCodeA")),
            item.get("rateBuy"),
            item.get("rateSell")
        ])))

    df = pd.DataFrame(rows)
    df.dropna(inplace=True)

    return df


def dataframe_privatbank(data: list, name: str = "privat") -> pd.DataFrame:   
    rows = []

    for item in data:
        date = item.get("date")
        base_currency = item.get("baseCurrencyLit")
        if base_currency != "UAH":
            continue
        for exchange in item.get("exchangeRate"):
            rows.append(dict(zip(df_columns, [
                name,
                date,
                exchange.get("currency"),
                exchange.get("purchaseRate", exchange.get("purchaseRateNB")),
                exchange.get("saleRate", exchange.get("saleRateNB"))
            ])))

    df = pd.DataFrame(rows)
    df.dropna(inplace=True)

    return df


def parse_json_to_df(path: str, dataframe_method) -> pd.DataFrame:
    if not path.endswith(".json"):
        path += ".json"
    data = json.load(open(path, "r", encoding="utf-8"))
    return dataframe_method(data)

# data[data.isna().any(axis=1)]

# nbu_url = f"https://bank.gov.ua/NBU_Exchange/exchange_site?start={(date.today() - timedelta(7)).strftime("%Y%m%d")}&end={date.today().strftime("%Y%m%d")}&json"
# mono_url = f"https://api.monobank.ua/bank/currency"
# privat_url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date.today().strftime("%d.%m.%Y")}"

# # urls = [nbu_url, privat_url, mono_url]

# # for url in urls:
# #     gather_and_dump(url)

bank_dict = {
    "": dataframe_bank,
    "mono": dataframe_monobank,
    "privat": dataframe_privatbank
}

if __name__ == "__main__":
    # data = pd.concat([parse_json_df(f"exchange_rates\\exchange_rates_{bank}bank.json", bank_dict[bank]) for bank in bank_dict], join="inner", ignore_index=True)
    # data.to_csv("raw_data.csv", index=False)

    # currencies: dict = json.load(open("exchange_names\\ua.json", "r"))
    # bank_names: dict = json.load(open("bank_names\\ua.json", "r"))

    # data = pd.read_csv("csv\\raw_data.csv")
    # data["currency"] = data["currency"].apply(lambda code: currencies.get(code, None))
    # data["bank"] = data["bank"].apply(lambda bank: bank_names.get(bank, None))
    # data.dropna(inplace=True)

    # print(*sorted(data["currency"].unique()), sep="\n", end="\n\n")
    # print(*sorted(data["bank"].unique()), sep="\n", end="\n\n")

    pass
