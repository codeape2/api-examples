from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


def create_authenticated_http_session(client_id, client_secret):
    oauth2_client = BackendApplicationClient(client_id=client_id)
    session = OAuth2Session(client=oauth2_client)
    session.fetch_token(
        token_url='https://api.sbanken.no/identityserver/connect/token',
        client_id=client_id,
        client_secret=client_secret
    )
    return session


def get_customer_information(http_session, customerid):
    response = http_session.get(
        "https://api.sbanken.no/customers/api/v1/Customers/{}".format(customerid)
    ).json()

    if not response["isError"]:
        return response["item"]
    else:
        raise RuntimeError("{} {}".format(response["errorType"], response["errorMessage"]))


def get_accounts(http_session, customerid):
    response = http_session.get(
        "https://api.sbanken.no/bank/api/v1/Accounts/{}".format(customerid)
    ).json()

    if not response["isError"]:
        return response["items"]
    else:
        raise RuntimeError("{} {}".format(response["errorType"], response["errorMessage"]))


def main():
    import api_settings
    import pprint

    http_session = create_authenticated_http_session(api_settings.CLIENTID, api_settings.SECRET)

    customer_info = get_customer_information(http_session, api_settings.CUSTOMERID)
    pprint.pprint(customer_info)

    accounts = get_accounts(http_session, api_settings.CUSTOMERID)
    pprint.pprint(accounts)


if __name__ == "__main__":
    main()
