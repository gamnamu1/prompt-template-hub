# [CR-PROJECT] 스크래핑 모듈 구현 가이드 (For Claude Code)

## 1. 최종 목표 (Goal)

사용자가 입력한 모든 유형의 뉴스 기사 URL에서 **광고, 댓글, 관련 뉴스 등 불필요한 요소를 모두 제거**하고, **기사 본문과 핵심 메타데이터(제목, 언론사, 기자, 작성일)를 정확하게 추출**하는 파이썬 모듈 `scraping_module.py`를 구현합니다.

## 2. 개발 우선순위 및 범위

총 6개의 뉴스 소스를 대상으로 하며, 아래 명시된 순서대로 개발을 진행합니다.

| 우선순위 | 구분 | 대상 | 도메인 (예시) | 비고 |
| :--- | :--- | :--- | :--- | :--- |
| **1** | 포털 | **네이버 뉴스** | `n.news.naver.com` | **최우선 구현** |
| **2** | 포털 | **다음 뉴스** | `v.daum.net` | |
| **3** | 언론사 | **연합뉴스** | `www.yna.co.kr` | |
| **4** | 언론사 | **조선일보** | `www.chosun.com` | |
| **5** | 언론사 | **한겨레** | `www.hani.co.kr` | |
| **6** | 언론사 | **한국경제** | `www.hankyung.com` | |

### **범위에서 제외 (Out of Scope)**

*   **네이트 뉴스**: 시장 점유율이 낮아 구현 우선순위에서 제외합니다.
*   **YouTube 뉴스**: 영상/텍스트 혼합 형태로 별도 분석이 필요하므로 이번 단계에서는 다루지 않습니다.

## 3. 기술 명세 (Technical Specifications)

### 3.1. 최종 산출물

*   `scraping_module.py` 파일 1개

### 3.2. 표준 데이터 구조 (Data Class)

모든 스크래퍼는 아래 `Article` 데이터 클래스 형식으로 결과를 반환해야 합니다.

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    title: str          # 기사 제목
    author: str         # 기자 이름 (이메일 포함 시 함께 추출)
    press: str          # 언론사명
    published_at: str   # 발행일시 (YYYY-MM-DD HH:MM 형식)
    body: str           # 기사 본문 (텍스트만)
    original_url: str   # 원본 기사 URL
```

### 3.3. 메인 아키텍처

URL을 받아 출처를 식별하고, 적절한 스크래퍼를 호출하는 Dispatcher 패턴을 사용합니다.

```python
# scraping_module.py

# [여기에 Article 데이터 클래스 정의]

def scrape_naver(url: str) -> Article:
    # 네이버 뉴스 스크래핑 로직 구현
    pass

def scrape_daum(url: str) -> Article:
    # 다음 뉴스 스크래핑 로직 구현
    pass

# [나머지 4개 언론사 스크래퍼 함수 정의]

SOURCE_MAP = {
    "naver.com": scrape_naver,
    "daum.net": scrape_daum,
    "yna.co.kr": scrape_yonhap, # 함수명은 자유롭게 정의
    "chosun.com": scrape_chosun,
    "hani.co.kr": scrape_hani,
    "hankyung.com": scrape_hankyung,
}

def scrape_article(url: str) -> Article:
    """입력된 URL을 분석하여 적절한 스크래퍼를 호출하고 결과를 반환"""
    # 1. 단축 URL 처리 (requests.head(..., allow_redirects=True) 사용)
    # 2. 최종 URL의 도메인을 확인하여 SOURCE_MAP에서 적절한 함수 선택
    # 3. 선택된 함수를 호출하여 스크래핑 실행
    # 4. 결과가 없거나 에러 발생 시 예외 처리
    pass
```

## 4. 소스별 상세 가이드

### **1. 네이버 뉴스**
*   **URL 패턴**: `n.news.naver.com/mnews/article/{언론사코드}/{기사번호}`
*   **CSS Selectors**:
    *   **제목**: `#title_area > span`
    *   **언론사**: `img.media_end_head_top_logo_img.light_type` 의 `title` 속성
    *   **기자**: `.media_end_head_journalist_name`
    *   **발행일시**: `.media_end_head_info_datestamp_time`
    *   **본문**: `#dic_area`
*   **특이사항**: 본문 내 불필요한 `div`, `span` 태그 및 광고 스크립트 제거 필요.

### **2. 다음 뉴스**
*   **URL 패턴**: `v.daum.net/v/{기사ID}`
*   **CSS Selectors**:
    *   **제목**: `.tit_view`
    *   **언론사**: `img#kakaoServiceLogo` 의 `alt` 속성
    *   **기자**: `.info_view .txt_info`
    *   **발행일시**: `.info_view .num_date`
    *   **본문**: `.article_view`
*   **특이사항**: 본문 내 "관련기사", "많이 본 뉴스" 등 섹션 제외 처리.

## 5. 필수 준수 사항

1.  **에러 처리**: 스크래핑 실패, 페이지 없음(404), 구조 변경 등의 경우 `None`을 반환하거나 적절한 예외를 발생시켜야 합니다.
2.  **클린 텍스트**: 최종 `body` 텍스트에는 HTML 태그, CSS, Javascript 코드가 포함되어서는 안 됩니다.
3.  **외부 라이브러리**: `requests`와 `BeautifulSoup4` 사용을 권장합니다.
4.  **주석**: 각 스크래퍼 함수 상단에 대상 사이트와 간단한 설명을 주석으로 추가해주세요.

이 가이드를 바탕으로 `scraping_module.py` 구현을 시작해주세요. 각 소스별로 개별 PR을 생성하여 순차적으로 리뷰를 진행하는 것을 권장합니다.
