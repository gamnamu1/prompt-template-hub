"""
기사 스크래핑 모듈

한국 주요 언론사 및 포털 뉴스 사이트에서 기사 본문과 메타데이터를 추출합니다.
광고, 댓글, 관련 뉴스 등 불필요한 요소를 제거하고 핵심 정보만 반환합니다.

지원 대상:
- Phase 1: 네이버 뉴스, 다음 뉴스
- Phase 2: 연합뉴스, 조선일보, 중앙일보, 한겨레, 한국경제
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
    # 다음 형식: "입력 2025.11.14. 오후 2:30" → "2025-11-14 14:30"
    try:
        # "입력 " 제거
        published_text = published_text.replace('입력 ', '').replace('수정 ', '')
        # "2025.11.14. 오후 2:30" → datetime 변환
        # 간단히 텍스트 그대로 유지 (정규식으로 변환 가능하지만 복잡도 증가)
        published_at = published_text
    except Exception:
        published_at = published_text

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
    연합뉴스 기사를 스크래핑합니다. (Phase 2 구현 예정)

    Args:
        url: 연합뉴스 기사 URL

    Returns:
        Article 객체

    Raises:
        NotImplementedError: 아직 구현되지 않음
    """
    raise NotImplementedError("연합뉴스 스크래퍼는 Phase 2에서 구현 예정입니다")


def scrape_chosun(url: str) -> Article:
    """
    조선일보 기사를 스크래핑합니다. (Phase 2 구현 예정)

    Args:
        url: 조선일보 기사 URL

    Returns:
        Article 객체

    Raises:
        NotImplementedError: 아직 구현되지 않음
    """
    raise NotImplementedError("조선일보 스크래퍼는 Phase 2에서 구현 예정입니다")


def scrape_joongang(url: str) -> Article:
    """
    중앙일보 기사를 스크래핑합니다. (Phase 2 구현 예정)

    Args:
        url: 중앙일보 기사 URL

    Returns:
        Article 객체

    Raises:
        NotImplementedError: 아직 구현되지 않음
    """
    raise NotImplementedError("중앙일보 스크래퍼는 Phase 2에서 구현 예정입니다")


def scrape_hani(url: str) -> Article:
    """
    한겨레 기사를 스크래핑합니다. (Phase 2 구현 예정)

    Args:
        url: 한겨레 기사 URL

    Returns:
        Article 객체

    Raises:
        NotImplementedError: 아직 구현되지 않음
    """
    raise NotImplementedError("한겨레 스크래퍼는 Phase 2에서 구현 예정입니다")


def scrape_hankyung(url: str) -> Article:
    """
    한국경제 기사를 스크래핑합니다. (Phase 2 구현 예정)

    Args:
        url: 한국경제 기사 URL

    Returns:
        Article 객체

    Raises:
        NotImplementedError: 아직 구현되지 않음
    """
    raise NotImplementedError("한국경제 스크래퍼는 Phase 2에서 구현 예정입니다")


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
