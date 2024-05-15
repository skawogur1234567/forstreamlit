
import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from PIL import Image


enter = '''

'''
st.title('QQQ 크롤링')
st.header('웹 스크레이핑')
st.subheader('')
text1 = '''웹 페이지는

    정적 웹페이지 - 클릭할게 없어서 내용이 안 바뀌는 페이지
    동적 웹 페이지 - 클릭하면 내용이 바뀌는 페이지'''
st.text(text1)
text1_1 ='''이렇게 나누어집니다
당연히 정적 웹페이지가 더 쉽고 내용도 간단해서 가져오기도 쉽습니다'''
st.text(text1_1)



text2 = '저희가 가져올 페이지'
QQQlink = 'https://www.schwab.wallst.com/schwab/Prospect/research/etfs/schwabETF/index.asp?type=holdings&symbol=QQQ'
text2_1='''이 페이지 들어가보시면 60개로보기 다음 페이지 클릭하기 이런 버튼들 있지 않습니까?
안타깝게도 이 버튼들 클릭해서 페이지가 바뀌는
동적 웹 페이지 입니다.
'''
st.text(enter)

st.text(text2)
st.text(QQQlink)
st.text(text2_1)
st.text(enter)


text3 = '''정적 웹페이지 크롤링은
파이썬 코드 창에
!pip install bs4
이거만 실행하면 딱히 더 할건 없는데'''
st.text(text3)
st.text(enter)


text_4 = '''
저희가 해야하는 동적 웹페이지 크롤링은
!pip install Selenium 하는건 문제 없는데
아마도 코랩에서는 실행이 안될겁니다
아마도 driver=Chrome( ) 이 부분에서 오류 뜰 듯 합니다
로컬 환경에서 실행해야해서 그런거 같은데
저는 아나콘다 주피터노트북으로 실행했습니다
'''
st.text(text_4)
st.text(enter)

st.text('아나콘다 설치, 크롬드라이버 설치는 문서 하단에 첨부해두었습니다.')
st.text(enter)

st.subheader('패키지 불러오기')
code = '''
import pandas as pd
import numpy as np
import requests
from io import StringIO
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
'''
st.code(code)
st.text(enter)

st.subheader('1. 크롬 창 띄우기')
code1 = '''
driver = Chrome()
url = 'https://www.schwab.wallst.com/schwab/Prospect/research/etfs/schwabETF/index.asp?type=holdings&symbol=QQQ'
driver.get(url)
'''
st.code(code1)
st.text(enter)

st.subheader('2. 60개로 보기 클릭')
text5 = '''1. CTRL + SHIFT + C 눌러서
2. 표 밑의 Show 20 40 60 PAGE의 60 클릭
3. Elements 창에 <a perpage=60 .... 이라고 되어있는 부분 오른쪽 클릭
4. copy의 Copy Xpath 클릭해서 확인하면 //*[@id="PaginationContainer"]/ul[1]/li[4]/a
5. 다시 파이썬 코드로 돌아가서 element 변수에 Xpath 저장 - > 클릭할 대상을 저장하는 과정
6. 그리고 element 클릭'''
code2 = '''
element = WebDriverWait(driver, 5).until(
EC.presence_of_element_located((By.XPATH, '//*[@id="PaginationContainer"]/ul[1]/li[4]/a'))
)
element.click()
'''


st.markdown(text5)
st.code(code2)
st.text(enter)

st.subheader('3. 페이지로부터 데이터프레임 읽어오기')
st.markdown('''
1. page_html 에 지금 페이지의 html 텍스트 전체를 저장
2. df_list에 StringIO를 통해 html 텍스트 가공한 내용들을 저장
df_list는 리스트 형태이긴 한데 리스트의 요소가 데이터프레임''')
st.code('''
page_html = driver.page_source
df_list = pd.read_html(StringIO(page_html))
''')
st.code('df_list[1].head(3)')
url = 'https://raw.githubusercontent.com/skawogur1234567/forstreamlit/main/csv/df_holings1.csv'
response = requests.get(url)
with open('df_holings1.csv', 'wb') as f:
    f.write(response.content)
df_holings1 = pd.read_csv('df_holings1.csv')
st.dataframe(df_holings1.head(3))




st.subheader('4. 데이터 프레임 추출')
st.markdown('''
1. 사실 원래대로라면 Xpath 저장하고 그거 대로 추출하는게 정석이지만 경험상 아무 숫자 찍어넣고 찾아보는게 훨씬 빠른듯 합니다
2. df_holdings1 에 불러온 데이터 프레임 저장
3. 날짜, 마지막 가격은 df_list[0]에 있음
4. 날짜는 iloc[1]로 추출, 마지막 가격은 iloc[0]으로 추출 후 형식 에 맞게 가공
''')
st.code('df_holdings1 = df_list[1]')
st.code('df_holdings1.head(3)')
st.dataframe(df_holings1.head(3))

url1 = 'https://raw.githubusercontent.com/skawogur1234567/forstreamlit/main/csv/df_list(0).csv'
response = requests.get(url1)
with open('df_list(0).csv', 'wb') as f:
    f.write(response.content)
df_list_0 = pd.read_csv('df_list(0).csv')



st.code('df_list[0]')
st.dataframe(df_list_0)
st.code('''
date = df_list[0]["Last Price"].iloc[1].replace("As of close\xa0", "")
last_price = float(df_list[0]["Last Price"].iloc[0].replace("$", ""))
''')
st.code('last_price')
st.markdown("442.06")
st.code('date')
st.markdown("'05/10/2024'")




st.subheader('5. 2페이지로 넘어가기')
st.markdown('''
1. element2에 < Previous 1 2 Next > 중 2번 버튼의 Xpath를 Copy Xpath를 통해 복사해서 저장
2. element2.click()으로 2페이지로 넘어가기
''')
st.code('''
element2 = WebDriverWait(driver, 5).until(
EC.presence_of_element_located((By.XPATH, '//*[@id="PaginationContainer"]/ul[2]/li[3]/a'))
)
element2.click()
''')


st.subheader('6. 페이지로부터 데이터프레임 읽어오기')
st.markdown('''
1. page_html2 에 지금 페이지의 html 텍스트 전체를 저장
2. df_lis2t에 StringIO를 통해 html 텍스트 가공한 내용들을 저장
''')
st.code('''page_html2 = driver.page_source
df_list2 = pd.read_html(StringIO(page_html2))
''')



st.subheader('7. 데이터 프레임 추출')
st.markdown('''
1. df_holdings2 에 불러온 데이터 프레임 저장
2. 날짜, 마지막 가격은 df_list[0]에 있음
3. 날짜는 iloc[1]로 추출, 마지막 가격은 iloc[0]으로 추출 후 형식 에 맞게 가공
''')
st.code('df_holdings2 = df_list2[1]')
st.code('df_holdings2.head(3)')

url3 = 'https://raw.githubusercontent.com/skawogur1234567/forstreamlit/main/csv/df_holdings2.csv'
response3 = requests.get(url3)
with open('df_holings2.csv', 'wb') as f:
    f.write(response3.content)
df_holings2 = pd.read_csv('df_holings2.csv')
st.dataframe(df_holings2.head(3))






st.subheader('8.데이터 병합')
st.code('df = pd.concat([df_holdings1,df_holdings2],axis=0)')
st.code('df.head(3)')
df = pd.concat([df_holings1,df_holings2],axis=0)
st.dataframe(df.head(3))
st.code('df.shape')
st.text(df.shape)

st.subheader('9.파일로 저장')
st.code("df.to_excel('QQQ.xlsx',index=False)")


# #=====================================================
# #=====================================================
# #=====================================================
# #=====================================================
# #=====================================================
# #=====================================================
# #=====================================================
# #=====================================================
# #=====================================================

csv_data = df.to_csv()
# excel_data = BytesIO()
# df.to_excel(excel_data)

# st.subheader('엑셀 파일로 다운로드')
# st.download_button('엑셀 파일 다운로드',excel_data,file_name='qqq_crawling.xlsx')

st.subheader('CSV 파일로 다운로드')
st.download_button('CSV 파일 다운로드',csv_data,file_name='qqq_crawling.csv')


st.subheader('10.df 정제')
st.markdown('1. 티커가 -- 인거 확인')
st.code("df[df['Symbol']=='--']")
df[df['Symbol']=='--']
st.dataframe(df[df['Symbol']=='--'])
st.markdown('2. Description이 Coca-Cola Europacific Partners PLC인거는 CCEP로 Symbol 변경 ')
st.code("df.loc[df['Description']=='Coca-Cola Europacific Partners PLC','Symbol']='CCEP'")
df.loc[df['Description']=='Coca-Cola Europacific Partners PLC','Symbol']='CCEP'
st.dataframe(df[df['Symbol']=='CCEP'])
st.markdown('3. Description이 cash는 제거')
st.code("df = df[df['Symbol']!='--']")
df = df[df['Symbol']!='--']
st.dataframe(df.head(3))
st.markdown('4. df의 개수 확인')
st.code("df.shape")
st.markdown(df.shape)


st.subheader("11. FINVIZ.COM에서 리스트들 가져오기")
import threading
import os
import time
st.write('1. 패키지 불러오기')
st.code('''
import threading
import os
import time
''')
st.markdown("2.finviz_crawling이라는 함수 생성")
st.code('''
def finviz_crawling(symbols):
    # 파라미터로 넣어주는 symbols의 타입은 리스트 형태여야 합니다
    
    # 1. 링크로부터 연결되었는지 확인
    headers = {'User-agent': 'Mozila/5.0'}
    result = pd.DataFrame()
    
    for symbol in symbols:
        url = f'https://finviz.com/quote.ashx?t={symbol}&p=d'
        response = requests.get(url, headers=headers)
        
        # 해당 티커가 finviz.com에 없으면 다음 티커로 넘어가게 만들었습니다.
        if response.status_code != 200:
            continue
            
        # 2. 표 가져오기
        df = pd.read_html(StringIO(response.text))[6]
        
        # 3. 데이터 가공
        data = [df.iloc[:, i:i+2].rename(columns={df.columns[i]: 0, df.columns[i + 1]: 1}) 
                      for i in range(0, len(df.columns), 2)]
        data1 = pd.concat(data, axis=0).transpose()
        data1.columns = data1.iloc[0]
        data1 = data1.iloc[1:].reset_index(drop=True)
        data1['Ticker'] = symbol
        data1.reset_index(drop=True, inplace=True)
        result = pd.concat([result, data1], ignore_index=True)
        
        time.sleep(1)
        
    return result
''')
st.markdown('3. 불러올 티커 리스트 설정')
st.write("불러올 티커 리스트는 df의 'Symbol'컬럼에 있습니다")
st.code('''
ticker_list = df['Symbol']
len(ticker_list)
''')
ticker_list = df['Symbol']
len(ticker_list)
st.write('101')

st.markdown('4. final에 finviz_crawling을 통해 df의 Symbol컬럼에 있는 값들 가져오기')
st.write('이거 원래 한 2~3분 시간 걸립니다')
url4 = 'https://raw.githubusercontent.com/skawogur1234567/forstreamlit/main/csv/merge_test.csv'
response4 = requests.get(url4)
with open('merge_test.csv', 'wb') as f:
    f.write(response4.content)
merge_test = pd.read_csv('merge_test.csv',header=0)

st.code('''
final = finviz_crawling(ticker_list)
print(final.shape)
final.head(3)
''')
st.write('101,79')
st.dataframe(merge_test.head(3))
csv_data1 = merge_test.to_csv()
st.subheader('CSV 파일로 다운로드')
st.download_button('CSV 파일 다운로드',csv_data1,file_name='qqq_finviz.csv')







st.subheader('아나콘다 설치')

youtube_url = 'https://youtu.be/YNej6WeVpD4?si=FDlSCm00_p9pqkDy'
st.write(youtube_url)
