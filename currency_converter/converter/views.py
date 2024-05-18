import os
import requests
from django.shortcuts import render
from dotenv import load_dotenv
import csv
from django.conf import settings

load_dotenv()

API_KEY = os.getenv("api_key")

API = os.getenv("api")

# Initialize an empty dictionary to store currency codes
currency_codes = {}

# Specify the absolute file path of the CSV file
file_path = settings.BASE_DIR / "converter/currency_code.csv"

# Print the file path and check if the file exists for debugging purposes
print(f"File path: {file_path}")
print(f"File exists: {os.path.isfile(file_path)}")

# Try to read the CSV file and populate the dictionary
try:
    with open(file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            key, value = row
            currency_codes[key] = value
    print("CSV file read successfully.")
except FileNotFoundError:
    print("FileNotFoundError: The CSV file was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

def get_currency_code(name):
    """Convert common currency names to ISO 4217 codes."""
    return currency_codes.get(name.lower(), name.upper())

def convert_currency(request):
    context = {}
    if request.method == 'POST':
        # Get the form data
        from_currency = request.POST.get("from_currency").upper()
        to_currency = request.POST.get("to_currency").upper()
        amount = request.POST.get("amount")

        # Debugging prints
        print(f"From Currency: {from_currency}")
        print(f"To Currency: {to_currency}")
        print(f"Amount: {amount}")

        # Convert common currency names to ISO 4217 codes
        from_currency = get_currency_code(from_currency)
        to_currency = get_currency_code(to_currency)


        # Validate input fields
        if not from_currency or not to_currency or not amount:
            context["error"] = "Please fill in all fields."
            return render(request, "converter/index.html", context)

    
        try:
            amount = float(amount)
        except ValueError:
            context["error"] = "Please enter a valid amount."
            return render(request, "converter/index.html", context)

        # Get API key from environment variables
        url = f"{API}/{API_KEY}/latest/{from_currency}"

        try:
            # Make a request to the Exchange Rate API
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            print(f"API Response: {data}")

            # Check if the target currency is in the response
            if to_currency in data["conversion_rates"]:
                conversion_rate = data["conversion_rates"][to_currency]
                converted_amount = amount * conversion_rate
                context = {
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "amount": amount,
                    "converted_amount": converted_amount,
                    "rate": conversion_rate
                }
            else:
                context["error"] = "Currency not found in the response."
        except requests.exceptions.HTTPError as http_err:
            context["error"] = f"HTTP error occurred: {http_err}"
        except requests.exceptions.RequestException as req_err:
            context["error"] = f"Request error occurred: {req_err}"
        except ValueError:
            context["error"] = "Invalid response from the API."

        
        print(f"Context: {context}")

    # Render the template with the context
    context["currency_codes"] = currency_codes
    print(context)
    return render(request, "converter/index.html", context)