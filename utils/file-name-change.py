import os

# 'dog_images' 폴더 경로를 지정합니다.
folder_path = 'dog_images'

# 폴더 내 모든 파일을 가져옵니다.
for filename in os.listdir(folder_path):
    # 파일이름에 '제주-제주'가 포함된 경우
    if '제주-제주' in filename:
        # 새 파일 이름을 생성합니다.
        new_filename = filename.replace('제주-제주', 'Jeju-Jeju')
        
        # 파일의 전체 경로를 생성합니다.
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, new_filename)
        
        # 파일 이름을 변경합니다.
        os.rename(old_file, new_file)

print("파일 이름 변경 완료")
