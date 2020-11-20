import xml.etree.ElementTree as ET

#Funcion para parseo del tag metaData 
def retrv_xml_meta(stringed_xml):
    tree = ET.fromstring(stringed_xml)
    meta_data = {}
    for meta in tree.find("./metaData"):
        meta_data[meta.tag] = meta.text

    return meta_data

#Funcion para parsear comunicacion XMLRPC
def parse_from_xml(stringed_xml):

    tree = ET.fromstring(stringed_xml)
    method_name = tree.find("./methodName").text
    name_param = tree.find("./params/param[@name='nombre']/value/string").text
    val_param = tree.find("./params/param[@name='valor']/value/string").text

    if tree.find(".//param[@name='valor']/value").tag == "int":
        value_param = int(value_param)

    return (method_name, name_param, val_param)

#Funcion para strings de tipo XMLRPC
def parse_to_xml(params, upd_call, history):

    tree = ET.parse("methodCall.xml")
    if upd_call == "UPDATED" or upd_call == "CREATED":
        tree.find("methodName").text = "Set"
    elif upd_call == "INCREMENTED":
        tree.find("methodName").text = "Inc"
    elif upd_call == "EXPIRING":
        tree.find("methodName").text = "Exp"
    elif upd_call == "EXPIRED":
        tree.find("methodName").text = "Del"

    tree.find("./params/param[@name='nombre']/value/string").text = params[0]
    tree.find("./params/param[@name='valor']/value/string").text = params[1]

    tree.find("./metaData/id").text = params[2]
    tree.find("./metaData/timestamp").text = str(history["timestamp"])
    tree.find("./metaData/origin").text = history["origin"]

    tree = tree.getroot()

    return ET.tostring(tree)
