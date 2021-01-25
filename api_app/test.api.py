import unittest
from api import app
import json


class MyTestCase(unittest.TestCase):
    tester = app.test_client()


    def test_CardNumber_required(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CardHolder':"Naazneen" ,
         "ExpirationDate":"03/21", "SecurityCode":"541", "Amount":"120"})
        response = self.tester.post(data=test_data,headers=headers)
        #print("look:", response.data, response.status_code)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,b"Error: No CreditCardNumber field provided. Please specify CreditCardNumber.")
        

    def test_CardNumber_invalid(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398717", 'CardHolder':"Naazneen" ,
         "ExpirationDate":"03/21", "SecurityCode":"541", "Amount":"120"})
        response = self.tester.post(data=test_data,headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,b"Error: CardNumber is invalid. Please provide correct CreditCardNumber.")
        
 
    def test_home_CardHolder_NotGiven(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398716", 
         "ExpirationDate":"03/21", "SecurityCode":"541", "Amount":"120"})
        response = self.tester.post(data=test_data,headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data,b"Error: Card Holder is required.")

    
    def test_home_Expiration_NotGiven(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398716", 'CardHolder':"Naazneen" ,
        "SecurityCode":"541", "Amount":"120"})
        response = self.tester.post(data=test_data,headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: Expiration Date is required.")


    def test_home_Expiration_ImproperFormat(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398716", 'CardHolder':"Naazneen" ,
        "ExpirationDate":"03/2021", "SecurityCode":"541", "Amount":"120"})
        response = self.tester.post(data=test_data,headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: Expiration date format is mm/yy")


    def test_home_Expiration_Expired(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398716", 'CardHolder':"Naazneen" ,
        "ExpirationDate":"12/20", "SecurityCode":"541", "Amount":"120"})
        response = self.tester.post(data=test_data,headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: Card is expired.")
    
    
    def test_home_Amount_Invalid(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398716", 'CardHolder':"Naazneen" ,
        "ExpirationDate":"03/21", "SecurityCode":"541", "Amount":"120D"})
        response = self.tester.post(data=test_data,headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: invalid amount")

   
    def test_home_Amount_Negative(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398716", 'CardHolder':"Naazneen" ,
        "ExpirationDate":"03/21", "SecurityCode":"541", "Amount":"-120"})
        response = self.tester.post(data=test_data,headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: invalid amount(negative)")


    def test_home_Amount_NotGiven(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398716", 'CardHolder':"Naazneen" ,
        "ExpirationDate":"03/21"})
        response = self.tester.post(data=test_data,headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: No Amount field provided. Please specify an Amount.")


    def test_home_SecurityCode_not3digit(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398716", 'CardHolder':"Naazneen" ,
        "ExpirationDate":"03/21", "SecurityCode":"54321", "Amount":"-120"})
        response = self.tester.post(data=test_data,headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: invalid Security Code. Security Code should be 3 digits.")


    def test_home_Security_Invalid(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398716", 'CardHolder':"Naazneen" ,
        "ExpirationDate":"03/21", "SecurityCode":"FD2", "Amount":"-120"})
        response = self.tester.post(data=test_data,headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, b"Error: invalid Security Code.")
        
    
    def test_cheap(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398716", 'CardHolder':"Naazneen" ,
        "ExpirationDate":"03/21", "SecurityCode":"123", "Amount":"18"})
        response = self.tester.post(data=test_data,headers=headers)

        if response.data == b"Payment Failed using CheapPaymentGateway":
            #print("here")
            self.assertEqual(response.status_code, 500)
        elif response.data == b"Payment Processed using CheapPaymentGateway":
            #print("there")
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.data, "Unknown error occured.")
            self.assertEqual(response.status_code, 500)

    
    def test_expensive(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398716", 'CardHolder':"Naazneen" ,
        "ExpirationDate":"03/21", "SecurityCode":"124", "Amount":"58"})
        response = self.tester.post(data=test_data,headers=headers)
        
        if response.data == b"Payment Failed using ExpensivePaymentGateway" or response.data == b"Payment Failed using CheapPaymentGateway":
            # print("here")
            self.assertEqual(response.status_code, 500)
        elif response.data == b"Payment Processed using ExpensivePaymentGateway" or response.data == b"Payment Processed using CheapPaymentGateway":
            # print("there")
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.data, "Unknown error occured.")
            self.assertEqual(response.status_code, 500)

    
    def test_premium(self):
        headers = {'Content-type': 'application/json'}
        test_data = json.dumps({'CreditCardNumber':"49927398716", 'CardHolder':"Naazneen" ,
        "ExpirationDate":"03/21", "SecurityCode":"123", "Amount":"580"})
        response = self.tester.post(data=test_data,headers=headers)
        
        if response.data == b"Payment Failed using PremiumPaymentGateway":
            # print("here")
            self.assertEqual(response.status_code, 500)
        elif response.data == b"Payment Processed using PremiumPaymentGateway":
            # print("there")
            self.assertEqual(response.status_code, 200)
        else:
            self.assertEqual(response.data, "Unknown error occured.")
            self.assertEqual(response.status_code, 500)
    
   
    def test_404(self):
        response = self.tester.get('/paymentdone')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, b"<h1>404</h1><p>The resource could not be found.</p>")


    def test_get(self):
        response = self.tester.get("/")
        self.assertEqual(response.status_code, 405)

    

if __name__ == '__main__':
    unittest.main()
