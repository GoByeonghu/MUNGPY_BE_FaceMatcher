import pandas as pd
from datetime import datetime

# 현재 연도 구하기
current_year = datetime.now().year

# Excel 파일 읽기
df = pd.read_excel('../dogs.xlsx', sheet_name='sheet1', engine='openpyxl')

# 데이터 가공 및 SQL INSERT 명령어 생성
insert_statements = []
for index, row in df.iloc[0:147].iterrows():
    age = current_year - int(row['출생일'])  # S열의 년도 계산
    sex = row['성별']
    kind = row['품종']
    name = "없음"
    image = f"{row['공고번호']}.jpg"
    personality = row['구조시 특징']
    description = "없음"
    matchReason = "없음"
    rescuePlace = row['발생장소']
    protectPlace = row['보호센터']
    protectTelno = row['보호센터연락처']
    #expirationDate
    
    # SQL INSERT 명령어 생성
    sql = (f"INSERT INTO dogs (age, sex, kind, name, image, personality, description, match_reason, rescue_place, "
           f"protect_place, protect_telno) VALUES "
           f"({age}, '{sex}', '{kind}', '{name}', '{image}', '{personality}', '{description}', '{matchReason}', "
           f"'{rescuePlace}', '{protectPlace}', '{protectTelno}');")
    #SQL INSERT 명령어 생성
    insert_statements.append(sql)

# SQL 명령어를 파일에 저장
with open('insert_statements.sql', 'w') as file:
    for statement in insert_statements:
        file.write(statement + '\n')

print("SQL INSERT statements have been written to 'insert_statements.sql'.")

# mysql -u your_username -p your_database_name < insert_statements.sql
