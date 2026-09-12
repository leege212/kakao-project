from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256


def generate_hospital_keys():
    # RSA 키 생성
    key = RSA.generate(3072)

    # 병원 개인키
    with open("hospital_private.pem", "wb") as f:
        f.write(
            key.export_key(
                format="PEM",
                pkcs=8
            )
        )

    # 병원 공개키
    with open("hospital_public.pem", "wb") as f:
        f.write(
            key.publickey().export_key()
        )


def encrypt_aes_key(aes_key):
    # 병원 공개키 불러오기
    with open("hospital_public.pem", "rb") as f:
        public_key = RSA.import_key(f.read())

    # RSA-OAEP + SHA-256
    cipher = PKCS1_OAEP.new(
        public_key,
        hashAlgo=SHA256
    )

    # AES Key 암호화
    encrypted_key = cipher.encrypt(aes_key)

    # 암호화된 AES Key 저장
    with open("encrypted_key.bin", "wb") as f:
        f.write(encrypted_key)

    return encrypted_key