import requests
from django.utils.crypto import get_random_string
from python_daraja import payment
import datetime
from django.http import JsonResponse


def trigger_stk_push(phone_number: int, amount: int, callback_url: str, account_ref: str, description: str) -> dict:
    """

    :param phone_number: Customer Phone Number
    :param amount: Amount to be paid
    :param callback_url: Your callback URL configured in the dashboard
    :param account_ref: Account Reference (e.g. Company Name/Business Name)
    :param description: Transaction Description
    :return: Python Dictionary with transaction info
    """

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {payment._get_access_token()}'
    }
    # print(payment.SHORT_CODE)
    # payment.SHORT_CODE = '174379'
    # print(payment.SHORT_CODE)
    payload = {
        "BusinessShortCode": payment.SHORT_CODE,
        "Password": payment._get_password(),
        "Timestamp": datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        "TransactionType": 'CustomerPayBillOnline',
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": payment.SHORT_CODE,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_ref,
        "TransactionDesc": description
    }

    print(payload)

    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
                                headers=headers, json=payload)


    print(response.json())
    return dict(response.json())






def build_payment_request():
    details = trigger_stk_push(
        phone_number="254790841979",
        amount=1,
        callback_url='https://thinkopal.com',
        description='Payment',
        account_ref=get_random_string(10)
    )
    
   
    return