import requests
from bs4 import BeautifulSoup
import os

# 웹페이지 URL
url = "https://www.animal.go.kr/front/awtis/protection/protectionList.do?totalCount=146&pageSize=146&boardId=&desertionNo=&menuNo=1000000060&searchSDate=2019-08-05&searchEDate=2024-08-05&searchUprCd=6500000&searchOrgCd=&searchCareRegNo=&searchUpKindCd=417000&searchKindCd=&searchSexCd=&searchRfid=&&page=1"

# 페이지 요청 및 HTML 파싱
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# 이미지와 이름을 추출하여 저장
animals_list = soup.find('ul', class_='animals-list')

if animals_list:
    animal_items = animals_list.find_all('li')

    for item in animal_items:
        try:
            # 이미지 URL 추출
            img_tag = item.find('div', class_='thum-img').find('img')
            img_src = img_tag['src']
            img_url = "https://www.animal.go.kr" + img_src

            # 공고번호 추출
            info_div = item.find('li', class_='info').find('div', class_='info-item')
            announcement_number = info_div.find('div', class_='value').text.strip()

            # 이미지 다운로드
            img_data = requests.get(img_url).content

            # 파일 저장
            file_name = f"{announcement_number}.jpg"
            with open(file_name, 'wb') as file:
                file.write(img_data)
            
            print(f"{file_name} 저장 완료")
        
        except Exception as e:
            print(f"오류 발생: {e}")
else:
    print("동물 목록을 찾을 수 없습니다.")


# import os
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin
# from urllib.request import urlretrieve

# # 저장할 디렉토리 생성
# os.makedirs('dog_images', exist_ok=True)

# # 기본 URL 설정
# base_url = "https://www.animal.go.kr/front/awtis/protection/protectionList.do"

# # 페이지 번호를 변경하면서 데이터를 크롤링
# for page in range(1, 16):
#     params = {
#         'totalCount': 146,
#         'pageSize': 10,
#         'menuNo': 1000000060,
#         'searchSDate': '2019-08-05',
#         'searchEDate': '2024-08-05',
#         'searchUprCd': 6500000,
#         'searchUpKindCd': 417000,
#         'page': page
#     }
    
#     # 요청 보내기
#     response = requests.get(base_url, params=params)
#     response.raise_for_status()
    
#     # BeautifulSoup을 사용하여 HTML 파싱
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # 이미지 URL 추출
#     img_tags = soup.select('div.img img')  # 이미지 태그를 선택하는 CSS 선택자
#     for img_tag in img_tags:
#         img_url = urljoin(base_url, img_tag['src'])
#         img_name = os.path.basename(img_url)
#         img_path = os.path.join('dog_images', img_name)
        
#         # 이미지 다운로드
#         urlretrieve(img_url, img_path)
#         print(f"Downloaded {img_path}")

# print("All images downloaded.")