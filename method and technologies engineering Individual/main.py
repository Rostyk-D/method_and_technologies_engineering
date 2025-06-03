import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Завантаження даних
file_path = 'Retail_and_wherehouse_Sale.csv'
data = pd.read_csv(file_path)

# Видалення рядків із пропусками в колонці SUPPLIER
data = data.dropna(subset=['SUPPLIER'])

# Завантаження даних у таблицю sales_data
db_path = 'sales_database.db'
db_connection = sqlite3.connect(db_path)
cursor = db_connection.cursor()

data.to_sql('sales_data', db_connection, if_exists='replace', index=False)

# Вибір ознак і цільової змінної
features = data[['YEAR', 'MONTH', 'ITEM_TYPE', 'WAREHOUSE_SALES', 'RETAIL_TRANSFERS']]
target = data['RETAIL_SALES']

# Розділення даних на тренувальні та тестові
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=41)

# Перетворення категоріальних даних у числові
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['YEAR', 'MONTH', 'WAREHOUSE_SALES', 'RETAIL_TRANSFERS']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['ITEM_TYPE']),
    ])

# Список моделей регресії
models = {
    'Linear Regression': LinearRegression(),
    'Ridge Regression': Ridge(alpha=1.0),
    'Lasso Regression': Lasso(alpha=0.1),
    'Decision Tree': DecisionTreeRegressor(max_depth=5, random_state=41),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=41)
}

# Створення полотна для всіх моделей
plt.figure(figsize=(12, 8))

# Зберігання метрик для кожної моделі
metrics_results = []

for model_name, model_instance in models.items():
    # Побудова пайплайна
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', model_instance)
    ])

    # Навчання моделі
    pipeline.fit(X_train, y_train)

    # Прогнозування
    predictions = pipeline.predict(X_test)

    # Обчислення метрик
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    r2_cross = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='r2', n_jobs=-1).mean()

    # Друк метрик у консоль
    print(f"Model: {model_name}")
    print(f"  MAE: {mae}")
    print(f"  MSE: {mse}")
    print(f"  R2: {r2}")
    print(f"  R2 (Cross-Validation): {r2_cross}")
    print()

    predictions_data = list(zip(y_test, predictions))
    table_name = f'predictions{model_name.replace(' ', '').lower()}'

    cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (actual_sales REAL, predicted_sales REAL)')
    cursor.executemany(f'INSERT INTO {table_name} (actual_sales, predicted_sales) VALUES (?, ?)', predictions_data)
    db_connection.commit()

    # Додавання графіків для кожної моделі
    plt.scatter(y_test, predictions, alpha=0.6, label=model_name)

# Додавання загальної інформації на графік
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label='Ідеальна лінія')
plt.xlabel('Фактичні значення (RETAIL SALES)')
plt.ylabel('Прогнозовані значення (RETAIL SALES)')
plt.title('Фактичні vs Прогнозовані значення для різних моделей')
plt.legend()
plt.grid(alpha=0.4)
plt.show()

# Закриття з'єднання з базою даних
db_connection.close()
print("Аналіз завершено, з'єднання з базою даних закрито.")
