from flask import request
import flask
from flask.views import View
from flask_api import status
from utils import card_is_valid  # to validate card. 
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
            try:  # try expensive if available
                self.expensive()
                return (True, "using ExpensivePaymentGateway")

            except PaymentError:  # else go for cheap
                try:
                    self.cheap()
                    return (True, "using CheapPaymentGateway")
                except PaymentError:
                    return (False, "using CheapPaymentGateway")

        elif self.amt > 500:  # for amount more than 500
            tries = 0 # 
            resp = False
            while not resp and tries < 3:  # three tries on premium
                try:
                    self.premium()
                    return (True,"using PremiumPaymentGateway")  # if processed
                except PaymentError:
                    pass
                tries += 1
            return (False, "using PremiumPaymentGateway")


    # Functions to just demonstrate the payment gateways
    # raising some Error randomly for now.
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
    methods = ['POST']  # only POST request allowed

    def dispatch_request(self):
        try:
            data = request.get_json()

            # credit card number required
            cardnumber = data.get('CreditCardNumber')
            if not cardnumber:
                return ("Error: No CreditCardNumber field provided. Please specify CreditCardNumber.", status.HTTP_400_BAD_REQUEST)
            # must be valid
            if not card_is_valid(cardnumber):
                return ("Error: CardNumber is invalid. Please provide correct CreditCardNumber.", status.HTTP_400_BAD_REQUEST)
            
            # card holder required
            cardholder =  data.get('CardHolder')
            if not cardholder:
                return ("Error: Card Holder is required.", status.HTTP_400_BAD_REQUEST)

            # expiration required
            exp = data.get('ExpirationDate')
            if not exp:
                return ("Error: Expiration Date is required.", status.HTTP_400_BAD_REQUEST)
            
            # make in datetime format as mm/yy
            try:
                exp_date = datetime.strptime(exp, '%m/%y')
            except ValueError: # invalid format
                return ("Error: Expiration date format is mm/yy", status.HTTP_400_BAD_REQUEST)
            
            # Card is usually vaild through/ until not before.
            # But Acc. do instructions, exp must not be in past. 
            if exp_date < datetime.today():
                return ("Error: Card is expired.", status.HTTP_400_BAD_REQUEST)
        
            scode = data.get('SecurityCode')
            if scode:
                # if not all digits
                if not (scode.isdigit()):
                    return ("Error: invalid Security Code.", status.HTTP_400_BAD_REQUEST)
                # if more or less than 3
                if not (len(scode) == 3):
                    return ("Error: invalid Security Code. Security Code should be 3 digits.", status.HTTP_400_BAD_REQUEST)

            amount = data.get('Amount')  
            # amount required
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

# handle 404
@app.errorhandler(404)
def page_not_found(e):
    return ("<h1>404</h1><p>The resource could not be found.</p>", status.HTTP_404_NOT_FOUND)


# add in base URL
app.add_url_rule('/', view_func=ProcessPayment.as_view('processpayment'))

# launch if run, not when imported. 
if __name__ == "__main__":
    app.run()
