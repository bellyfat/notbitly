# -*- coding: utf-8 -*-

import psycopg2
import string


def dec_to_base(num):
    alphabet = string.digits + string.ascii_letters + "$-_.+!*'(),"
    base = len(alphabet)

    if base <= 0:
        return 0
    num, rem = divmod(num, base)
    result = alphabet[rem]
    while num:
        num, rem = divmod(num, base)
        result = alphabet[rem] + result
    return result

def to_base10(num):
    alphabet = string.digits + string.ascii_letters + "$-_.+!*'(),"

    return sum(alphabet.find(x)*len(alphabet)**i for i,x in enumerate(num))


print(dec_to_base(17))
print(to_base10('11'))
