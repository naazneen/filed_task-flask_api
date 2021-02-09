import random

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


    # Functions to just demonstrate the payment gateways
    # raising some Error randomly for now.
    def CheapPaymentGateway(self):  # cheap payment gateway
        n = random.randint(1, 30)
        if n == 3 or n == 9 or n == 6:
            raise PaymentError


    def ExpensivePaymentGateway(self):  # expensive payment gateway
        n = random.randint(1, 30)
        if n == 3 or n == 9:
            raise PaymentError


    def PremiumPaymentGateway(self):  # premium payment gateway
        n = random.randint(1, 30)
        if n == 3:
            raise PaymentError


    # select appropriate service, based on amount
    def choose_pay_service(self):
        if self.amt <= 20:  # for amount less than or equal 20
            try:
                self.CheapPaymentGateway()
                return (True, "using CheapPaymentGateway")
            except PaymentError:
                return (False, "using CheapPaymentGateway")

            #return resp, "using CheapPaymentGateway"

        elif 500 >= self.amt >= 21:  # for amount between 21 and 500 (inclusive)
            try:  # try expensive if available
                self.ExpensivePaymentGateway()
                return (True, "using ExpensivePaymentGateway")

            except PaymentError:  # else go for cheap
                try:
                    self.CheapPaymentGateway()
                    return (True, "using CheapPaymentGateway")
                except PaymentError:
                    return (False, "using CheapPaymentGateway")

        elif self.amt > 500:  # for amount more than 500
            tries = 0 # 
            resp = False
            while not resp and tries < 3:  # three tries on premium
                try:
                    self.PremiumPaymentGateway()
                    return (True,"using PremiumPaymentGateway")  # if processed
                except PaymentError:
                    pass
                tries += 1
            return (False, "using PremiumPaymentGateway")


 
