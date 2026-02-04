from __future__ import annotations

from typing import Optional
from xml.etree import ElementTree as ET


# Namespaces del XML externo (AttachedDocument).
# Se usan como prefijos en los XPath para resolver los espacios de nombres del UBL.
ATTACHED_NS = {
    "a": "urn:oasis:names:specification:ubl:schema:xsd:AttachedDocument-2",
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
}

# Namespaces del XML interno (Invoice embebido en CDATA).
# El XML interno tiene un namespace distinto al del AttachedDocument.
INVOICE_NS = {
    "i": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
}
tree = ET.parse("Documentos/ad08110370750002502561912.xml")
root = tree.getroot()


facturaid=root.find("cbc:ParentDocumentID", ATTACHED_NS).text
print("Factura ID:", facturaid)

direccion_emisor = root.find(".//cac:ReceiverParty/cac:PartyTaxScheme/cac:RegistrationAddress/cac:AddressLine/cbc:Line", ATTACHED_NS).text
print("Dirección del emisor:", direccion_emisor)

fechadevalidacion=root.find(".//cac:ParentDocumentLineReference/cac:DocumentReference/cac:ResultOfVerification/cbc:ValidationTime", ATTACHED_NS).text
print("Fecha de validación:", fechadevalidacion)

descripcion_datos=root.find(".//cac:Attachment/cac:ExternalReference/cbc:Description", ATTACHED_NS).text


Info=ET.fromstring(descripcion_datos.strip())
producto_nombre=Info.find(".//cac:InvoiceLine[2]/cac:Item/cbc:Description", INVOICE_NS).text
print("Nombre del producto:", producto_nombre)


















