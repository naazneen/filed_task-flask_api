from flask import request
import flask
from flask.views import View
from flask_api import status
from utils import card_is_valid  # to validate card.
from utils import process 
from datetime import datetime
import random


app = flask.Flask(__name__)
app.config["DEBUG"] = True


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

            # process class from utils.
            pay_Class = process(cardnumber,cardholder,amount,exp, scode)  # initialize
            result = pay_Class.choose_pay_service()  # make payment
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
