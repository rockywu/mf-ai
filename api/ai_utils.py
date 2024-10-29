import xml.etree.ElementTree as ET
import configparser
config = configparser.ConfigParser()
#该配置请在docker/api.ini中修改
config.read("config.ini")
def getConfig(key_path):
    section, key = key_path.split(".")
    return config.get(section, key)

def xml_to_json(xml_str):
    # 解析 XML 字符串
    root = ET.fromstring(xml_str)
    
    # 定义一个递归函数，将 XML 转换为字典
    def parse_element(element):
        # 将元素及其子元素转换为字典
        parsed_data = {}
        for child in element:
            parsed_data[child.tag] = child.text
        return parsed_data

    # 调用解析函数
    json_data = parse_element(root)
    
    # 转换为 JSON 对象
    return json_data

