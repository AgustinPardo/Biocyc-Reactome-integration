
import requests
import xml.etree.ElementTree as ET   


url=''
mm = requests.get(url)
ee = mm.text
root = ET.fromstring(ee)


xpath cover page
