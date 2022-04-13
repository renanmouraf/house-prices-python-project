
def check_string_empty_or_none(input_string: str):
    return (input_string is not None) and (input_string)

def sanitize_string(input_string: str):
    return input_string.strip()