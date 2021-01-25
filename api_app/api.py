from flask import request
import flask
from flask.views import View
from flask_api import status
from utils import card_is_valid
from datetime import datetime
import random


app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Some exception in case of payment failure
class PaymentError(Exception):
    pass


# make calls to appropriate Payment Gateway passing all details
class process():
    
    def __init__(self,cnumber, cholder, amt, exp, scode):
        self.cnummber = cnumber
        self.cholder = cholder
        self.exp = exp
        self.scode = scode
        self.amt = float(amt)


    # select appropriate service, based on amount
    def choose_pay_service(self):
        if self.amt <= 20:  # for amount less than or equal 20
            try:
                self.cheap()
                return (True, "using CheapPaymentGateway")
            except PaymentError:
                return (False, "using CheapPaymentGateway")

            #return resp, "using CheapPaymentGateway"

        elif 500 >= self.amt >= 21:  # for amount between 21 and 500 (inclusive)
            try:  # try expensive if there
                self.expensive()
                return (True, "using ExpensivePaymentGateway")

            except PaymentError:  # else go for cheap
                try:
                    self.cheap()
                    return (True, "using CheapPaymentGateway")
                except PaymentError:
                    return (False, "using CheapPaymentGateway")

        elif self.amt > 500:  # for amount more than 500
            tries = 0
            resp = False
            while not resp and tries < 3:
                try:
                    self.premium()
                    return (True,"using PremiumPaymentGateway")
                except PaymentError:
                    pass
                tries += 1
            return (False, "using PremiumPaymentGateway")

    
    def cheap(self):  # cheap payment gateway
        n = random.randint(1, 30)
        if n == 3 or n == 9 or n == 6:
            raise PaymentError


    def expensive(self):  # expensive payment gateway
        n = random.randint(1, 30)
        if n == 3 or n == 9:
            raise PaymentError


    def premium(self):  # premium payment gateway
        n = random.randint(1, 30)
        if n == 3:
            raise PaymentError


class ProcessPayment(View):
    methods = ['POST']

    def dispatch_request(self):
        try:
            data = request.get_json()

            cardnumber = data.get('CreditCardNumber')
            if not cardnumber:
                return ("Error: No CreditCardNumber field provided. Please specify CreditCardNumber.", status.HTTP_400_BAD_REQUEST)
            if not card_is_valid(cardnumber):
                return ("Error: CardNumber is invalid. Please provide correct CreditCardNumber.", status.HTTP_400_BAD_REQUEST)
            
            cardholder =  data.get('CardHolder')
            if not cardholder:
                return ("Error: Card Holder is required.", status.HTTP_400_BAD_REQUEST)
            
            exp = data.get('ExpirationDate')
            if not exp:
                return ("Error: Expiration Date is required.", status.HTTP_400_BAD_REQUEST)
            try:
                exp_date = datetime.strptime(exp, '%m/%y')
            except ValueError:
                return ("Error: Expiration date format is mm/yy", status.HTTP_400_BAD_REQUEST)
            # Card is usually vaild through/ until not before.
            # But Acc. do instructions, exp must not be in past. 
            if exp_date < datetime.today():
                return ("Error: Card is expired.", status.HTTP_400_BAD_REQUEST)
        
            scode = data.get('SecurityCode')
            if scode:
                if not (scode.isdigit()):
                    return ("Error: invalid Security Code.", status.HTTP_400_BAD_REQUEST)
                if not (len(scode) == 3):
                    return ("Error: invalid Security Code. Security Code should be 3 digits.", status.HTTP_400_BAD_REQUEST)

            amount = data.get('Amount')  
            if not amount:
                return ("Error: No Amount field provided. Please specify an Amount.",status.HTTP_400_BAD_REQUEST)
            try:  # if not decimal raise 400
                float(amount)
            except:
                return ("Error: invalid amount", status.HTTP_400_BAD_REQUEST)

            if float(amount) < 0:  # if negative raise 400
                return ("Error: invalid amount(negative)", status.HTTP_400_BAD_REQUEST)

            pay_Class = process(cardnumber,cardholder,amount,exp, scode)
            result = pay_Class.choose_pay_service()
            # print("result", result)
            if result[0]:  # if True
                return ("Payment Processed " + result[1], status.HTTP_200_OK)
            else:  # if False
                return ("Payment Failed " + result[1], status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
        except Exception as e:
            return ("Unknown error occured.", status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


app.add_url_rule('/', view_func=ProcessPayment.as_view('processpayment'))

if __name__ == "__main__":
    app.run()
