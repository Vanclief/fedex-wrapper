import os
import zeep


def track():
    """ Returns a waybill

    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    wsdl = BASE_DIR + '/TrackService_v12.wsdl'
    client = zeep.Client(wsdl=wsdl)
    factory = client.type_factory('ns0')


    parent_credential = factory.WebAuthenticationCredential(Key='6YeOgDMb3Gmus3kW', Password='DQst0qQlQRGAMvEtealFm5pRH')
    user_credential = factory.WebAuthenticationCredential(Key='6YeOgDMb3Gmus3kW', Password='DQst0qQlQRGAMvEtealFm5pRH')



    web_auth_detail = factory.WebAuthenticationDetail(ParentCredential=parent_credential, UserCredential=user_credential)

    client_detail = factory.ClientDetail(AccountNumber='510087500', MeterNumber='118786341')

    version = factory.VersionId(ServiceId='trck', Major='12', Intermediate='0', Minor='0')

    identifier_type = factory.TrackIdentifierType('TRACKING_NUMBER_OR_DOORTAG')
    package_identifier = factory.TrackPackageIdentifier(Type=identifier_type, Value='122816215025810')

    selection_detail = factory.TrackSelectionDetail(PackageIdentifier=package_identifier)
    return(client.service.track(WebAuthenticationDetail=web_auth_detail,
                                ClientDetail=client_detail,
                                Version=version,
                                SelectionDetails=selection_detail))
