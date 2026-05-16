from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

# =========================
# 1. AES 비밀키 읽기
# =========================

with open("key.bin", "rb") as f:
    key = f.read()

# =========================
# 2. 암호화 파일 읽기
# =========================

with open("encrypted.bin", "rb") as f:
    iv = f.read(16)          # IV 읽기
    ciphertext = f.read()   # 암호문 읽기

# =========================
# 3. AES 복호화
# =========================

cipher = AES.new(key, AES.MODE_CBC, iv)

try:
    plaintext = unpad(
        cipher.decrypt(ciphertext),
        AES.block_size
    )

except ValueError:
    print("복호화 실패")
    print("암호화 데이터가 변조되었을 가능성이 있습니다.")
    exit()

# =========================
# 4. 복호화 결과 저장
# =========================

with open("decrypted.txt", "wb") as f:
    f.write(plaintext)

print("복호화 완료")
print("decrypted.txt 생성 완료")

# =========================
# 5. 기존 HASH 읽기
# =========================

with open("hash.txt", "r") as f:
    original_hash = f.read()

# =========================
# 6. 복호화 데이터 HASH 생성
# =========================

new_hash = hashlib.sha256(plaintext).hexdigest()

# =========================
# 7. HASH 비교 검증
# =========================

print("\n원본 HASH:")
print(original_hash)

print("\n복호화 데이터 HASH:")
print(new_hash)

if original_hash == new_hash:
    print("\n무결성 검증 성공")
    print("데이터가 변조되지 않았습니다.")

else:
    print("\n무결성 검증 실패")
    print("데이터 변조 가능성이 있습니다.")