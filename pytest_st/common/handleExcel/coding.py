#encoding:utf-8
import types
from base64 import decode


def to_unicode(data, coding="utf-8"):
    if type(data) == str:
        print(data)
        return data
    elif type(data) == list:
        print(to_unicode(i) for i in data)
        return [to_unicode(i) for i in data]
    elif type(data) == dict:
        return {to_unicode(k): to_unicode(v) for k, v in data.iteritems()}
    else:
        return data
def str_dict_to_unicode(s_data, coding="utf-8"):
    s_data = s_data.strip()
    if s_data.startswith('{') and s_data.endswith('}'):
        s_data = s_data[1:-1]
        print(s_data)
def unicode2str(data, coding="utf-8"):
    if type(data) == str:
        print (data)
        return data
    elif type(data) == list:
        print ([unicode2str(i) for i in data])
        return [unicode2str(i) for i in data]
    elif type(data) == dict:
        print({unicode2str(k): unicode2str(v) for k, v in data.items()})
        return {unicode2str(k): unicode2str(v) for k, v in data.items()}

    else:
        # return str(data)
        return data

if __name__ == "__main__":
     #unicode2str("kkjdkk")
     #unicode2str([1,2,3])
     #unicode2str({"ss":"ss","jk":"oejk"})
     str_dict_to_unicode('{"ss":"ss","jk":"oejk"}')
     to_unicode("kll")


