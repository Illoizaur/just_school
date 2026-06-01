from flask import Flask, render_template_string
import requests

app = Flask(__name__)

PHP_API_URL = "https://justconsole.tech/python/api.php?table=users"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uk">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Паролі користувачів</title>

</head>
<body>

<h1>Паролі користувачів</h1>
{% for user in users %}

<p><strong>ім'я користувача:</strong> {{ user.username }} | <strong>пароль:</strong> {{ user.password

}}</p>
{% endfor %}

</body>
</html>
"""

@app.route('/', methods=['GET'])
def get_users():
    try:
        response = requests.get(PHP_API_URL)
        users = response.json() #Отримуємо список користувачів
        return render_template_string(HTML_TEMPLATE, users=users)

    except requests.exceptions.RequestException as e:

        return f"<p>Помилка при підключенні до сервера: {str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True, port=5001) 