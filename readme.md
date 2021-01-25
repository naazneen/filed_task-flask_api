# Flask Payment API

## Introduction
This is an api to redirect to the payment gateways based on the payment Amount in request.

## To run the app:

#### Pre-requisite:
To install requirements for this project, go to cmd and run:
```
pip install -r requirements.txt
```


Go to root directory from cmd and type
```
python api.py
```

**POSTMAN** example:

POST : http://127.0.0.1:5000/
Body:
{
    "CreditCardNumber":"49927398716",
    "CardHolder":"Naazneen",
    "ExpirationDate":"12/21",
    "Amount":"501",
    "SecurityCode":"230"
}

Expected Output:
Body:
{Payment Processed using PremiumPaymentGateway}

## To test the app
Go to root directory from cmd and type
```
python test.api.py
```

## Thank you for the test.
