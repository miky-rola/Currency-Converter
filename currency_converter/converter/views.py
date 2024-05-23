import os
import requests
from django.shortcuts import render
from dotenv import load_dotenv
import csv
from django.conf import settings
import logging


load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("api_key")
API = os.getenv("api")
LOCATION_API = os.getenv("location_api")
TOKEN = os.getenv("api_token")

# Initialize an empty dictionary to store currency codes
currency_codes = {}

# Specify the absolute file paths of the CSV files
currency_code_file_path = settings.BASE_DIR / "converter/currency_code.csv"
country_currency_file_path = settings.BASE_DIR / "converter/country_currency.csv"


# Function to read CSV file and populate a dictionary
def read_csv_to_dict(file_path):
    data_dict = {}
    try:
        with open(file_path, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                key, value = row
                data_dict[key] = value
        logger.info(f"CSV file {file_path} read successfully.")
    except FileNotFoundError:
        logger.error(f"FileNotFoundError: The CSV file {file_path} was not found.")
    except Exception as e:
        logger.error(f"An error occurred while reading {file_path}: {e}")
    return data_dict

# Populate dictionaries from CSV files
currency_codes = read_csv_to_dict(currency_code_file_path)
country_currency = read_csv_to_dict(country_currency_file_path)


def get_currency_code(name):
    """Convert common currency names to ISO 4217 codes."""
    return currency_codes.get(name.lower(), name.upper())

def get_country_currency():
    url = f"{LOCATION_API}={TOKEN}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"IPInfo API Response: {data}")
        if "country" in data:
            country = data["country"]
            currency = country_currency.get(country)
            logger.info(f"Detected Country: {country}, Currency: {currency}")
            return currency
        else:
            logger.error("Country information not found in the response.")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error occurred: {e}")
        return None

def convert_currency(request):
    context = {}
    default_currency = get_country_currency()
    context["default_currency"] = default_currency

    if request.method == 'POST':
        # Get the form data
        from_currency = request.POST.get("from_currency", "").upper()
        to_currency = request.POST.get("to_currency", "").upper()
        amount = request.POST.get("amount")

        # Use default currency if not provided
        from_currency = from_currency if from_currency else default_currency
        to_currency = to_currency if to_currency else default_currency

        # Debugging logs
        logger.info(f"From Currency: {from_currency}")
        logger.info(f"To Currency: {to_currency}")
        logger.info(f"Amount: {amount}")
        logger.info(f"Default Currency (from user's country): {default_currency}")

        # Convert common currency names to ISO 4217 codes
        from_currency = get_currency_code(from_currency)
        to_currency = get_currency_code(to_currency)

        # Validate input fields
        if not from_currency or not to_currency or not amount:
            context["error"] = "Please fill in all fields."
            context["currency_codes"] = currency_codes
            context["from_currency"] = from_currency
            context["to_currency"] = to_currency
            return render(request, "converter/index.html", context)

        try:
            amount = float(amount)
        except ValueError:
            context["error"] = "Please enter a valid amount."
            context["currency_codes"] = currency_codes
            context["from_currency"] = from_currency
            context["to_currency"] = to_currency
            return render(request, "converter/index.html", context)

        # Get API key from environment variables
        url = f"{API}/{API_KEY}/latest/{from_currency}"

        try:
            # Make a request to the Exchange Rate API
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            logger.info(f"API Response: {data}")

            # Check if the target currency is in the response
            if to_currency in data["conversion_rates"]:
                conversion_rate = data["conversion_rates"][to_currency]
                converted_amount = amount * conversion_rate
                context.update({
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "amount": amount,
                    "converted_amount": converted_amount,
                    "rate": conversion_rate
                })
            else:
                context["error"] = "Currency not found in the response."
        except requests.exceptions.HTTPError as http_err:
            context["error"] = f"HTTP error occurred: {http_err}"
        except requests.exceptions.RequestException as req_err:
            context["error"] = f"Request error occurred: {req_err}"
        except ValueError:
            context["error"] = "Invalid response from the API."

        logger.info(f"Context: {context}")

    # Ensure context includes currency codes even if no conversion was made
    context["currency_codes"] = currency_codes
    if "from_currency" not in context:
        context["from_currency"] = default_currency
    if "to_currency" not in context:
        context["to_currency"] = default_currency

    return render(request, "converter/index.html", context)
