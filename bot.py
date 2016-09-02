import xml.etree.ElementTree as ET
import urllib2
import sys
from HTMLParser import HTMLParser

reload(sys)  
sys.setdefaultencoding('utf-8')

var = raw_input("Please enter language codes (en es pt): ")
parser = HTMLParser()
languages = var.split() 
agent = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
xmlFile = ET.parse('strings/strings.xml').getroot()
root = ET.Element("resources")
def indent(elem, level=0):
  i = "\n" + level*"    "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "    "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def translate(translate_string, to_langage="auto"):
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, "en", translate_string.replace(" ", "+"))
    request = urllib2.Request(link, headers=agent)
    page = urllib2.urlopen(request).read()
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    # print "%s || %s" % (translate_string, parser.unescape(result).encode('utf-8'))
    return parser.unescape(result).encode('utf-8')

for code in languages:
    print "\n"
    print "Translating to %s" % code
    for strings in xmlFile.findall("string"):
        ET.SubElement(root, "string", name=strings.get('name')).text = translate(strings.text, code)
        indent(root)
    tree = ET.ElementTree(root)
    tree.write("strings/%s.xml" % code, xml_declaration=True, encoding='utf-8', method="xml")
    print "Translated strings to %s in %s.xml" % (code, code)