"""
FastAPI 서버

기사 스크래핑 모듈을 위한 RESTful API 서버입니다.
프론트엔드에서 기사 URL을 제출하면 스크래핑 결과를 JSON으로 반환합니다.

엔드포인트:
- POST /scrape: 기사 URL을 받아 스크래핑 수행
- GET /health: 서버 상태 확인
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
import logging
import os
from dotenv import load_dotenv

from scraper import scrape_article, Article

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="CR Template Hub API",
    description="한국 주요 언론사 기사 스크래핑 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS enabled for origins: {allowed_origins}")


# Pydantic 모델 정의

class ScrapeRequest(BaseModel):
    """스크래핑 요청 모델"""
    url: str = Field(
        ...,
        description="스크래핑할 기사 URL",
        example="https://n.news.naver.com/mnews/article/001/0014612345"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://n.news.naver.com/mnews/article/001/0014612345"
            }
        }


class ArticleResponse(BaseModel):
    """스크래핑 결과 응답 모델"""
    title: str = Field(..., description="기사 제목")
    author: str = Field(..., description="기자명")
    press: str = Field(..., description="언론사명")
    published_at: str = Field(..., description="발행일시 (YYYY-MM-DD HH:MM)")
    body: str = Field(..., description="기사 본문")
    original_url: str = Field(..., description="원본 기사 URL")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "기사 제목 예시",
                "author": "홍길동 기자",
                "press": "연합뉴스",
                "published_at": "2025-11-15 10:30",
                "body": "기사 본문 내용...",
                "original_url": "https://www.yna.co.kr/view/AKR20251115000100001"
            }
        }


class ErrorResponse(BaseModel):
    """에러 응답 모델"""
    error: str = Field(..., description="에러 메시지")
    detail: Optional[str] = Field(None, description="에러 상세 정보")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "스크래핑 실패",
                "detail": "지원하지 않는 언론사입니다"
            }
        }


# API 엔드포인트

@app.get("/", tags=["Root"])
async def root():
    """루트 엔드포인트 - API 정보 반환"""
    return {
        "name": "CR Template Hub API",
        "version": "1.0.0",
        "description": "한국 주요 언론사 기사 스크래핑 API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """서버 상태 확인 엔드포인트"""
    return {
        "status": "healthy",
        "service": "CR Template Hub API",
        "version": "1.0.0"
    }


@app.post(
    "/scrape",
    response_model=ArticleResponse,
    responses={
        200: {
            "description": "스크래핑 성공",
            "model": ArticleResponse
        },
        400: {
            "description": "잘못된 요청 (URL 형식 오류, 지원하지 않는 언론사 등)",
            "model": ErrorResponse
        },
        500: {
            "description": "서버 내부 오류 (스크래핑 실패, 네트워크 오류 등)",
            "model": ErrorResponse
        }
    },
    tags=["Scraping"]
)
async def scrape_news_article(request: ScrapeRequest):
    """
    기사 URL을 받아 스크래핑을 수행하고 결과를 JSON으로 반환합니다.

    **지원 언론사:**
    - 포털: 네이버 뉴스, 다음 뉴스
    - 언론사: 연합뉴스, 조선일보, 중앙일보, 한겨레, 한국경제

    **요청 예시:**
    ```json
    {
        "url": "https://n.news.naver.com/mnews/article/001/0014612345"
    }
    ```

    **성공 응답 예시 (200):**
    ```json
    {
        "title": "기사 제목",
        "author": "홍길동 기자",
        "press": "연합뉴스",
        "published_at": "2025-11-15 10:30",
        "body": "기사 본문 내용...",
        "original_url": "https://www.yna.co.kr/view/AKR20251115000100001"
    }
    ```

    **에러 응답 예시 (400/500):**
    ```json
    {
        "error": "스크래핑 실패",
        "detail": "지원하지 않는 언론사입니다"
    }
    ```
    """
    logger.info(f"스크래핑 요청 수신: {request.url}")

    try:
        # 스크래핑 실행
        article: Article = scrape_article(request.url)

        logger.info(f"스크래핑 성공: {article.title[:50]}...")

        # Article 객체를 ArticleResponse 형식으로 변환
        return ArticleResponse(
            title=article.title,
            author=article.author,
            press=article.press,
            published_at=article.published_at,
            body=article.body,
            original_url=article.original_url
        )

    except ValueError as e:
        # 스크래핑 로직에서 발생한 예상된 에러 (400 Bad Request)
        logger.warning(f"스크래핑 실패 (클라이언트 오류): {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "스크래핑 실패",
                "detail": str(e)
            }
        )

    except Exception as e:
        # 예상하지 못한 서버 내부 오류 (500 Internal Server Error)
        logger.error(f"스크래핑 실패 (서버 오류): {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "서버 내부 오류",
                "detail": "스크래핑 처리 중 예상치 못한 오류가 발생했습니다"
            }
        )


if __name__ == "__main__":
    import uvicorn

    # 개발 환경에서 직접 실행 시
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"서버 시작: {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # 개발 모드에서 코드 변경 시 자동 리로드
        log_level="info"
    )
