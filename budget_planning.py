from ru_local import *


def analyze_historical_spending(transactions: list) -> dict:
    category = {}
    
    for transaction in transactions:
        cat = transaction.get('Категория', OTHER)
        amount = float(transaction['Сумма'])  # Преобразование строки в число
        category.setdefault(cat, []).append(amount)
        
    average_spending = {cat: sum(val) / len(val) for cat, val in category.items()}
    total_spending = sum(sum(values) for values in category.values())
    recommendations = []
    
    for cat, avg in average_spending.items():
        percent = sum(category[cat]) / total_spending * 100
        if percent >= 30:
            recommendations.append(f'{RECOMMEND_REDUCE_SPENDING} {cat}: {percent:.1f}%')
            
    return {'average_spending': average_spending,
            'recommendations': recommendations
            }


def create_budget_template(analysis: dict, income: float) -> dict:
    average_spending = analysis['average_spending']
    average_total = sum(average_spending.values())
    budget = {cat: income * (val / average_total) for cat, val in average_spending.items()}
    budget[SAVINGS] = income * 0.1
    
    return budget


def compare_budget_vs_actual(budget: dict, actual_transactions: list) -> dict:
    actual_by_category = {}
    
    for actual_transaction in actual_transactions:
        cat = actual_transaction.get('Категория', OTHER)
        amount = float(actual_transaction['Сумма'])  # Преобразование строки в число
        actual_by_category[cat] = actual_by_category.get(cat, 0) + amount
        
    comparison = {}
    
    for cat, planned in budget.items():
        actual = actual_by_category.get(cat, 0)
        diff = planned - actual
        comparison[cat] = {ACTUAL: actual,
                           PLANNED: planned,
                           'diff': diff,
                           STATUS: IN_BUDGET if diff >= 0 else OVER_BUDGET
                           }
        
    return comparison


def print_financial_report(income, transactions, analysis, budget, comparison):
    total_spending = sum(float(t['Сумма']) for t in transactions)  # Преобразование строки в число
    balance = income - total_spending
    
    print(f'{INCOME}: {income}')
    print(f'{EXPENSES}: {total_spending}')
    print(f'{BALANCE}: {balance}')
    
    for cat, val in analysis['average_spending'].items():
        total = sum(float(t['Сумма']) for t in transactions if t['Категория'] == cat)  # Преобразование
        percent = (total / total_spending) * 100 if total_spending else 0
        print(f'{cat}: {total} {percent:.1f}%')
    
    if analysis['recommendations']:
        for r in analysis['recommendations']:
            print(' -', r)
    else:
        print(NO_RECOMMENDATIONS)
    
    for cat, infa in comparison.items():
        print(f" - {cat}: {PLANNED} - {infa[PLANNED]:.1f}, {ACTUAL} - {infa[ACTUAL]:.1f}, {STATUS}: {infa[STATUS]}")
