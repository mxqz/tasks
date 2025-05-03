from datetime import datetime, timedelta
import requests
import json
import os
import tldextract as tld
import pandas as pd
import layout


class RequestError(Exception):
    def __init__(self):
        super().__init__("Request Failure")


def ensure_extension(file_name: str, extension: str) -> None:
    extension = extension.lower()
    if not extension.isalpha():
        return
    ext = "." + extension
    if not file_name.endswith(ext):
        file_name += ext
    return file_name


def dump_json_shortcut(data: dict | list, path: str, sort: bool = False) -> None:  
    path = ensure_extension(path, "json")
    
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, sort_keys=sort)
    
    print(f"Дані збережено у файл: {path}")


def gather_json_from(url: str):
    try:    
        response = requests.get(url)
    except:
        print("Відсутнє інтернет з'єднання")
        raise RequestError

    if response.status_code != 200:
        domain = tld.extract(url).domain
        print(f"Не вдалося отримати дані {domain}")
        raise RequestError
    
    return response.json()


def gather_and_dump(url: str, path: str) -> None:
    data = gather_json_from(url)
    if not isinstance(data, list):
        data = [data]
    file_name = ensure_extension(tld.extract(url).domain, "json")
    dump_json_shortcut(data, os.path.join(path, file_name))


def parse_json_to_df(path: str, dataframe_method) -> pd.DataFrame:
    path = ensure_extension(path, "json")
    data = json.load(open(path, "r", encoding="utf-8"))
    return dataframe_method(data)


def sorted_unique(df: pd.Series) -> list:
    return sorted(df.unique().tolist())


translation = json.load(open("exchange_names\\codes.json"))
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

    df = pd.DataFrame(rows, columns = df_columns)
    df.dropna(inplace=True)

    return df


def dataframe_monobank(data: list, name: str = "mono") -> pd.DataFrame:
    global translation
    rows = []
    translate = dict(zip(translation.values(), translation.keys()))

    for item in data:
        if translate.get(item.get("currencyCodeB")) != "UAH":
            continue
        date = datetime.fromtimestamp(float(item.get("date"))).strftime("%d.%m.%Y")
        rows.append(dict(zip(df_columns, [
            name,
            date,
            translate.get(item.get("currencyCodeA")),
            item.get("rateBuy"),
            item.get("rateSell")
        ])))

    df = pd.DataFrame(rows, columns = df_columns)
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

    df = pd.DataFrame(rows, columns = df_columns)
    df.dropna(inplace=True)

    return df


def request_csv_reading(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)

    try:
        data["date"] = pd.to_datetime(data["date"], format="%d.%m.%Y")
        data["bank"] = data["bank"].apply(lambda name: layout.bank_names.get(name, None))
        data["currency"] = data["currency"].apply(lambda code: layout.currency_names.get(code, None))
    except:
        request_csv_and_jsons_clear(path)

    data.dropna(inplace=True)
    data.sort_values(by=["bank", "date"], inplace=True)

    return data


url_dict = json.load(open("config\\url.json", "r"))
bank_dict = dict(zip(url_dict.keys(), [
    dataframe_bank,
    dataframe_monobank,
    dataframe_privatbank
]))

data = pd.DataFrame(columns=df_columns)


def parse_jsons_to_csv(path_to: str, path_from: str, bank_dict: dict = bank_dict) -> None:
    info = pd.concat([parse_json_to_df(os.path.join(path_from, f"{bank}.json"), bank_dict[bank]) for bank in bank_dict], 
                     join="inner", ignore_index=True)
    
    try:
        info = pd.concat([info, pd.read_csv(path_to)], join="inner", ignore_index=True).drop_duplicates(["bank", "date", "currency"])
    except:
        pass
    
    info.dropna(inplace=True)
    info["date"] = pd.to_datetime(data["date"], format="%d.%m.%Y")
    info.sort_values(["bank", "date"], inplace=True)
    info["date"] = info["date"].dt.strftime("%d.%m.%Y")

    info.to_csv(path_to, index=False)


def request_jsons_for_dates(start: datetime, end: datetime, path: str) -> None:  
    global url_dict

    gather_and_dump(url_dict["bank"].format(start.strftime("%Y%m%d"), end.strftime("%Y%m%d")), path)

    gather_and_dump(url_dict["monobank"], path)

    days = (end - start).days + 1
    privat_file = ensure_extension(tld.extract(url_dict["privatbank"]).domain, "json")
    privat_info = []
    for date in [start + timedelta(day) for day in range(days)]:
        try:
            info = gather_json_from(url_dict["privatbank"].format(date.strftime("%d.%m.%Y")))
        except RequestError:
            break
        else:
            privat_info.append(info)
    dump_json_shortcut(privat_info, os.path.join(path, privat_file))
    

def request_external_csv_update(start: datetime, end: datetime, path_to: str, path_from: str) -> None:
    global data
    request_jsons_for_dates(start, end, path_from)
    parse_jsons_to_csv(path_to, path_from)
    data = request_csv_reading(path_to)


domains = ["bank", "monobank", "privatbank"]


def request_csv_and_jsons_clear(path: str) -> None:
    if not os.path.exists(path):
        return
    
    for domain in domains:
        open(f"exchange_rates\\{domain}.json", "w").close()
    
    line = ",".join(df_columns) + "\n"
    
    with open(path, "w") as file:
        file.write(line)
