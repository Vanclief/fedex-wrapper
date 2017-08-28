import os
import zeep
from datetime import datetime


def ship(
    production,
    key,
    password,
    account_number,
    meter_number,
    shipper_address,
    shipper_contact,
    recipient_address,
    recipient_contact,
    length,
    width,
    height,
    weight,
    customer_reference_value='',
    order_reference_value=''
):
    """ Creates a new shipment with fedex, with the provided data.

    """
    base_dir = os.path.dirname(os.path.abspath(__file__)) + '/wsdl'
    if production:
        base_dir = base_dir + '/production'
    wsdl = base_dir + '/ShipService_v19.wsdl'
    client = zeep.Client(wsdl=wsdl)
    factory = client.type_factory('ns0')

    parent_credential = factory.WebAuthenticationCredential(Key=key, Password=password)
    user_credential = factory.WebAuthenticationCredential(Key=key, Password=password)

    web_auth_detail = factory.WebAuthenticationDetail(ParentCredential=parent_credential,
                                                      UserCredential=user_credential)

    client_detail = factory.ClientDetail(AccountNumber=account_number, MeterNumber=meter_number)

    version = factory.VersionId(ServiceId='ship', Major='19', Intermediate='0', Minor='0')

    ship_timestamp = datetime.utcnow()
    dropoff_type = factory.DropoffType('REQUEST_COURIER')
    service_type = factory.ServiceType('FEDEX_EXPRESS_SAVER')
    packaging_type = factory.PackagingType('YOUR_PACKAGING')

    s_address = factory.Address(**shipper_address)
    s_contact = factory.Contact(**shipper_contact)
    r_address = factory.Address(**recipient_address)
    r_contact = factory.Contact(**recipient_contact)

    contact = factory.Contact(PersonName='Enrique Nogales Piñas',
                              Title='CEO',
                              CompanyName='iupick',
                              PhoneNumber='5523832042',
                              PhoneExtension='',
                              EMailAddress='nogalpi@gmail.com')

    address = factory.Address(StreetLines=['Nogal 333', 'Colonia Arboledas'],
                              City='Querétaro',
                              StateOrProvinceCode='QT',
                              PostalCode='76140',
                              CountryCode='MX',
                              CountryName='Mexico',
                              Residential=True)

    shipper = factory.Party(Contact=s_contact,
                            Address=s_address)

    recipient = factory.Party(Contact=r_contact,
                              Address=r_address)

    payment_type = factory.PaymentType('THIRD_PARTY')
    payor_party = factory.Party(AccountNumber=account_number,
                                Contact=contact,
                                Address=address)

    payor = factory.Payor(ResponsibleParty=payor_party)

    shipping_charges_payment = factory.Payment(PaymentType=payment_type,
                                               Payor=payor)

    label_format_type = factory.LabelFormatType('COMMON2D')
    label_specification = factory.LabelSpecification(LabelFormatType=label_format_type,
                                                     ImageType='PDF')

    package_count = '1'

    weight_units = factory.WeightUnits('KG')
    weight = factory.Weight(Units=weight_units,
                            Value=weight)

    dimensions = factory.Dimensions(Length=length,
                                    Width=width,
                                    Height=height,
                                    Units='CM')

    customer_reference_type = factory.CustomerReferenceType('CUSTOMER_REFERENCE')
    customer_reference = factory.CustomerReference(CustomerReferenceType=customer_reference_type,
                                                   Value=customer_reference_value)

    order_reference_type = factory.CustomerReferenceType('P_O_NUMBER')
    order_reference = factory.CustomerReference(CustomerReferenceType=order_reference_type,
                                                Value=order_reference_value)
    
    customer_references = [customer_reference, order_reference]
    requested_package_line_item = factory.RequestedPackageLineItem(SequenceNumber='1',
                                                                   Weight=weight,
                                                                   Dimensions=dimensions,
                                                                   CustomerReferences=customer_references)

    requested_package_line_items = [requested_package_line_item]

    requested_shipment = factory.RequestedShipment(
       ShipTimestamp=ship_timestamp,
       DropoffType=dropoff_type,
       ServiceType=service_type,
       PackagingType=packaging_type,
       Shipper=shipper,
       Recipient=recipient,
       ShippingChargesPayment=shipping_charges_payment,
       LabelSpecification=label_specification,
       RequestedPackageLineItems=requested_package_line_items,
       PackageCount=package_count
    )

    return client.service.processShipment(WebAuthenticationDetail=web_auth_detail,
                                          ClientDetail=client_detail,
                                          Version=version,
                                          RequestedShipment=requested_shipment)
