# vFunctions SDK

This package offers tools to develop vFunctions inside a secure enclave.

For an use case example visit the [Verifiably documentation](https://developer.verifiably.com/examples/) page.

## Installation
To install this library run:
```
pip install vfunctions_sdk
```

## Mercury Bank example

``` python
import json
import requests

from vfunctions_sdk import vFunction
from vfunctions_sdk import connection

def mercury_balance_check(account_id, mercury_token, params):

    # Set the url for the mercury API to get the account information
    # Use the account id
    mercury_bank_url = "https://api.mercury.com/api/v1/account/{}".format(account_id)

    # Use the mercury token for the API
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(mercury_token)
    }

    response = requests.request("GET", mercury_bank_url, headers=headers)
    mercury_data = json.loads(response.text)

    if "errors" in mercury_data:
        return False

    if mercury_data["currentBalance"] > params["balance_threshold"]:
        return True

    return False


def main():

    function_params = vFunction.FunctionParams()

    # Get the secrets from the provider
    secrets_bundle = connection.WsockSecretsProvider(function_params).get_secrets()

    # Get the necessary secrets
    account_id = secrets_bundle["mercuryBank"]["accountId"]
    mercury_token = secrets_bundle["mercuryBank"]["mercuryToken"]

    # Get the information from the mercury account
    result_value = mercury_balance_check(account_id, mercury_token, function_params.params)

    result_dict = {
            "result": result_value,
            "balance": function_params.params["balance_threshold"]
    }
    
    # Send the email with the results
    function_params.email_results(function_params.params['email'], result_dict)

if __name__ == '__main__':
    main()
```

