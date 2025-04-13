from menu import *
import json
import pandas as pd
# import api_requests_and_dump as api

if __name__ == "__main__":
    bank_names = json.load(open("bank_names\\en.json", "r"))
    currency_names = json.load(open("exchange_names\\en.json", "r"))

    df = pd.read_csv("csv\\raw_data.csv")
    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")
    df["bank"] = df["bank"].apply(lambda name: bank_names.get(name, None))
    df["currency"] = df["currency"].apply(lambda code: currency_names.get(code, None))
    df.dropna(inplace=True)

    app = QApplication(sys.argv)
    window = CryptoExchangeGUI(df)
    window.show()
    app.exec()
