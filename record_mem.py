# ------------------------------------------------serial file------------------------------------------
# author by hailong.wang
# date at 2022.3.20
# -----------------------------------------------------------------------------------------------------

from xml.dom.minidom import parse
from xml.dom.minidom import Document

COMM_BOX_XML_FILE = 'commbox.xml'
COMM_BOX_XML_PATH = './commbox.xml'


class RecordMemory:
    @staticmethod
    def create_xml():
        doc = Document()
        # root content
        commbox = doc.createElement('CommBox\n')
        commbox.setAttribute('xmlns:i', 'http://www.w3.org/2001/XMLSchema-instance')
        commbox.setAttribute('xmlns', 'http://schemas.citytouch.com/FactoryLink/v1.0')
        doc.appendChild(commbox)
        # unique ID
        uniqueid = doc.createElement('UniqueId')
        commbox.appendChild(uniqueid)
        uniqueid_value = doc.createTextNode('null')
        uniqueid.appendChild(uniqueid_value)
        # ten NC
        ten_nc = doc.createElement('CommercialDesignation')
        commbox.appendChild(ten_nc)
        ten_nc_value = doc.createTextNode('null')
        ten_nc.appendChild(ten_nc_value)
        # brand name
        brand_name = doc.createElement('BrandName')
        commbox.appendChild(brand_name)
        brand_name_value = doc.createTextNode('null')
        brand_name.appendChild(brand_name_value)
        # product name
        product_name = doc.createElement('ProductName')
        commbox.appendChild(product_name)
        product_name_value = doc.createTextNode('null')
        product_name.appendChild(product_name_value)
        # product date
        product_date = doc.createElement('ProductionDate')
        commbox.appendChild(product_date)
        product_date_value = doc.createTextNode('null')
        product_date.appendChild(product_date_value)
        # product week
        product_week = doc.createElement('ProductionWeek')
        commbox.appendChild(product_week)
        product_week_value = doc.createTextNode('null')
        product_week.appendChild(product_week_value)
        # product location
        product_location = doc.createElement('ProductionLocation')
        commbox.appendChild(product_location)
        product_location_value = doc.createTextNode('null')
        product_location.appendChild(product_location_value)
        # firmware version
        fw_ver = doc.createElement('FactoryFirmwareVersion')
        commbox.appendChild(fw_ver)
        fw_ver_value = doc.createTextNode('null')
        fw_ver.appendChild(fw_ver_value)
        # IOT modem information
        modem = doc.createElement('Modem')
        commbox.appendChild(modem)
        m_version = doc.createElement('Version')
        modem.appendChild(m_version)
        m_version_value = doc.createTextNode('null')
        m_version.appendChild(m_version_value)
        m_imei = doc.createElement('IMEI')
        modem.appendChild(m_imei)
        m_imei_value = doc.createTextNode('null')
        m_imei.appendChild(m_imei_value)
        m_serial = doc.createElement('Serial')
        modem.appendChild(m_serial)
        m_serial_value = doc.createTextNode('null')
        m_serial.appendChild(m_serial_value)
        # calibration
        calibration = doc.createElement('Calibration')
        commbox.appendChild(calibration)
        light_gain = doc.createElement('Lgain')
        calibration.appendChild(light_gain)
        light_gain_value = doc.createTextNode('null')
        light_gain.appendChild(light_gain_value)
        light_offset = doc.createElement('Loffset')
        calibration.appendChild(light_offset)
        light_offset_value = doc.createTextNode('null')
        light_offset.appendChild(light_offset_value)
        temperature_offset = doc.createElement('Toffset')
        calibration.appendChild(temperature_offset)
        temperature_offset_value = doc.createTextNode('null')
        temperature_offset.appendChild(temperature_offset_value)
        # hardware version
        hw_ver = doc.createElement('HardwareRevision')
        commbox.appendChild(hw_ver)
        hw_ver_value = doc.createTextNode('null')
        hw_ver.appendChild(hw_ver_value)
        # switch regime
        sw_regime = doc.createElement('SwitchRegime')
        commbox.appendChild(sw_regime)
        sw_regime_value = doc.createTextNode('null')
        sw_regime.appendChild(sw_regime_value)

        filename = 'commbox.xml'
        f = open(filename, 'w')

        f.write(doc.toprettyxml(indent="  "))
        f.close()

    @staticmethod
    def update_item_xml(name, value):
        domTree = parse(COMM_BOX_XML_PATH)
        rootNode = domTree.documentElement

        element = rootNode.getElementsByTagName(name)
        # print(element[0].firstChild.data)
        element[0].firstChild.data = value
        # print(element[0].firstChild.data)

        with open(COMM_BOX_XML_FILE, 'w') as f:
            domTree.writexml(f, indent='', addindent='', encoding='utf-8')

