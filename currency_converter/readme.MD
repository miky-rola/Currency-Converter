# Currency Converter Application
This Django application allows users to convert amounts from one currency to another using real-time exchange rates obtained from an external API. The application supports user-friendly currency names and converts them to ISO 4217 codes for API requests.

## Features
- Convert amounts between different currencies.
- User-friendly input for common currency names.
- Real-time exchange rates fetched from an external API.
- Error handling for invalid inputs and API request issues.
- Displays the conversion rate and the converted amount.

## Prerequisites
- Python 3.x
- Django
- Requests library
- python-dotenv library

## Setup
**Clone the repository:**
`git clone https://github.com/miky-rola/Currency-Converter.git`


**Create and activate a virtual environment:**
`python -m venv venv`
`source venv/bin/activate ` # On Mac 
`venv\Scripts\activate` # On Windows 

**Install the required packages:**
`pip install -r requirements.txt`

`Set up environment variables:`
Create a .env file in the project root directory and add your API key and API URL.

`api_key=YOUR_API_KEY_HERE`
`API`=API_URL_HERE
`api=API`

Ensure the currency_code.csv file is present:
Place the currency_code.csv file in the converter directory. This file should contain currency names and their corresponding ISO 4217 codes in CSV format.

**Run the Django server:**
`python manage.py runserver`

Access the application:
Open your web browser and navigate to http://127.0.0.1:8000.

## Usage
**Convert Currency:**
1. Enter the amount you want to convert.
2. Enter the currency you are converting from.
3. Enter the currency you are converting to.
4. Click the "Convert" button to see the result.

**Error Handling:**
- Ensure all fields are filled out.
- Enter a valid numeric amount.
- Verify the entered currencies are supported.
- Project Structure

***converter/: Contains the Django application code.***
***views.py: Contains the main logic for converting currencies and handling API requests.***
***currency_code.csv: CSV file mapping common currency names to ISO 4217 codes.***
***templates/converter/: Contains HTML templates.***
***index.html: Main template for the currency converter interface.***


## Contributing
Feel free to open issues or submit pull requests with improvements or bug fixes. Ensure your contributions adhere to the project's coding standards.

For any questions or further assistance, please contact [(https://github.com/miky-rola)| (mikyrola8@gmail.com)].
