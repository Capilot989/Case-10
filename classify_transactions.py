def create_categories() -> dict:
    """
        Create a dictionary of transaction categories with their associated keywords.

        Returns:
            dict: Dictionary where keys are category names and values are lists
                  of keywords associated with each category.
        """
    categories = {
        "Супермаркеты": [
            "пятерочка", "магнит", "перекресток",
            "лента", "ашан", "метро", "окей", "дикси",
            "вкусВилл", "билла", "быстроном", "ярче"
        ],

        "Фастфуд": [
            "вкусно и точка", "rostic's", "теремок",
            "академия кофе", "бургер кинг", "хан буз",
            "свиток"
        ],

        "Ресторан": [
            "якитория", "чайхона", "шоколадница",
            "кофемания"
        ],

        "Такси": [
            "яндекс.такси", "такси maxim", "uber"
        ],

        "Каршеринг": [
            "каршеринг", "ситимобил"
        ],

        "Общественный транспорт": [
          "метро", "аэроэкспресс", "ппк", "мцд"
        ],

        "ЖКХ": [
            "новосибэнергосбыт", "моэк", "ростелеком", "мгтс",
            "дом.ru", "новосибводоканал"
        ],

        "Связь": [
            "мтс", "tele2", "мегафон", "билайн"
        ],

        "Онлайн кинотеатры": [
            "ivi", "oko", "kinopub"
        ],

        "Онлайн-сервисы": [
            "яндекс.плюс", "vk", "steam",
            "youtube premium", "apple music", "spotify"
        ],

        "Маркетплейсы": [
            "ozon", "wildberries", "яндекс.маркет"
        ],

        "Развлечения": [
            "кинотеатр", "арена", "цирк", "парк", "зоопарк"
        ],

        "Магазины электроники": [
            "м.видео", "эльдорадо", "связной", "евросеть",
            "dns"
        ],

        "Зарплата": [
            "зарплата"
        ],

        "Переводы": [
            "перевод"
        ]
    }
    return categories

def categorize_transaction(description: str, categories: dict) -> str:
    """
        Categorize a transaction based on its description.

        Args:
            description (str): Transaction description text
            categories (dict): Dictionary of categories and their keywords

        Returns:
            str: Category name if a match is found, otherwise "Other"
        """
    lower_descr = description.lower()
    for category, key_words in categories.items():
        if any(key_word in lower_descr for key_word in key_words):
            return category
    return "Другое"

def categorize_all_transactions(transactions: list) -> list:
    """
       Categorize all transactions in the provided list.

       Args:
           transactions (list): List of transaction dictionaries

       Returns:
           list: List of transactions with added 'Category' field
       """
    all_categories = create_categories()
    update_transactions = []

    for transaction in transactions:
        description = transaction['Описание']
        category = categorize_transaction(description, all_categories)
        transaction['Категория'] = category
        update_transactions.append(transaction)
        
    return update_transactions
