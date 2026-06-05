import schedule
import time


def send_reminder():
    print("Нагадування: час зробити перерву! ⏳")


# Налаштовуємо частоту нагадування
schedule.every(5).seconds.do(send_reminder)

while True:
    schedule.run_pending()  # Перевірка, чи потрібно виконати завдання
    time.sleep(1)  # Затримка для економії ресурсів