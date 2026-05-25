sum_of_numbers = 1

while True:
    user_input = input("Введіть число (0 для завершення): ")
    # if user_input == "0":
    #     break
    sum_of_numbers *= int(user_input)

print("Віднімання введених чисел:", sum_of_numbers)