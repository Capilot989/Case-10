def analyze_historical_spending(transactions: list) -> dict:
    category = {}
    for transaction in transactions:
        cat = transaction.get('category', 'other')
        amount = transaction['amount']
        category.setdefault(cat, []).append(amount)
    average_spending = {cat: sum(val) / len(val) for cat, val in category.items()}
    total_spending = sum(sum(values) for values in category.values())
    recommendations = []
    for cat, avg in average_spending.items():
        percent = sum(category[cat]) / total_spending * 100
        if percent >= 30:
            recommendations.append(f'рекомендуем сократить расходы в категории {cat}:{percent:.1f}%')
    return {'average_spending': average_spending,
            'recommendations': recommendations
            }


def create_budget_template(analysis: dict, income: float) -> dict:
    average_spending = analysis['average_spending']
    average_total = sum(average_spending.values())
    budget = {cat: income * (val / average_total) for cat, val in average_spending.items()}
    budget['savings'] = income * 0.1
    return budget


def compare_budget_vs_actual(budget: dict, actual_transactions: list) -> dict:
    actual_by_category = {}
    for actual_transaction in actual_transactions:
        cat = actual_transaction.get('category', 'other')
        actual_by_category[cat] = actual_by_category.get(cat, 0) + actual_transaction['amount']
    comparison = {}
    for cat, planned in budget.items():
        actual = actual_by_category.get(cat, 0)
        diff = planned - actual
        comparison[cat] = {'actual': actual,
                           'planned': planned,
                           'diff': diff,
                           'status': 'in budget' if diff >= 0 else 'not in budget'
                           }
    return comparison


def print_financial_report(income, transactions, analysis, budget, comparison):
    total_spending = sum(t['amount'] for t in transactions)
    balance = income - total_spending
    print('income:', income)
    print('spending:', total_spending)
    print('balance:', balance)
    for cat, val in analysis['average_spending'].items():
        total = sum(t['amount'] for t in transactions if t['category'] == cat)
        percent = (total / total_spending) * 100 if total_spending else 0
        print(f'{cat}:{total} {percent:.1f}%')
    if analysis['recommendations']:
        for r in analysis['recommendations']:
            print(' -', r)
    else:
        print('no recommendations')
    for cat, infa in comparison.items():
        print(f" -{cat}:plan-{infa['planned']:.1f}, actual-{infa['actual']:.1f}, status:{infa['status']}")


transactions = [
    {"date": "2024-01-15", "amount": 15000.0, "category": "Еда"},
    {"date": "2024-01-16", "amount": 3500.0, "category": "Транспорт"},
    {"date": "2024-01-17", "amount": 1200.0, "category": "Развлечения"},
    {"date": "2024-01-18", "amount": 4500.0, "category": "Здоровье"},
    {"date": "2024-01-18", "amount": 5500.0, "category": "Накопления"},
]
income = 50000

analysis = analyze_historical_spending(transactions)
budget = create_budget_template(analysis, income)
comparison = compare_budget_vs_actual(budget, transactions)
print_financial_report(income, transactions, analysis, budget, comparison)

