# Імпортуємо необхідні бібліотеки
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

# Приклад колекції документів (список текстів)
documents = [
    "Машинне навчання з використанням алгоритмів",
    "Алгоритм машинного навчання для обробки даних",
    "Моделі машинного навчання для класифікації"
]

# Створюємо об'єкт TfidfVectorizer
vectorizer = TfidfVectorizer()

# Підраховуємо TF-IDF для кожного слова в кожному документі
tfidf_matrix = vectorizer.fit_transform(documents)

# Перетворюємо результат у масив
tfidf_array = tfidf_matrix.toarray()

# Отримуємо список термінів
terms = vectorizer.get_feature_names_out()

# Створюємо DataFrame для зручності відображення
df = pd.DataFrame(tfidf_array, columns=terms)

# Виводимо отриману матрицю TF-IDF
print(df)
