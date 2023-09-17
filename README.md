## [KHUDA] 경희대학교 도서관 책 추천 GPT : desKHU
```
경희대학교 도서관에는 여러분을 위한 책이 기다리고 있습니다.
```
***desKHU***는 사용자의 관심사를 입력하면 경희대학교 도서관에 소장된 책 중에서 관심사에 맞는 책을 추천해주는 서비스입니다.

본 프로젝트의 메인 아이디어는 사용자의 관심사와 책 소개에 기반한 Content-Based Filtering입니다. 
1. 사용자의 관심사를 텍스트로 입력받아 이와 관련된 쿼리를 생성합니다. 
2. 해당 쿼리를 바탕으로 책을 검색합니다.
3. 책의 isbn을 통해 소장정보를 확인합니다.
4. 소장된 책을 중심으로 책 소개와 사용자의 관심사를 임베딩하여 유사도를 계산합니다.
5. 사용자의 관심사와 가장 유사한 소개를 갖는 책 k개 추천합니다.
> desKHU를 이용하여 관심사에 맞는 도서를 찾아보세요!

## Members
|                     최용빈                     |                홍민혁                |             
| :---------------------------------------------: | :----------------------------------: | 
|`Modeling`, `Serving`|`Modeling`|
|<img src='https://avatars.githubusercontent.com/u/64704608?v=4' alt="whybe-choi" width="100" height="100">|<img src='https://avatars.githubusercontent.com/u/108979014?v=4' alt="Minhyuckhong" width="100" height="100">|
|[GitHub](https://github.com/whybe-choi)|[GitHub](https://github.com/MinhyukHong)|

## Architecture
<img width="856" alt="스크린샷 2023-07-26 오전 1 52 56" src="https://github.com/whybe-choi/khuda-project-3/assets/64704608/73312506-07ba-484c-9116-c4958e52deaa">

## Preview
![vllo 5](https://github.com/whybe-choi/khuda-project-3/assets/64704608/190665b7-6a11-4f0e-97b1-7c8285a51768)

![vllo 4](https://github.com/whybe-choi/khuda-project-3/assets/64704608/6fb86f57-e2b4-414f-a431-62aaf41dc65b)

<img width="500" alt="스크린샷 2023-07-23 오전 1 35 16" src="https://github.com/whybe-choi/khuda-project-3/assets/64704608/b25e2362-e704-473c-b97e-cc8cfa0d4732">

## How to use
1. 필요한 패키지 설치
```
pip install -r requirements.txt
```
2. streamlit 실행
```
streamlit run app.py
```
3. OpenAI API 키 입력 / GPT 모델 및 추천 결과 수 선택
<img width="319" alt="스크린샷 2023-07-25 오전 10 52 42" src="https://github.com/whybe-choi/khuda-project-3/assets/64704608/e6c0550c-39da-4144-917e-89640586021e">

4. 관심사 입력
<img width="672" alt="스크린샷 2023-07-25 오전 10 57 19" src="https://github.com/whybe-choi/khuda-project-3/assets/64704608/79cc3bfb-b4d8-4817-a406-1f8e0ef806f4">

## Reference
- https://github.com/Alfex4936/Ajou-Library-GPT