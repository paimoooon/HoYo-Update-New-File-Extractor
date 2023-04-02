import xml.sax

# CONSTANTS

OLD_XML = "./input/old_assetmap.xml"
NEW_XML = "./input/new_assetmap.xml"
OUTPUT_XML = "./output/added_assets.xml"

# CLASSES

class OldHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.names = []
        self.buffer = None

    def startElement(self, name, attrs):
        if name == "Name":
            self.buffer = ""

    def endElement(self, name):
        if name == "Name":
            self.names.append(self.buffer)
            self.buffer = None

    def characters(self, content):
        if self.buffer is not None:
            self.buffer += content

class NewHandler(xml.sax.ContentHandler):
    def __init__(self, names, output_file):
        self.names = names
        self.output_file = output_file
        self.buffer = None
        self.asset_buffer = []
        self.in_asset = False
        self.write_flag = False

    def startElement(self, name, attrs):
        if name == "Asset":
            self.write_flag = False
            self.in_asset = True
            self.asset_buffer.append("  <Asset>\n")
        elif self.in_asset:
            self.buffer = ""
            self.asset_buffer.append(f"    <{name}>")

    def endElement(self, name):
        if name == "Asset":
            self.in_asset = False
            self.asset_buffer.append("  </Asset>\n")
            asset_str = "".join(self.asset_buffer)
            if self.write_flag:
                with open(self.output_file, "a", encoding="utf-8") as f:
                    f.write(asset_str)
            self.asset_buffer = []
        elif name == "Name":
            self.asset_buffer.append(f"{self.buffer}</{name}>\n")
            if self.buffer not in self.names:
                self.write_flag = True
            else:
                self.write_flag = False
            self.buffer = None
        elif self.in_asset:
            self.asset_buffer.append(f"{self.buffer}</{name}>\n")
            self.buffer = None

    def characters(self, content):
        if self.buffer is not None:
            self.buffer += content

# FUNCTIONS

def compare_xml_files(file1, file2, output_file):

    print("Parsing the old AssetMap file...")
    parser_old = xml.sax.make_parser()
    handler_old = OldHandler()
    parser_old.setContentHandler(handler_old)
    parser_old.parse(file1)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("<Assets>\n")

    print("Parsing and filtering the new AssetMap file...")
    parser_new = xml.sax.make_parser()
    handler_new = NewHandler(set(handler_old.names), output_file)
    parser_new.setContentHandler(handler_new)
    parser_new.parse(file2)

    with open(output_file, "a", encoding="utf-8") as f:
        f.write("</Assets>\n")

    print(f"New AssetMap for added assets is written to {output_file}")

if __name__ == "__main__":

    compare_xml_files(OLD_XML, NEW_XML, OUTPUT_XML)