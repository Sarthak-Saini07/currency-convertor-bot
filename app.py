# from flask import Flask, render_template, request
# import requests
# import os

# app = Flask(__name__)

# class CurrencyConvertor:
#     rates = {}
    
#     def __init__(self, url):
#         data = requests.get(url).json()
#         self.rates = data["rates"]
    
#     def convert(self, from_currency, to_currency, amount):
#         initial_amount = amount
#         if from_currency != 'EUR':
#             amount = amount / self.rates[from_currency]
#         amount = round(amount * self.rates[to_currency], 2)
#         return amount

# API_KEY = 'e911fba6f5cd3ebfb999c1bca1c692a1'
# URL = f'http://data.fixer.io/api/latest?access_key={API_KEY}'

# @app.route('/')
# def landing():
#     return render_template('landing.html')

# @app.route('/converter', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         amount = float(request.form['amount'])
#         from_currency = request.form['from_currency']
#         to_currency = request.form['to_currency']
        
#         converter = CurrencyConvertor(URL)
#         converted_amount = converter.convert(from_currency, to_currency, amount)
        
#         return render_template('result.html', 
#                              amount=amount,
#                              from_currency=from_currency,
#                              to_currency=to_currency,
#                              converted_amount=converted_amount)
    
#     data = requests.get(URL).json()
#     currencies = list(data['rates'].keys())
#     return render_template('index.html', currencies=currencies)

# if __name__ == '__main__':
#     app.run(debug=True)






# from flask import Flask, render_template, request
# import requests
# import os

# app = Flask(__name__)

# class CurrencyConvertor:
#     rates = {}
#     base_currency = 'EUR'  # Fixer.io uses EUR as base
    
#     def __init__(self, url):
#         data = requests.get(url).json()
#         self.rates = data["rates"]
#         print("Latest rates loaded:", self.rates)  # Debug output
    
#     def convert(self, from_currency, to_currency, amount):
#         try:
#             # Convert from source currency to EUR (base currency)
#             if from_currency != self.base_currency:
#                 if from_currency not in self.rates:
#                     raise ValueError(f"Unsupported currency: {from_currency}")
#                 amount_in_eur = amount / self.rates[from_currency]
#             else:
#                 amount_in_eur = amount
            
#             # Convert from EUR to target currency
#             if to_currency != self.base_currency:
#                 if to_currency not in self.rates:
#                     raise ValueError(f"Unsupported currency: {to_currency}")
#                 converted_amount = amount_in_eur * self.rates[to_currency]
#             else:
#                 converted_amount = amount_in_eur
            
#             return round(converted_amount, 2)
            
#         except Exception as e:
#             print(f"Conversion error: {str(e)}")
#             raise

# # Use your actual API key
# API_KEY = 'e911fba6f5cd3ebfb999c1bca1c692a1'
# URL = f'http://data.fixer.io/api/latest?access_key={API_KEY}&symbols=USD,INR,EUR,GBP,JPY,AUD,CAD'  # Add more currencies as needed

# @app.route('/')
# def landing():
#     return render_template('landing.html')

# @app.route('/converter', methods=['GET', 'POST'])
# def index():
#     error = None
#     converted_amount = None
    
#     if request.method == 'POST':
#         try:
#             amount = float(request.form['amount'])
#             from_currency = request.form['from_currency']
#             to_currency = request.form['to_currency']
            
#             converter = CurrencyConvertor(URL)
#             converted_amount = converter.convert(from_currency, to_currency, amount)
            
#         except ValueError as e:
#             error = str(e)
#         except Exception as e:
#             error = f"An error occurred: {str(e)}"
    
#     try:
#         data = requests.get(URL).json()
#         currencies = sorted(data['rates'].keys())
#         currencies.insert(0, 'EUR')  # Ensure EUR is first
#     except Exception as e:
#         error = f"Failed to fetch currency data: {str(e)}"
#         currencies = ['EUR', 'USD', 'INR']  # Fallback currencies
    
#     return render_template('index.html', 
#                          currencies=currencies,
#                          converted_amount=converted_amount,
#                          error=error)

# if __name__ == '__main__':
#     app.run(debug=True)






from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

class CurrencyConvertor:
    rates = {}
    
    def __init__(self, url):
        data = requests.get(url).json()
        self.rates = data["rates"]
        self.base = data["base"]  # Store the base currency
    
    def convert(self, from_currency, to_currency, amount):
        try:
            # If converting from base currency
            if from_currency == self.base:
                return round(amount * self.rates[to_currency], 2)
            
            # If converting to base currency
            if to_currency == self.base:
                return round(amount / self.rates[from_currency], 2)
            
            # Cross-currency conversion
            amount_in_base = amount / self.rates[from_currency]
            return round(amount_in_base * self.rates[to_currency], 2)
            
        except KeyError as e:
            raise ValueError(f"Invalid currency code: {e}")

API_KEY = 'e911fba6f5cd3ebfb999c1bca1c692a1'
URL = f'http://data.fixer.io/api/latest?access_key={API_KEY}&symbols=USD,INR,EUR,GBP'

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/converter', methods=['GET'])
def converter_form():
    data = requests.get(URL).json()
    currencies = list(data['rates'].keys())
    currencies.insert(0, data['base'])  # Add base currency first
    return render_template('index.html', currencies=currencies)

@app.route('/convert', methods=['POST'])
def convert_currency():
    try:
        amount = float(request.form['amount'])
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        
        converter = CurrencyConvertor(URL)
        converted_amount = converter.convert(from_currency, to_currency, amount)
        
        return render_template('result.html',
                            amount=amount,
                            from_currency=from_currency,
                            to_currency=to_currency,
                            converted_amount=converted_amount)
    
    except Exception as e:
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)