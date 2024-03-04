def is_gbk_encodable(input_string):
    try:
        input_string.encode('gbk')
        return True
    except UnicodeEncodeError:
        return False