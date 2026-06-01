from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

PHP_API_URL = "https://justconsole.tech/python/api.php?table=users"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uk">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Форма входу</title>

</head>
<body>

<h1>Вхід на сайт</h1>

{% if error %}

<p style="color: red;">{{ error }}</p>

{% endif %}

<form method="POST">

<input type="text" name="username" placeholder="Ім'я користувача" required><br><br>
<input type="password" name="password" placeholder="Пароль" required><br><br>
<button type="submit">Увійти</button>

</form>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

    try:
        # Отримуємо список користувачів з API
        response = requests.get(PHP_API_URL)
        users = response.json()

        # Перевіряємо, чи є такий користувач і чи співпадає пароль
        for user in users:

            if user['username'] == username and user['password'] == password:

                return f"<h1>Вітаємо, {username}!</h1>" # Успішний вхід

            # Якщо користувача немає або пароль не співпав
            return render_template_string(HTML_TEMPLATE, error="Невірне ім'я користувача або пароль.")

    except requests.exceptions.RequestException as e:
        return f"<p>Помилка при підключенні до сервера: {str(e)}</p>"

    return render_template_string(HTML_TEMPLATE, error=None)

if __name__ == '__main__':
    app.run(debug=True, port=5001)