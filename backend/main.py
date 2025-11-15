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
from typing import Optional, Dict
import logging
import os
from dotenv import load_dotenv
import anthropic

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

# Anthropic 클라이언트 초기화
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    logger.warning("ANTHROPIC_API_KEY가 설정되지 않았습니다. /evaluate 엔드포인트를 사용할 수 없습니다.")
    anthropic_client = None
else:
    anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
    logger.info("Anthropic 클라이언트 초기화 완료")


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


class EvaluateRequest(BaseModel):
    """기사 평가 요청 모델"""
    article_body: str = Field(
        ...,
        description="평가할 기사 본문",
        min_length=10
    )
    article_title: Optional[str] = Field(
        None,
        description="기사 제목 (선택사항)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "article_body": "서울 - 오늘 국회에서는...",
                "article_title": "국회, 새로운 법안 통과"
            }
        }


class EvaluationResponse(BaseModel):
    """기사 평가 결과 응답 모델"""
    evaluation_summary: str = Field(..., description="평가 요약")
    scores: Dict[str, int] = Field(..., description="8차원 평가 점수 (1-10)")
    detailed_feedback: Optional[str] = Field(None, description="상세 피드백")

    class Config:
        json_schema_extra = {
            "example": {
                "evaluation_summary": "이 기사는 전반적으로 저널리즘 윤리 기준을 잘 준수하고 있습니다.",
                "scores": {
                    "진실성": 8,
                    "정확성": 7,
                    "공정성": 6,
                    "투명성": 8,
                    "맥락": 7,
                    "인권_존중": 9,
                    "책임성": 7,
                    "독립성": 8
                },
                "detailed_feedback": "진실성과 투명성 측면에서 우수하나, 공정성 측면에서 다양한 관점 제시가 부족합니다."
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


@app.post(
    "/evaluate",
    response_model=EvaluationResponse,
    responses={
        200: {
            "description": "평가 성공",
            "model": EvaluationResponse
        },
        400: {
            "description": "잘못된 요청 (기사 본문 누락, API 키 미설정 등)",
            "model": ErrorResponse
        },
        500: {
            "description": "서버 내부 오류 (Claude API 오류 등)",
            "model": ErrorResponse
        }
    },
    tags=["Evaluation"]
)
async def evaluate_article(request: EvaluateRequest):
    """
    기사 본문을 받아 Claude AI로 저널리즘 윤리 기준 8차원 평가를 수행합니다.

    **평가 기준 (8차원):**
    1. 진실성 (Truth): 사실과 의견 구분, 출처 명시
    2. 정확성 (Accuracy): 통계 정확성, 인용 정확성
    3. 공정성 (Fairness): 다양한 관점, 균형 잡힌 보도
    4. 투명성 (Transparency): 출처 공개, 이해관계 명시
    5. 맥락 (Context): 배경 정보, 역사적 맥락
    6. 인권 존중 (Human Rights): 취약 집단 보호, 차별 없는 표현
    7. 책임성 (Accountability): 오류 정정, 피해 구제
    8. 독립성 (Independence): 외부 압력으로부터 자유

    **요청 예시:**
    ```json
    {
        "article_body": "서울 - 오늘 국회에서...",
        "article_title": "국회, 새로운 법안 통과"
    }
    ```

    **성공 응답 예시 (200):**
    ```json
    {
        "evaluation_summary": "이 기사는 전반적으로 저널리즘 윤리 기준을 잘 준수하고 있습니다.",
        "scores": {
            "진실성": 8,
            "정확성": 7,
            "공정성": 6,
            "투명성": 8,
            "맥락": 7,
            "인권_존중": 9,
            "책임성": 7,
            "독립성": 8
        },
        "detailed_feedback": "..."
    }
    ```
    """
    logger.info("기사 평가 요청 수신")

    # Anthropic 클라이언트 확인
    if not anthropic_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "API 키 미설정",
                "detail": "ANTHROPIC_API_KEY 환경 변수가 설정되지 않았습니다"
            }
        )

    try:
        # Claude에게 보낼 프롬프트 구성
        evaluation_prompt = f"""당신은 저널리즘 윤리 전문가입니다. 다음 기사를 8가지 차원으로 평가해주세요.

**평가 기준:**
1. 진실성 (Truth): 사실과 의견 구분, 출처 명시
2. 정확성 (Accuracy): 통계 정확성, 인용 정확성
3. 공정성 (Fairness): 다양한 관점, 균형 잡힌 보도
4. 투명성 (Transparency): 출처 공개, 이해관계 명시
5. 맥락 (Context): 배경 정보, 역사적 맥락
6. 인권 존중 (Human Rights): 취약 집단 보호, 차별 없는 표현
7. 책임성 (Accountability): 오류 정정, 피해 구제
8. 독립성 (Independence): 외부 압력으로부터 자유

**기사 제목:** {request.article_title if request.article_title else "제목 없음"}

**기사 본문:**
{request.article_body}

**요구사항:**
1. 각 차원별로 1-10점으로 평가하세요 (10점이 가장 우수)
2. 전체 평가 요약을 2-3문장으로 작성하세요
3. 상세 피드백을 제공하세요 (개선이 필요한 부분 중심)

**응답 형식 (JSON):**
{{
  "evaluation_summary": "전체 평가 요약 (2-3문장)",
  "scores": {{
    "진실성": <점수>,
    "정확성": <점수>,
    "공정성": <점수>,
    "투명성": <점수>,
    "맥락": <점수>,
    "인권_존중": <점수>,
    "책임성": <점수>,
    "독립성": <점수>
  }},
  "detailed_feedback": "상세 피드백 (개선이 필요한 부분 중심)"
}}

JSON 형식으로만 응답하세요. 다른 텍스트는 포함하지 마세요."""

        # Claude API 호출
        logger.info("Claude API 호출 시작")
        message = anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": evaluation_prompt
                }
            ]
        )

        # 응답 파싱
        response_text = message.content[0].text
        logger.info(f"Claude API 응답 수신: {len(response_text)} 문자")

        # JSON 파싱
        import json
        try:
            evaluation_data = json.loads(response_text)
        except json.JSONDecodeError:
            # JSON이 아닌 경우, 텍스트에서 JSON 부분 추출 시도
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                evaluation_data = json.loads(json_match.group())
            else:
                raise ValueError("Claude API 응답을 JSON으로 파싱할 수 없습니다")

        logger.info("기사 평가 완료")

        return EvaluationResponse(
            evaluation_summary=evaluation_data.get("evaluation_summary", ""),
            scores=evaluation_data.get("scores", {}),
            detailed_feedback=evaluation_data.get("detailed_feedback")
        )

    except anthropic.APIError as e:
        logger.error(f"Claude API 오류: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Claude API 오류",
                "detail": str(e)
            }
        )

    except ValueError as e:
        logger.warning(f"평가 실패 (클라이언트 오류): {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "평가 실패",
                "detail": str(e)
            }
        )

    except Exception as e:
        logger.error(f"평가 실패 (서버 오류): {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "서버 내부 오류",
                "detail": "평가 처리 중 예상치 못한 오류가 발생했습니다"
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
