from collections import defaultdict
from datetime import datetime


def calculate_basic_stats(transactions: list) -> dict:
    total_income = sum(float(transaction['Сумма'])
                       for transaction in transactions if float(transaction['Сумма']) > 0)
    total_expense = sum(float(transaction['Сумма'])
                        for transaction in transactions if float(transaction['Сумма']) < 0)
    balance = total_income + total_expense
    transaction_count = len(transactions)

    return {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'transaction_count': transaction_count
    }


def calculate_by_category(transactions: list) -> dict:
    category_stats = defaultdict(
        lambda: {'sum': 0, 'count': 0, 'expense_percent': 0, 'income_percent': 0})
   
    total_expense = sum(float(transaction['Сумма']) 
                        for transaction in transactions if float(transaction['Сумма']) < 0)
    total_income = sum(float(transaction['Сумма']) 
                       for transaction in transactions if float(transaction['Сумма']) > 0)

    for transaction in transactions:
        category = transaction['Категория']
        amount = float(transaction['Сумма'])
        
        category_stats[category]['sum'] += amount
        category_stats[category]['count'] += 1

    for category, data in category_stats.items():
        if data['sum'] < 0:
            data['expense_percent'] = (
                abs(data['sum']) / abs(total_expense) * 100) if total_expense != 0 else 0
            data['income_percent'] = 0
            
        else:
            data['income_percent'] = (
                data['sum'] / total_income * 100) if total_income != 0 else 0
            data['expense_percent'] = 0

    return dict(category_stats)


def analyze_by_time(transactions: list) -> dict:
    monthly_stats = defaultdict(lambda: {'income': 0, 'expenses': 0})

    for transaction in transactions:
        date_obj = datetime.strptime(transaction['Дата'], '%d.%m.%Y')
        month_str = date_obj.strftime('%Y-%m')
        amount = float(transaction['Сумма'])
        
        if amount > 0:
            monthly_stats[month_str]['income'] += amount
        else:
            monthly_stats[month_str]['expenses'] += abs(amount)

    return dict(monthly_stats)
