import re
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def remove_extra_spaces(text: str):
    text_content = re.sub(r'\s{2,}', ' ', text)
    return convert_to_oneline(text_content)

def convert_to_oneline(multiline_string: str):
    one_line_string = ''.join(line.strip() for line in multiline_string.splitlines())
    
    one_line_string = multiline_string.replace('\n', '')
    
    return one_line_string
    