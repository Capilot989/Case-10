from collections import defaultdict
from datetime import datetime
from ru_local import *


def calculate_basic_stats(transactions: list) -> dict:
    total_income = sum(float(transaction['Сумма'])
                       for transaction in transactions if float(transaction['Сумма']) > 0)
    total_expense = sum(float(transaction['Сумма'])
                        for transaction in transactions if float(transaction['Сумма']) < 0)
    balance = total_income + total_expense
    transaction_count = len(transactions)

    return {
        TOTAL_INCOME: total_income,
        TOTAL_EXPENSE: total_expense,
        BALANCE: balance,
        TRANSACTION_COUNT: transaction_count
    }


def calculate_by_category(transactions: list) -> dict:
    category_stats = defaultdict(
        lambda: {SUM: 0, COUNT: 0, EXPENSE_PERCENT: 0, INCOME_PERCENT: 0})
    
    total_expense = sum(float(transaction['Сумма']) 
                        for transaction in transactions if float(transaction['Сумма']) < 0)
    total_income = sum(float(transaction['Сумма']) 
                       for transaction in transactions if float(transaction['Сумма']) > 0)

    for transaction in transactions:
        category = transaction['Категория']
        amount = float(transaction['Сумма'])
        
        category_stats[category][SUM] += amount
        category_stats[category][COUNT] += 1

    for category, data in category_stats.items():
        if data[SUM] < 0:
            data[EXPENSE_PERCENT] = (
                abs(data[SUM]) / abs(total_expense) * 100) if total_expense != 0 else 0
            data[INCOME_PERCENT] = 0
        else:
            data[INCOME_PERCENT] = (
                data[SUM] / total_income * 100) if total_income != 0 else 0
            data[EXPENSE_PERCENT] = 0

    return dict(category_stats)


def analyze_by_time(transactions: list) -> dict:
    monthly_stats = defaultdict(lambda: {INCOME: 0, EXPENSES: 0})

    for transaction in transactions:
        date_obj = datetime.strptime(transaction['Дата'], DATE_FORMAT)
        month_str = date_obj.strftime(MONTH_FORMAT)
        amount = float(transaction['Сумма'])
        
        if amount > 0:
            monthly_stats[month_str][INCOME] += amount
        else:
            monthly_stats[month_str][EXPENSES] += abs(amount)

    return dict(monthly_stats)


def create_categories() -> dict:
    categories = {
        SUPERMARKETS: [
            "пятерочка", "магнит", "перекресток",
            "лента", "ашан", "метро", "окей", "дикси",
            "вкусвилл", "билла", "быстроном", "ярче"
        ],
        FAST_FOOD: [
            "вкусно и точка", "rostic's", "теремок",
            "академия кофе", "бургер кинг", "хан буз",
            "свиток"
        ],
        RESTAURANT: [
            "якитория", "чайхона", "шоколадница",
            "кофемания"
        ],
        TAXI: [
            "яндекс.такси", "такси maxim", "uber"
        ],
        CARSHARING: [
            "каршеринг", "ситимобил"
        ],
        PUBLIC_TRANSPORT: [
          "метро", "аэроэкспресс", "ппк", "мцд"
        ],
        UTILITIES: [
            "новосибэнергосбыт", "моэк", "ростелеком", "мгтс",
            "дом.ru", "новосибводоканал"
        ],
        MOBILE: [
            "мтс", "tele2", "мегафон", "билайн"
        ],
        ONLINE_CINEMA: [
            "ivi", "oko", "kinopub"
        ],
        ONLINE_SERVICES: [
            "яндекс.плюс", "vk", "steam",
            "youtube premium", "apple music", "spotify"
        ],
        MARKETPLACES: [
            "ozon", "wildberries", "яндекс.маркет"
        ],
        ENTERTAINMENT: [
            "кинотеатр", "арена", "цирк", "парк", "зоопарк"
        ],
        ELECTRONICS: [
            "м.видео", "эльдорадо", "связной", "евросеть",
            "dns"
        ],
        SALARY: [
            "зарплата"
        ],
        TRANSFERS: [
            "перевод"
        ]
    }
    return categories


def categorize_transaction(description: str, categories: dict) -> str:
    lower_descr = description.lower()
    for category, key_words in categories.items():
        if any(key_word in lower_descr for key_word in key_words):
            return category
    return OTHER


def categorize_all_transactions(transactions: list) -> list:
    all_categories = create_categories()
    update_transactions = []

    for transaction in transactions:
        description = transaction['Описание']
        category = categorize_transaction(description, all_categories)
        transaction['Категория'] = category
        update_transactions.append(transaction)
        
    return update_transactions
