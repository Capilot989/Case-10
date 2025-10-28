def create_categories() -> dict:
    """
        Create a dictionary of transaction categories with their associated keywords.

        Returns:
            dict: Dictionary where keys are category names and values are lists
                  of keywords associated with each category.
        """
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
    return OTHER


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
