import os
import zeep
from datetime import date
from datetime import timedelta


def service_availability(production,
                         key,
                         password,
                         account_number,
                         meter_number,
                         tracking_number,
                         origin_postal_code,
                         origin_country_code,
                         destination_postal_code,
                         destination_country_code):
    """ Returns the status of a package as a dictionary

    """
    base_dir = os.path.dirname(os.path.abspath(__file__)) + '/wsdl'
    if production:
        base_dir = base_dir + '/production'
    wsdl = base_dir + '/TrackService_v12.wsdl'
    client = zeep.Client(wsdl=wsdl)
    factory = client.type_factory('ns0')

    parent_credential = factory.WebAuthenticationCredential(Key=key, Password=password)
    user_credential = factory.WebAuthenticationCredential(Key=key, Password=password)

    web_auth_detail = factory.WebAuthenticationDetail(ParentCredential=parent_credential,
                                                      UserCredential=user_credential)

    client_detail = factory.ClientDetail(AccountNumber=account_number, MeterNumber=meter_number)

    version = factory.VersionId(ServiceId='vacs', Major='6', Intermediate='0', Minor='0')

    origin = factory.Address(PostalCode=origin_postal_code,
                             CountryCode=origin_country_code)

    destination = factory.Address(PostalCode=destination_postal_code,
                                  CountryCode=destination_country_code)

    delta = timedelta(days=2)
    shipdate = date.today() + delta
    carrier_code = factory.CarrierCodeType('FDXG')

    return client.service.serviceAvailability(WebAuthenticationDetail=web_auth_detail,
                                              ClientDetail=client_detail,
                                              Version=version,
                                              Origin=origin,
                                              Destination=destination,
                                              ShipDate=shipdate,
                                              CarrierCode=carrier_code)
