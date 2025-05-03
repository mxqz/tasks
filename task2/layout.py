import json

raw_data = "csv\\raw_data.csv"
raw_exchange_rates = "exchange_rates\\"
stylesheet = "config\\themes\\{}.qss"
config = json.load(open("config\\config.json", "r"))
languages = config["available_lang"]
lang = config["selected_lang"]
locals = None
bank_names = None
currency_names = None

def set_localization(choice: str) -> None:
    global lang, locals, bank_names, currency_names
    if choice != lang:
        lang = choice
        config["selected_lang"] = lang
        json.dump(config, open("config\\config.json", "w"), indent=4)
    locals = json.load(open(f"config\\lang\\{lang}.json", "r", encoding="utf-8"))
    bank_names = json.load(open(f"bank_names\\{lang}.json", "r", encoding="utf-8"))
    currency_names = json.load(open(f"exchange_names\\{lang}.json", "r", encoding="utf-8"))

set_localization(lang)
