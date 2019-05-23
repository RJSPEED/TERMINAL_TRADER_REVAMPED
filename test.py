"""
import hashlib

SALT = "this is anything"

def hash_password(password):
    hasher = hashlib.sha512()
    #hasher.update(password.encode()) + SALT.encode()
    hasher.update(password.encode())
    return hasher.hexdigest()

if __name__=="__main__":
    print(hash_password('passw0rd'))
"""

url_str = ("http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol" + "xxx")
print(url_str)