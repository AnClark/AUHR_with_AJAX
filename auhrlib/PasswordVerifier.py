"""
-------------------------------------------------------------
    自编模块
    登录验证系统 之 密码验证
-------------------------------------------------------------

"""

import hashlib


def sha256_verify(pwd_str, digest_in_db):
    pwd_str_enc = hashlib.sha256(pwd_str.encode())
    if pwd_str_enc.digest() == digest_in_db:
        return True
    else:
        return False


def test():
    src = input("Input password without encoding:\n")
    enc = hashlib.sha256(src.encode())

    print("Your encrypted password data is:\n %s" % enc.digest())

    print("\n")
    print("Verify your encryption:")
    print(sha256_verify(src, enc.digest()))

if __name__ == "__main__":
    test()