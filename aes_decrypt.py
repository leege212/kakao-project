from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# 키 읽기
with open("key.bin", "rb") as f:
    key = f.read()

# 암호문 읽기
with open("encrypted.bin", "rb") as f:
    iv = f.read(16)
    ciphertext = f.read()

# AES 객체 생성
cipher = AES.new(key, AES.MODE_CBC, iv)

# 복호화
plaintext = unpad(
    cipher.decrypt(ciphertext),
    AES.block_size
)

# 저장
with open("decrypted.txt", "wb") as f:
    f.write(plaintext)

print("복호화 완료")