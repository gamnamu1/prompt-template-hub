"""
기사 스크래핑 모듈

한국 주요 언론사 및 포털 뉴스 사이트에서 기사 본문과 메타데이터를 추출합니다.
광고, 댓글, 관련 뉴스 등 불필요한 요소를 제거하고 핵심 정보만 반환합니다.

지원 대상 (7개 언론사):
- 포털: 네이버 뉴스, 다음 뉴스
- 언론사: 연합뉴스, 조선일보, 중앙일보, 한겨레, 한국경제

참고:
- 모든 스크래퍼는 표준 Article 데이터클래스 형식으로 결과를 반환합니다.
- CSS 셀렉터는 웹사이트 구조 변경에 따라 조정이 필요할 수 있습니다.
- 실제 사용 전 각 언론사별 테스트를 권장합니다.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Callable
import re
import requests
from bs4 import BeautifulSoup
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 상수
TIMEOUT = 10  # 초
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'


@dataclass
class Article:
    """
    기사 데이터 표준 구조

    Attributes:
        title: 기사 제목
        author: 기자명 (이메일 포함 가능)
        press: 언론사명
        published_at: 발행일시 (YYYY-MM-DD HH:MM 형식)
        body: 기사 본문 (텍스트만, HTML 태그 제거)
        original_url: 원본 기사 URL
    """
    title: str
    author: str
    press: str
    published_at: str
    body: str
    original_url: str


def clean_text(text: str) -> str:
    """
    텍스트에서 불필요한 공백, 줄바꿈을 정리합니다.

    Args:
        text: 정리할 텍스트

    Returns:
        정리된 텍스트
    """
    if not text:
        return ""

    # 연속된 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    # 앞뒤 공백 제거
    text = text.strip()
    return text


def parse_daum_date(date_text: str) -> str:
    """
    다음 뉴스 날짜 형식을 YYYY-MM-DD HH:MM으로 변환합니다.

    Args:
        date_text: "입력 2025.11.14. 오후 2:30" 형식의 텍스트

    Returns:
        "2025-11-14 14:30" 형식의 날짜 문자열

    Examples:
        >>> parse_daum_date("입력 2025.11.14. 오전 9:30")
        "2025-11-14 09:30"
        >>> parse_daum_date("입력 2025.11.14. 오후 2:30")
        "2025-11-14 14:30"
    """
    try:
        # "입력 " 또는 "수정 " 제거
        text = date_text.replace('입력 ', '').replace('수정 ', '').strip()

        # 정규식: "2025.11.14. 오후 2:30" 형식 파싱
        pattern = r'(\d{4})\.(\d{1,2})\.(\d{1,2})\.\s*(오전|오후)\s*(\d{1,2}):(\d{2})'
        match = re.search(pattern, text)

        if not match:
            # 파싱 실패 시 원본 반환
            return text

        year, month, day, meridiem, hour, minute = match.groups()
        hour = int(hour)

        # 오후이고 12시가 아니면 +12
        if meridiem == '오후' and hour != 12:
            hour += 12
        # 오전 12시는 00시로 변환
        elif meridiem == '오전' and hour == 12:
            hour = 0

        return f"{year}-{month.zfill(2)}-{day.zfill(2)} {hour:02d}:{minute}"

    except Exception as e:
        logger.warning(f"날짜 파싱 실패: {date_text}, 에러: {e}")
        return date_text


def resolve_url(url: str) -> str:
    """
    단축 URL을 실제 URL로 변환합니다.

    Args:
        url: 원본 URL (단축 URL 가능)

    Returns:
        최종 리다이렉트된 URL

    Raises:
        requests.RequestException: 네트워크 에러
    """
    try:
        response = requests.head(
            url,
            allow_redirects=True,
            timeout=TIMEOUT,
            headers={'User-Agent': USER_AGENT}
        )
        return response.url
    except requests.RequestException as e:
        logger.error(f"URL 리다이렉트 실패: {url}, 에러: {e}")
        raise


def scrape_naver(url: str) -> Article:
    """
    네이버 뉴스 기사를 스크래핑합니다.

    URL 패턴: n.news.naver.com/mnews/article/{언론사코드}/{기사번호}

    Args:
        url: 네이버 뉴스 기사 URL

    Returns:
        Article 객체

    Raises:
        ValueError: 필수 요소를 찾을 수 없는 경우
        requests.RequestException: 네트워크 에러
    """
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            headers={'User-Agent': USER_AGENT}
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"기사를 찾을 수 없습니다: {url}")
        raise
    except requests.Timeout:
        raise ValueError(f"요청 시간 초과: {url}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목 추출
    title_elem = soup.select_one('#title_area > span')
    if not title_elem:
        raise ValueError("제목을 찾을 수 없습니다")
    title = clean_text(title_elem.get_text())

    # 언론사 추출
    press_elem = soup.select_one('img.media_end_head_top_logo_img.light_type')
    if not press_elem:
        raise ValueError("언론사 정보를 찾을 수 없습니다")
    press = press_elem.get('title', '')

    # 기자명 추출
    author_elem = soup.select_one('.media_end_head_journalist_name')
    author = clean_text(author_elem.get_text()) if author_elem else "기자 정보 없음"

    # 발행일시 추출
    date_elem = soup.select_one('.media_end_head_info_datestamp_time')
    if not date_elem:
        raise ValueError("발행일시를 찾을 수 없습니다")

    # data-date-time 속성에서 추출 (ISO 형식)
    published_raw = date_elem.get('data-date-time', '')
    if published_raw:
        # ISO 형식 (2025-11-14T10:30:00+09:00) → YYYY-MM-DD HH:MM
        try:
            dt = datetime.fromisoformat(published_raw.replace('+09:00', ''))
            published_at = dt.strftime('%Y-%m-%d %H:%M')
        except ValueError:
            published_at = clean_text(date_elem.get_text())
    else:
        published_at = clean_text(date_elem.get_text())

    # 본문 추출
    body_elem = soup.select_one('#dic_area')
    if not body_elem:
        raise ValueError("본문을 찾을 수 없습니다")

    # 본문 내 불필요한 요소 제거
    for tag in body_elem.select('script, style, a.media_end_head_autosummary_button'):
        tag.decompose()

    # 광고 및 관련 기사 제거
    for tag in body_elem.find_all(['div', 'span'], class_=re.compile(r'ad|banner|related', re.I)):
        tag.decompose()

    body = clean_text(body_elem.get_text())

    return Article(
        title=title,
        author=author,
        press=press,
        published_at=published_at,
        body=body,
        original_url=url
    )


def scrape_daum(url: str) -> Article:
    """
    다음 뉴스 기사를 스크래핑합니다.

    URL 패턴: v.daum.net/v/{기사ID}

    Args:
        url: 다음 뉴스 기사 URL

    Returns:
        Article 객체

    Raises:
        ValueError: 필수 요소를 찾을 수 없는 경우
        requests.RequestException: 네트워크 에러
    """
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            headers={'User-Agent': USER_AGENT}
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"기사를 찾을 수 없습니다: {url}")
        raise
    except requests.Timeout:
        raise ValueError(f"요청 시간 초과: {url}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목 추출
    title_elem = soup.select_one('.tit_view')
    if not title_elem:
        raise ValueError("제목을 찾을 수 없습니다")
    title = clean_text(title_elem.get_text())

    # 언론사 추출
    press_elem = soup.select_one('img#kakaoServiceLogo')
    if not press_elem:
        raise ValueError("언론사 정보를 찾을 수 없습니다")
    press = press_elem.get('alt', '')

    # 기자명 추출
    author_elem = soup.select_one('.info_view .txt_info')
    author = clean_text(author_elem.get_text()) if author_elem else "기자 정보 없음"

    # 발행일시 추출
    date_elem = soup.select_one('.info_view .num_date')
    if not date_elem:
        raise ValueError("발행일시를 찾을 수 없습니다")

    published_text = clean_text(date_elem.get_text())
    # "입력 2025.11.14. 오후 2:30" → "2025-11-14 14:30" 형식으로 변환
    published_at = parse_daum_date(published_text)

    # 본문 추출
    body_elem = soup.select_one('.article_view')
    if not body_elem:
        raise ValueError("본문을 찾을 수 없습니다")

    # 본문 내 불필요한 요소 제거
    for tag in body_elem.select('script, style'):
        tag.decompose()

    # "관련기사", "인기기사" 섹션 제거
    for tag in body_elem.find_all(['div', 'section'], class_=re.compile(r'related|popular|recommend', re.I)):
        tag.decompose()

    body = clean_text(body_elem.get_text())

    return Article(
        title=title,
        author=author,
        press=press,
        published_at=published_at,
        body=body,
        original_url=url
    )


def scrape_yonhap(url: str) -> Article:
    """
    연합뉴스 기사를 스크래핑합니다.

    URL 패턴: www.yna.co.kr/view/...

    Args:
        url: 연합뉴스 기사 URL

    Returns:
        Article 객체

    Raises:
        ValueError: 필수 요소를 찾을 수 없는 경우
        requests.RequestException: 네트워크 에러

    Note:
        CSS 셀렉터는 웹사이트 구조 변경에 따라 조정이 필요할 수 있습니다.
    """
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            headers={'User-Agent': USER_AGENT}
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"기사를 찾을 수 없습니다: {url}")
        raise
    except requests.Timeout:
        raise ValueError(f"요청 시간 초과: {url}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목 추출 - 여러 패턴 시도
    title_elem = (
        soup.select_one('h1.tit') or
        soup.select_one('.article-head h1') or
        soup.select_one('h1')
    )
    if not title_elem:
        raise ValueError("제목을 찾을 수 없습니다")
    title = clean_text(title_elem.get_text())

    # 언론사 - 연합뉴스로 고정
    press = "연합뉴스"

    # 기자명 추출
    author_elem = (
        soup.select_one('.writer') or
        soup.select_one('.byline') or
        soup.select_one('.journalist')
    )
    author = clean_text(author_elem.get_text()) if author_elem else "기자 정보 없음"

    # 발행일시 추출
    date_elem = (
        soup.select_one('div.info-box01 span.txt-time') or
        soup.select_one('.update-time') or
        soup.select_one('time') or
        soup.select_one('.date')
    )
    if not date_elem:
        raise ValueError("발행일시를 찾을 수 없습니다")

    published_text = clean_text(date_elem.get_text())
    # 표준 형식으로 변환 시도
    published_at = published_text

    # 본문 추출
    body_elem = (
        soup.select_one('.article-body') or
        soup.select_one('.story-news') or
        soup.select_one('.content')
    )
    if not body_elem:
        raise ValueError("본문을 찾을 수 없습니다")

    # 본문 내 불필요한 요소 제거
    for tag in body_elem.select('script, style, .ad, .adrs, .related-news'):
        tag.decompose()

    # 광고 및 관련 기사 제거
    for tag in body_elem.find_all(['div', 'aside'], class_=re.compile(r'ad|banner|related|recommend', re.I)):
        tag.decompose()

    body = clean_text(body_elem.get_text())

    return Article(
        title=title,
        author=author,
        press=press,
        published_at=published_at,
        body=body,
        original_url=url
    )


def scrape_chosun(url: str) -> Article:
    """
    조선일보 기사를 스크래핑합니다.

    URL 패턴: www.chosun.com/...

    Args:
        url: 조선일보 기사 URL

    Returns:
        Article 객체

    Raises:
        ValueError: 필수 요소를 찾을 수 없는 경우
        requests.RequestException: 네트워크 에러

    Note:
        CSS 셀렉터는 웹사이트 구조 변경에 따라 조정이 필요할 수 있습니다.
    """
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            headers={'User-Agent': USER_AGENT}
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"기사를 찾을 수 없습니다: {url}")
        raise
    except requests.Timeout:
        raise ValueError(f"요청 시간 초과: {url}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목 추출 - 여러 패턴 시도
    title_elem = (
        soup.select_one('h1.article-header__headline') or
        soup.select_one('.article-title') or
        soup.select_one('h1[itemprop="headline"]') or
        soup.select_one('h1')
    )
    if not title_elem:
        raise ValueError("제목을 찾을 수 없습니다")
    title = clean_text(title_elem.get_text())

    # 언론사 - 조선일보로 고정
    press = "조선일보"

    # 기자명 추출
    author_elem = (
        soup.select_one('.article-header__reporter') or
        soup.select_one('.byline') or
        soup.select_one('[itemprop="author"]') or
        soup.select_one('.reporter')
    )
    author = clean_text(author_elem.get_text()) if author_elem else "기자 정보 없음"

    # 발행일시 추출
    date_elem = (
        soup.select_one('.article-header__date') or
        soup.select_one('time') or
        soup.select_one('[itemprop="datePublished"]') or
        soup.select_one('.date')
    )
    if not date_elem:
        raise ValueError("발행일시를 찾을 수 없습니다")

    # datetime 속성이 있으면 사용
    published_at = (
        date_elem.get('datetime') or
        date_elem.get('content') or
        clean_text(date_elem.get_text())
    )

    # 본문 추출 - 조선일보 특정 셀렉터 우선
    body_elem = (
        soup.select_one('section.article-body') or
        soup.find('section', {'itemprop': 'articleBody'}) or
        soup.select_one('.article-content') or
        soup.select_one('.story-body')
    )
    if not body_elem:
        raise ValueError("본문을 찾을 수 없습니다")

    # 본문 내 불필요한 요소 제거
    for tag in body_elem.select('script, style, .ad, .advertisement, .related-article'):
        tag.decompose()

    # 광고 및 관련 기사 제거
    for tag in body_elem.find_all(['div', 'aside', 'section'], class_=re.compile(r'ad|banner|related|recommend|promotion', re.I)):
        tag.decompose()

    body = clean_text(body_elem.get_text())

    return Article(
        title=title,
        author=author,
        press=press,
        published_at=published_at,
        body=body,
        original_url=url
    )


def scrape_joongang(url: str) -> Article:
    """
    중앙일보 기사를 스크래핑합니다.

    URL 패턴: www.joongang.co.kr/article/...

    Args:
        url: 중앙일보 기사 URL

    Returns:
        Article 객체

    Raises:
        ValueError: 필수 요소를 찾을 수 없는 경우
        requests.RequestException: 네트워크 에러

    Note:
        CSS 셀렉터는 웹사이트 구조 변경에 따라 조정이 필요할 수 있습니다.
    """
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            headers={'User-Agent': USER_AGENT}
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"기사를 찾을 수 없습니다: {url}")
        raise
    except requests.Timeout:
        raise ValueError(f"요청 시간 초과: {url}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목 추출 - 여러 패턴 시도
    title_elem = (
        soup.select_one('h1.headline') or
        soup.select_one('.article-title') or
        soup.select_one('h1[itemprop="headline"]') or
        soup.select_one('.head-title') or
        soup.select_one('h1')
    )
    if not title_elem:
        raise ValueError("제목을 찾을 수 없습니다")
    title = clean_text(title_elem.get_text())

    # 언론사 - 중앙일보로 고정
    press = "중앙일보"

    # 기자명 추출
    author_elem = (
        soup.select_one('.reporter') or
        soup.select_one('.byline') or
        soup.select_one('[itemprop="author"]') or
        soup.select_one('.name')
    )
    author = clean_text(author_elem.get_text()) if author_elem else "기자 정보 없음"

    # 발행일시 추출
    date_elem = (
        soup.select_one('.date-time') or
        soup.select_one('time') or
        soup.select_one('[itemprop="datePublished"]') or
        soup.select_one('.article-date')
    )
    if not date_elem:
        raise ValueError("발행일시를 찾을 수 없습니다")

    # datetime 속성이 있으면 사용
    published_at = (
        date_elem.get('datetime') or
        date_elem.get('content') or
        clean_text(date_elem.get_text())
    )

    # 본문 추출
    body_elem = (
        soup.select_one('.article-body') or
        soup.select_one('#article_body') or
        soup.find('div', {'itemprop': 'articleBody'}) or
        soup.select_one('.article_body')
    )
    if not body_elem:
        raise ValueError("본문을 찾을 수 없습니다")

    # 본문 내 불필요한 요소 제거
    for tag in body_elem.select('script, style, .ad, .advertisement, .related'):
        tag.decompose()

    # 광고 및 관련 기사 제거
    for tag in body_elem.find_all(['div', 'aside'], class_=re.compile(r'ad|banner|related|recommend|ab-', re.I)):
        tag.decompose()

    body = clean_text(body_elem.get_text())

    return Article(
        title=title,
        author=author,
        press=press,
        published_at=published_at,
        body=body,
        original_url=url
    )


def scrape_hani(url: str) -> Article:
    """
    한겨레 기사를 스크래핑합니다.

    URL 패턴: www.hani.co.kr/arti/...

    Args:
        url: 한겨레 기사 URL

    Returns:
        Article 객체

    Raises:
        ValueError: 필수 요소를 찾을 수 없는 경우
        requests.RequestException: 네트워크 에러

    Note:
        CSS 셀렉터는 웹사이트 구조 변경에 따라 조정이 필요할 수 있습니다.
    """
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            headers={'User-Agent': USER_AGENT}
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"기사를 찾을 수 없습니다: {url}")
        raise
    except requests.Timeout:
        raise ValueError(f"요청 시간 초과: {url}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목 추출 - 여러 패턴 시도
    title_elem = (
        soup.select_one('.article-head-title') or
        soup.select_one('.title') or
        soup.select_one('h1.article-title') or
        soup.select_one('h1')
    )
    if not title_elem:
        raise ValueError("제목을 찾을 수 없습니다")
    title = clean_text(title_elem.get_text())

    # 언론사 - 한겨레로 고정
    press = "한겨레"

    # 기자명 추출
    author_elem = (
        soup.select_one('.article-writer') or
        soup.select_one('.byline') or
        soup.select_one('.name') or
        soup.select_one('.reporter')
    )
    author = clean_text(author_elem.get_text()) if author_elem else "기자 정보 없음"

    # 발행일시 추출
    date_elem = (
        soup.select_one('.article-date') or
        soup.select_one('.date-time') or
        soup.select_one('time') or
        soup.select_one('.date')
    )
    if not date_elem:
        raise ValueError("발행일시를 찾을 수 없습니다")

    # datetime 속성이 있으면 사용
    published_at = (
        date_elem.get('datetime') or
        clean_text(date_elem.get_text())
    )

    # 본문 추출
    body_elem = (
        soup.select_one('.article-text') or
        soup.select_one('#article-text') or
        soup.select_one('.article-body') or
        soup.select_one('.text')
    )
    if not body_elem:
        raise ValueError("본문을 찾을 수 없습니다")

    # 본문 내 불필요한 요소 제거
    for tag in body_elem.select('script, style, .ad, .adrs, .related-article'):
        tag.decompose()

    # 광고 및 관련 기사 제거
    for tag in body_elem.find_all(['div', 'aside'], class_=re.compile(r'ad|banner|related|recommend', re.I)):
        tag.decompose()

    body = clean_text(body_elem.get_text())

    return Article(
        title=title,
        author=author,
        press=press,
        published_at=published_at,
        body=body,
        original_url=url
    )


def scrape_hankyung(url: str) -> Article:
    """
    한국경제 기사를 스크래핑합니다.

    URL 패턴: www.hankyung.com/...

    Args:
        url: 한국경제 기사 URL

    Returns:
        Article 객체

    Raises:
        ValueError: 필수 요소를 찾을 수 없는 경우
        requests.RequestException: 네트워크 에러

    Note:
        CSS 셀렉터는 웹사이트 구조 변경에 따라 조정이 필요할 수 있습니다.
    """
    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
            headers={'User-Agent': USER_AGENT}
        )
        response.raise_for_status()
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"기사를 찾을 수 없습니다: {url}")
        raise
    except requests.Timeout:
        raise ValueError(f"요청 시간 초과: {url}")

    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목 추출 - 여러 패턴 시도
    title_elem = (
        soup.select_one('.headline') or
        soup.select_one('.article-tit') or
        soup.select_one('h1.title') or
        soup.select_one('h1')
    )
    if not title_elem:
        raise ValueError("제목을 찾을 수 없습니다")
    title = clean_text(title_elem.get_text())

    # 언론사 - 한국경제로 고정
    press = "한국경제"

    # 기자명 추출
    author_elem = (
        soup.select_one('.byline') or
        soup.select_one('.reporter') or
        soup.select_one('.author') or
        soup.select_one('.journalist')
    )
    author = clean_text(author_elem.get_text()) if author_elem else "기자 정보 없음"

    # 발행일시 추출
    date_elem = (
        soup.select_one('.date-time') or
        soup.select_one('.article-date') or
        soup.select_one('time') or
        soup.select_one('.txt-date')
    )
    if not date_elem:
        raise ValueError("발행일시를 찾을 수 없습니다")

    # datetime 속성이 있으면 사용
    published_at = (
        date_elem.get('datetime') or
        clean_text(date_elem.get_text())
    )

    # 본문 추출
    body_elem = (
        soup.select_one('.article-body') or
        soup.select_one('#articletxt') or
        soup.select_one('.txt-article') or
        soup.select_one('.news-text')
    )
    if not body_elem:
        raise ValueError("본문을 찾을 수 없습니다")

    # 본문 내 불필요한 요소 제거
    for tag in body_elem.select('script, style, .ad, .advertisement, .related'):
        tag.decompose()

    # 광고 및 관련 기사 제거
    for tag in body_elem.find_all(['div', 'aside'], class_=re.compile(r'ad|banner|related|recommend', re.I)):
        tag.decompose()

    body = clean_text(body_elem.get_text())

    return Article(
        title=title,
        author=author,
        press=press,
        published_at=published_at,
        body=body,
        original_url=url
    )


# 도메인 → 스크래퍼 함수 매핑
SOURCE_MAP: Dict[str, Callable[[str], Article]] = {
    "naver.com": scrape_naver,
    "daum.net": scrape_daum,
    "yna.co.kr": scrape_yonhap,
    "chosun.com": scrape_chosun,
    "joongang.co.kr": scrape_joongang,
    "hani.co.kr": scrape_hani,
    "hankyung.com": scrape_hankyung,
}


def scrape_article(url: str) -> Article:
    """
    입력 URL을 분석하여 적절한 스크래퍼를 호출하고 Article 객체를 반환합니다.

    Dispatcher 패턴을 사용하여 URL의 도메인을 확인한 후,
    SOURCE_MAP에서 해당 스크래퍼 함수를 선택하여 실행합니다.

    Args:
        url: 기사 URL (단축 URL 가능)

    Returns:
        Article 객체 (제목, 기자, 언론사, 발행일시, 본문, URL)

    Raises:
        ValueError: 지원하지 않는 언론사 또는 스크래핑 실패
        requests.RequestException: 네트워크 에러

    Examples:
        >>> article = scrape_article("https://n.news.naver.com/mnews/article/...")
        >>> print(article.title)
        "기사 제목"
        >>> print(article.press)
        "언론사명"
    """
    logger.info(f"스크래핑 시작: {url}")

    # 1. 단축 URL 처리
    try:
        final_url = resolve_url(url)
        logger.info(f"최종 URL: {final_url}")
    except requests.RequestException as e:
        raise ValueError(f"URL 접근 실패: {url}") from e

    # 2. 도메인 추출 및 스크래퍼 선택
    scraper_func = None
    for domain, func in SOURCE_MAP.items():
        if domain in final_url:
            scraper_func = func
            logger.info(f"매칭된 도메인: {domain}")
            break

    if not scraper_func:
        supported_domains = ", ".join(SOURCE_MAP.keys())
        raise ValueError(
            f"지원하지 않는 언론사입니다: {final_url}\n"
            f"지원 도메인: {supported_domains}"
        )

    # 3. 스크래핑 실행
    try:
        article = scraper_func(final_url)
        logger.info(f"스크래핑 성공: {article.title[:30]}...")
        return article
    except NotImplementedError as e:
        raise ValueError(str(e)) from e
    except Exception as e:
        logger.error(f"스크래핑 실패: {final_url}, 에러: {e}")
        raise ValueError(f"스크래핑 중 오류 발생: {e}") from e


if __name__ == "__main__":
    # 테스트 예시
    test_urls = [
        # 네이버 뉴스 예시 (실제 URL로 교체 필요)
        # "https://n.news.naver.com/mnews/article/001/0014612345",
        # 다음 뉴스 예시 (실제 URL로 교체 필요)
        # "https://v.daum.net/v/20251114103000123",
    ]

    for test_url in test_urls:
        try:
            article = scrape_article(test_url)
            print(f"\n제목: {article.title}")
            print(f"언론사: {article.press}")
            print(f"기자: {article.author}")
            print(f"발행: {article.published_at}")
            print(f"본문: {article.body[:100]}...")
        except Exception as e:
            print(f"에러: {e}")
