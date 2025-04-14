import requests
import json
import os
from datetime import datetime, timedelta
import tldextract as tld
import pandas as pd


class RequestError(Exception):
    def __init__(self):
        super().__init__("Request Failure")


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
        raise RequestError
    
    return response.json()


def gather_and_dump(url: str, script_dir: str ="") -> None:
    data = gather_json_from(url)
    if not isinstance(data, list):
        data = [data]
    domain = tld.extract(url).domain
    dump_json_shortcut(data, f"{domain}", script_dir)


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


def sorted_unique(df: pd.Series) -> list:
    return sorted(df.unique())


locals = json.load(open("config\\en.json", "r"))
url_dict = json.load(open("config\\url.json", "r"))
bank_names = json.load(open("bank_names\\en.json", "r"))
currency_names = json.load(open("exchange_names\\en.json", "r"))
bank_dict = dict(zip(url_dict.keys(), [
    dataframe_bank,
    dataframe_monobank,
    dataframe_privatbank
]))

data = pd.read_csv("csv\\raw_data.csv")

data["date"] = pd.to_datetime(data["date"], format="%d.%m.%Y")
data["bank"] = data["bank"].apply(lambda name: bank_names.get(name, None))
data["currency"] = data["currency"].apply(lambda code: currency_names.get(code, None))

data.dropna(inplace=True)


def parse_jsons_to_csv(bank_dict: dict = bank_dict, file_name: str = "raw_data.csv") -> None:
    info = pd.concat([parse_json_to_df(f"exchange_rates\\{bank}.json", bank_dict[bank]) for bank in bank_dict], 
                     join="inner", ignore_index=True)
    
    if not file_name.endswith(".csv"):
        file_name += ".csv"

    path = f"csv\\{file_name}"
    
    if open(path, "r"):
        info = pd.concat([info, pd.read_csv(path)], join="inner", ignore_index=True).drop_duplicates()
    
    info.dropna(inplace=True)
    
    info.to_csv(path, index=False)


def request_jsons_for_dates(start: datetime, end: datetime) -> None:  
    gather_and_dump(url_dict["bank"].format(start.strftime("%Y%m%d"), end.strftime("%Y%m%d")), "exchange_names")

    gather_and_dump(url_dict["monobank"], "exchange_names")

    days = (end - start).days
    privat_file = tld.extract(url_dict["privatbank"]).domain
    privat_info = []
    for date in [start + timedelta(day) for day in range(days)]:
        try:
            info = gather_json_from(url_dict["privatbank"].format(date.strftime("%d.%m.%Y")))
        except RequestError:
            break
        else:
            privat_info.append(info)
    dump_json_shortcut(privat_info, privat_file, "exchange_rates")
    

def request_external_csv_update(start: datetime, end: datetime, file_name: str = "raw_data.csv") -> None:
    request_jsons_for_dates(start, end)
    parse_jsons_to_csv(file_name=file_name)


if __name__ == "__main__":
    request_external_csv_update(datetime.strptime("01.04.2024", "%d.%m.%Y"), datetime.strptime("14.04.2025", "%d.%m.%Y"))
