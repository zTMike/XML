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
tree = ET.parse("Documentos/fv08909165750152500772933.xml")
root = tree.getroot()


facturaid_elem=root.find("cbc:ParentDocumentID", ATTACHED_NS)
facturaid = facturaid_elem.text if facturaid_elem is not None else "No encontrado"
print("Factura ID:", facturaid)

direccion_elem = root.find(".//cac:ReceiverParty/cac:PartyTaxScheme/cac:RegistrationAddress/cac:AddressLine/cbc:Line", ATTACHED_NS)
direccion_emisor = direccion_elem.text if direccion_elem is not None else "No encontrado"
print("Dirección del emisor:", direccion_emisor)

fecha_elem=root.find(".//cac:ParentDocumentLineReference/cac:DocumentReference/cac:ResultOfVerification/cbc:ValidationTime", ATTACHED_NS)
fechadevalidacion = fecha_elem.text if fecha_elem is not None else "No encontrado"
print("Fecha de validación:", fechadevalidacion)

desc_elem=root.find(".//cac:Attachment/cac:ExternalReference/cbc:Description", ATTACHED_NS)
descripcion_datos = desc_elem.text if desc_elem is not None else ""


Info=ET.fromstring(descripcion_datos.strip())
producto_nombre=Info.find(".//cac:InvoiceLine[1]/cac:Item/cbc:Description", INVOICE_NS).text
print("Nombre del producto:", producto_nombre)


productos={}
i=0
while True:
    elemento=Info.find(f".//cac:InvoiceLine[{i+1}]/cac:Item/cbc:Description", INVOICE_NS)
    if elemento is None:
        break

    # Función auxiliar para extraer texto o atributo de forma segura
    def get_text(path):
        elem = Info.find(path, INVOICE_NS)
        return elem.text if elem is not None else None
    
    def get_attr(path, attr):
        elem = Info.find(path, INVOICE_NS)
        return elem.get(attr) if elem is not None else None
    
    base = f".//cac:InvoiceLine[{i+1}]"
    
    productos[f"producto_{i+1}"] = {
        # DATOS GENERALES
        "NumeroLinea": get_text(f"{base}/cbc:ID"),
        "Descripcion": get_text(f"{base}/cac:Item/cbc:Description"),
        "Cantidad": get_text(f"{base}/cbc:InvoicedQuantity"),
        "Unidad": get_attr(f"{base}/cbc:InvoicedQuantity", "unitCode"),
        "TotalLinea (cant*precio)": get_text(f"{base}/cbc:LineExtensionAmount"),
        "Gratis": get_text(f"{base}/cbc:FreeOfChargeIndicator"),
        
        # IDENTIFICACION PRODUCTO
        "CodigoInterno": get_text(f"{base}/cac:Item/cac:SellersItemIdentification/cbc:ID"),
        "CodigoBarras": get_text(f"{base}/cac:Item/cac:StandardItemIdentification/cbc:ID"),
        
        # PRECIOS
        "Precio Base": get_text(f"{base}/cac:Price/cbc:PriceAmount"),
        "CantidadBasePrecio": get_text(f"{base}/cac:Price/cbc:BaseQuantity"),
        
        # IMPUESTOS
        
            "IVA_Valor": get_text(f"{base}/cac:TaxTotal/cbc:TaxAmount"),
            "IVA_Porcentaje": get_text(f"{base}/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cbc:Percent"),
            "IVA_Base": get_text(f"{base}/cac:TaxTotal/cac:TaxSubtotal/cbc:TaxableAmount"),
            "IVA_Tipo": get_text(f"{base}/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cac:TaxScheme/cbc:Name"),
            "IVA_Codigo": get_text(f"{base}/cac:TaxTotal/cac:TaxSubtotal/cac:TaxCategory/cac:TaxScheme/cbc:ID"),
        
        # DESCUENTOS / CARGOS
        "Descuento_Indicador": get_text(f"{base}/cac:AllowanceCharge/cbc:ChargeIndicator"),
        "Descuento_Motivo": get_text(f"{base}/cac:AllowanceCharge/cbc:AllowanceChargeReason"),
        "Descuento_Codigo": get_text(f"{base}/cac:AllowanceCharge/cbc:AllowanceChargeReasonCode"),
        "Descuento_Porcentaje": get_text(f"{base}/cac:AllowanceCharge/cbc:MultiplierFactorNumeric"),
        "Descuento_Valor": get_text(f"{base}/cac:AllowanceCharge/cbc:Amount"),
        "Descuento_Base": get_text(f"{base}/cac:AllowanceCharge/cbc:BaseAmount"),
        
        # OTROS
        "Moneda_Total": get_attr(f"{base}/cbc:LineExtensionAmount", "currencyID"),
        "Moneda_Precio": get_attr(f"{base}/cac:Price/cbc:PriceAmount", "currencyID"),
        "Moneda_IVA": get_attr(f"{base}/cac:TaxTotal/cbc:TaxAmount", "currencyID"),
    }
    i+=1

print("Lista Productos:")
for clave, producto in productos.items():
    print(f"\n{clave}:")
    for campo, valor in producto.items():
        print(f"  {campo}: {valor}")






    


  