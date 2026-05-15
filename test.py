import customtkinter

UAN_TO_USD = 0.0227
USD_TO_UAN = 44.17
BIGGER_TEXT = ("Arial", 26)

def convert_currency(amount, from_currency, to_currency):
    amount = float(amount)
    if from_currency == "UAN" and to_currency == "USD":
        result = amount * UAN_TO_USD
    elif from_currency == "USD" and to_currency == "UAN":
        result = amount * USD_TO_UAN
    else:        
        result = amount
    
    result_label.configure(text=f"{amount} {from_currency} = {result:.2f} {to_currency}")

root = customtkinter.CTk()
root.title("Currency Converter")
root.geometry("400x400")

amount_entry = customtkinter.CTkEntry(root, placeholder_text="Enter amount", font=BIGGER_TEXT)
amount_entry.pack(pady=10)

from_currency_var = customtkinter.StringVar(value="UAN")
from_currency_menu = customtkinter.CTkOptionMenu(root, variable=from_currency_var, values=["UAN", "USD"], font=BIGGER_TEXT)
from_currency_menu.pack(pady=10)
to_currency_var = customtkinter.StringVar(value="USD")
to_currency_menu = customtkinter.CTkOptionMenu(root, variable=to_currency_var, values=["UAN", "USD"], font=BIGGER_TEXT)
to_currency_menu.pack(pady=10)

convert_button = customtkinter.CTkButton(root, text="Convert", command=lambda: convert_currency(amount_entry.get(), from_currency_var.get(), to_currency_var.get()), font=BIGGER_TEXT)
convert_button.pack(pady=10)

result_label = customtkinter.CTkLabel(root, text="", font=BIGGER_TEXT)
result_label.pack(pady=10)
root.mainloop()