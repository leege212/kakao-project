import requests
import os

def upload_file_to_pinata(file_path):
    PINATA_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiIwNDVmYmJiZi1lMGUyLTQ2YTQtODJlYy1lYzlmODBjNTFhMzIiLCJlbWFpbCI6InNzeXlraW0wM0BuYXZlci5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJGUkExIn0seyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJOWUMxIn1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiMjNiNmJmZWY2ZjhmNzE4MzNmZWMiLCJzY29wZWRLZXlTZWNyZXQiOiJlNDEyZDQ0NTYwMmFjMTExZjVkNDM5ZDYwMzJhMWFmZjkxNDBmNmJhNDcyNTZmZDY2ZTY1YjdlYmE5NmE5MTI2IiwiZXhwIjoxODEwMzU0MjAxfQ.ei1uAU6IlZpjuTavmZSYpG7WqzUK9pbbmVjCGddU3o0"
    
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    
    headers = {
        "Authorization": f"Bearer {PINATA_JWT}"
    }

    if not os.path.exists(file_path):
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        return None

    print(f"🚀 Pinata(IPFS)에 '{file_path}' 업로드 중...")

    try:
        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file)}
            response = requests.post(url, headers=headers, files=files)

            if response.status_code == 200:
                cid = response.json().get('IpfsHash')
                print(f"✅ 업로드 성공!")
                print(f"🎉 반환된 CID: {cid}")
                return cid
            else:
                print(f"❌ 업로드 실패. 상태 코드: {response.status_code}")
                print(response.text)
                return None

    except Exception as e:
        print(f"업로드 중 오류 발생: {e}")
        return None

# --- 테스트 실행 부분 ---
if __name__ == "__main__":
    # 테스트용 더미 파일 만들기
    test_file_name = "test_data.txt"
    with open(test_file_name, "w", encoding="utf-8") as f:
        f.write("이 데이터가 IPFS에 무사히 올라간다면 성공입니다!")

    # 함수 실행
    returned_cid = upload_file_to_pinata(test_file_name)