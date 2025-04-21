import requests

def test_currency_api():
    url = 'https://v1.apiplugin.io/v1/currency/kJi6dj9r/rates'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Выводим полный ответ для понимания структуры
        print("Ответ API:", data)

        # Предполагаем, что курсы лежат в data['rates']
        rates = data.get('rates', {})
        if not rates:
            print("Ключ 'rates' не найден или пуст.")
            return

        print("Курсы валют относительно USD:")
        for currency, rate in rates.items():
            print(f"{currency}: {rate}")

    except requests.RequestException as e:
        print("Ошибка запроса к API:", e)

if __name__ == "__main__":
    test_currency_api()
