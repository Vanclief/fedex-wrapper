import os
import zeep


def track(production,
          key,
          password,
          account_number,
          meter_number,
          tracking_number):
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

    version = factory.VersionId(ServiceId='trck', Major='12', Intermediate='0', Minor='0')

    identifier_type = factory.TrackIdentifierType('TRACKING_NUMBER_OR_DOORTAG')
    package_identifier = factory.TrackPackageIdentifier(Type=identifier_type,
                                                        Value=tracking_number)

    selection_detail = factory.TrackSelectionDetail(PackageIdentifier=package_identifier)

    print(production)
    print(key)
    print(password)
    print(account_number)
    print(meter_number)
    print(tracking_number)

    return(client.service.track(WebAuthenticationDetail=web_auth_detail,
                                ClientDetail=client_detail,
                                Version=version,
                                SelectionDetails=selection_detail))
