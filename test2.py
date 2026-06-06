def generate_text(prompt):
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "command-xlarge-nightly", # Використовується модель для генерації тексту
        "prompt": prompt,
        "max_tokens": 100, # Максимальна кількість токенів
    }
    try:
        response = requests.post(COHERE_API_URL, json=data, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            generation = response_data["text"]
            return generation

    except Exception as e:
        return f"Помилка: {e}"

