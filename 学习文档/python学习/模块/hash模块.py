import hashlib
import os
import time


'''
    hashlib 是python 中常见的摘要算法，支持算法如下:
        1. md5()
        2. sha1()
        3. sha224()
        4. sha256()
        5. sha384()
        6. sha512()
        7. blake2b()
        8. blake2s(),
        9. sha3_224, sha3_256, sha3_384, sha3_512, shake_128, and shake_256.
    
    摘要算法:   计算文件或数据的统一身份、校验是否被篡改，密文方式展示，不可解密，且同一数据摘要算法结果一定一致。
'''

Str = "abcd112"
def test_md5(s):

    size = 0
    md5_str = ""
    sale = 'abc'
    with open(file=s,mode='rb') as r:
        hash_obj = hashlib.md5()
        file_size = os.path.getsize('config.ini')
        while  size <= file_size:
            res = r.read(10)
            # 加盐
            hash_obj.update(res + sale.encode('utf-8'))
            size += 10
    return  hash_obj.hexdigest()


