from collections import defaultdict
from datetime import datetime
from ru_local import *


def calculate_basic_stats(transactions: list) -> dict:
    """
    Calculate basic financial statistics from transactions data.
    
    Args:
        transactions (list): List of transaction dictionaries with 'Сумма' key
        
    Returns:
        dict: Dictionary containing:
            - 'total_income': Total positive transaction amounts
            - 'total_expense': Total negative transaction amounts  
            - 'balance': Difference between income and expense
            - 'transaction_count': Total number of transactions
    """
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
    """
    Calculate detailed statistics grouped by transaction categories.
    
    Args:
        transactions (list): List of transaction dictionaries with 'Сумма' and 'Категория' keys
        
    Returns:
        dict: Dictionary with categories as keys and statistics as values including:
            - 'sum': Total amount per category
            - 'count': Number of transactions per category
            - 'expense_percent': Percentage of total expenses for expense categories
            - 'income_percent': Percentage of total income for income categories
    """
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
    """
    Analyze transactions by monthly time periods.
    
    Args:
        transactions (list): List of transaction dictionaries with 'Дата' and 'Сумма' keys
        
    Returns:
        dict: Dictionary with months as keys (format: 'YYYY-MM') and values containing:
            - 'income': Total income for the month
            - 'expenses': Total expenses for the month (positive values)
    """
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
