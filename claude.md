# CR 템플릿 허브 프로젝트

> **Claude Code 웹 버전을 활용한 한국 언론 기사 저널리즘 윤리 평가 자동화 프로젝트**

---

## 프로젝트 컨텍스트

### 목표
한국 언론 기사의 저널리즘 윤리를 평가하기 위한 자동화된 도구를 개발합니다.

**핵심 기능:**
- 🔗 기사 URL 입력 시 자동 스크래핑
- 🤖 AI 기반 기사 유형 자동 분류
- 📝 기사 유형 + AI 서비스에 최적화된 평가 템플릿 제공
- 💬 사용자 피드백 수집을 통한 지속적 개선

### 핵심 가치
1. **투명성 (Transparency)**: 평가 기준과 프로세스를 명확히 공개
2. **객관성 (Objectivity)**: 다양한 AI 서비스를 활용한 균형 잡힌 평가
3. **접근성 (Accessibility)**: 누구나 쉽게 사용할 수 있는 간단한 인터페이스

### 개발 기간
- **Phase 1 (MVP)**: 5-6주
- **배포 목표**: 2025년 12월

---

## 개발 워크플로우

### 기본 원칙: Think → Implement → Review

모든 기능 개발 시 다음 3단계를 반드시 따릅니다:

1. **Think (사고)**:
   - 설계 전략 제안
   - 엣지 케이스 고려
   - 대안 검토

2. **Implement (구현)**:
   - 설계를 바탕으로 코드 작성
   - 코드 표준 준수
   - 충분한 주석 작성

3. **Review (검토)**:
   - 엣지 케이스 처리 확인
   - 보안 취약점 점검
   - 성능 최적화 검토

**예시:**
```
[Backend Developer 역할]

Task: backend/scraper.py 구현

1. Think:
   - 언론사별 HTML 구조 분석
   - paywall, 동적 콘텐츠 대응 전략

2. Implement:
   - BeautifulSoup4로 스크래핑 로직 구현

3. Review:
   - 404, timeout, encoding 에러 처리 확인
```

### 역할 전환 활용 시점

다음 상황에서 명시적으로 역할을 호출합니다:

- ✅ **백엔드 API 개발**: `[Backend Developer 역할]`
- ✅ **프론트엔드 UI 개발**: `[Frontend Developer 역할]`
- ✅ **코드 품질 검증**: `[Code Reviewer 역할]`
- ❌ **단순 버그 수정/문서 작성**: 역할 호출 불필요

---

## 개발 역할 정의

### 역할 1: Backend Developer

**호출 방법**: 프롬프트 시작 시 `[Backend Developer 역할]`

**전문 분야**:
- FastAPI 라우팅 및 미들웨어 설계
- Pydantic 데이터 검증
- 비동기 처리 (async/await)
- 외부 API 통합 (Claude API, 웹 스크래핑)
- 에러 처리 및 로깅
- REST API 설계 및 OpenAPI 문서 생성

**준수 사항**:
1. claude.md의 "코드 표준 (Python)" 섹션 준수
2. Think → Implement → Review 워크플로우 적용
3. 프로젝트 구조에 맞는 파일 배치 (`backend/` 디렉토리)
4. 모든 함수에 타입 힌트 및 docstring 작성

**응답 형식**:
```markdown
## Think
[설계 전략 및 고려사항]

## Implement
[코드 구현]

## Review
[엣지 케이스 점검 및 개선 제안]
```

**예시 프롬프트**:
```
[Backend Developer 역할]

backend/scraper.py 구현:
- 조선일보, 중앙일보, 한겨레 스크래핑
- 출력: JSON (title, content, author, published_date, url)
- 에러 처리: 404, timeout, paywall

Think → Implement → Review 단계로 진행
```

---

### 역할 2: Frontend Developer

**호출 방법**: 프롬프트 시작 시 `[Frontend Developer 역할]`

**전문 분야**:
- Next.js 14 App Router
- Server Components vs Client Components 구분
- TailwindCSS 반응형 디자인
- 폼 처리 및 클라이언트 검증
- 상태 관리 (React hooks: useState, useEffect)
- API 연동 (fetch, error handling)

**준수 사항**:
1. claude.md의 "코드 표준 (TypeScript)" 섹션 준수
2. "아키텍처 철학 (마법사 방식 UI)" 참조
3. Think → Implement → Review 워크플로우 적용
4. 접근성 (a11y) 고려
5. 모바일/데스크톱 반응형 디자인

**응답 형식**:
```markdown
## Think
[UI/UX 설계 전략]

## Implement
[컴포넌트 구현]

## Review
[접근성, 반응형, 사용성 검토]
```

**예시 프롬프트**:
```
[Frontend Developer 역할]

app/page.tsx 구현:
- URL 입력 폼
- 유효성 검증 (한국 언론사 URL)
- 로딩 상태 표시
- 에러 메시지 UI

마법사 방식 UI 철학 참조
Think → Implement → Review
```

---

### 역할 3: Code Reviewer

**호출 방법**: 프롬프트 시작 시 `[Code Reviewer 역할]`

**리뷰 체크리스트**:

1. ✅ **코드 표준 준수**
   - Python: PEP 8, 타입 힌트, docstring
   - TypeScript: ESLint, Prettier, strict mode

2. ✅ **엣지 케이스 처리**
   - 빈 값, null, undefined 처리
   - 네트워크 에러 (timeout, 404, 500)
   - 유효하지 않은 입력 검증

3. ✅ **보안 취약점**
   - API 키 하드코딩 여부 (환경변수 사용?)
   - XSS 공격 방어 (사용자 입력 sanitize)
   - SQL 인젝션 (Phase 2 DB 도입 시)
   - CORS 설정 적절성

4. ✅ **성능 최적화**
   - 불필요한 렌더링 (React.memo, useMemo)
   - N+1 쿼리 문제
   - 캐싱 전략

5. ✅ **타입 안정성**
   - Python: 모든 함수에 타입 힌트
   - TypeScript: strict mode, any 타입 최소화

6. ✅ **테스트 가능성**
   - 함수의 단일 책임 원칙
   - 의존성 주입 가능 여부
   - Mock 가능한 구조

**출력 형식**:
```markdown
## 코드 리뷰 결과

### 📛 Critical Issues (즉시 수정 필요)
- [이슈 설명]
  - **파일**: `backend/scraper.py`
  - **라인**: 42-45
  - **문제**: API 키가 하드코딩되어 있음
  - **수정 방안**: 환경변수로 이동 (`os.getenv('ANTHROPIC_API_KEY')`)

### 🔴 High Priority (수정 권장)
- [이슈 설명]

### 🟡 Medium Priority (개선 제안)
- [이슈 설명]

### 🟢 Low Priority (최적화 제안)
- [이슈 설명]

### ✅ 잘된 점
- [긍정적 피드백]
```

**예시 프롬프트**:
```
[Code Reviewer 역할]

다음 파일들을 리뷰:
- backend/scraper.py
- backend/classifier.py
- app/page.tsx

중점 검토:
- 보안 취약점
- 에러 처리 충분성
- 타입 안정성
```

---

## Skills 활용 가이드 (웹 버전)

### Skills란?

**Skills**는 도메인 지식, 참조 문서, 평가 기준 등을 패키징하여 Claude에게 제공하는 기능입니다. 역할(Role)이 "어떻게 일하는가"를 정의한다면, Skills는 "무엇을 알고 있는가"를 정의합니다.

**웹 버전 사용법**:
- 로컬에서 ZIP 파일로 준비
- Claude.ai 웹 설정에서 업로드
- 프롬프트에서 명시적으로 호출

### 역할 vs Skills 비교

| 구분 | 역할 (Role) | Skills |
|------|------------|--------|
| **목적** | 워크플로우, 코드 표준 | 도메인 지식, 참조 데이터 |
| **정의 위치** | claude.md 내부 | 별도 ZIP 파일 |
| **크기** | 작음 (< 100KB) | 클 수 있음 (< 10MB) |
| **업데이트** | Git으로 버전 관리 | 재업로드 필요 |
| **예시** | Backend Developer, Code Reviewer | CR 평가 기준, 언론사 HTML 구조 |

**권장 조합**:
- **역할**: 개발 프로세스, 코드 작성 방법
- **Skills**: 도메인 전문 지식, 참조 문서, 예시 데이터

### 프로젝트에서 사용할 Skills

#### CR 평가 기준 Skill (Week 5 도입)

**이름**: `CR Evaluation Criteria`

**목적**: 한국 언론 기사를 8차원 평가 기준으로 분석하기 위한 체계적 가이드

**포함 내용**:
1. **진실성 (Truth)**: 사실과 의견 구분, 출처 명시
2. **정확성 (Accuracy)**: 통계 정확성, 인용 정확성
3. **공정성 (Fairness)**: 다양한 관점, 균형 잡힌 보도
4. **투명성 (Transparency)**: 출처 공개, 이해관계 명시
5. **맥락 (Context)**: 배경 정보, 역사적 맥락
6. **인권 존중 (Human Rights)**: 취약 집단 보호, 차별 없는 표현
7. **책임성 (Accountability)**: 오류 정정, 피해 구제
8. **독립성 (Independence)**: 외부 압력으로부터 자유

**기사 유형별 중점 차원**:
- 스트레이트 뉴스: 진실성, 정확성, 투명성
- 해설/분석: 공정성, 맥락, 독립성
- 인터뷰: 공정성, 투명성, 인권 존중
- 사설/칼럼: 논리성, 독립성, 책임성

**도입 시점**: Week 5 (템플릿 생성 작업 시작 시)

### Skills 호출 방법

Skills를 사용하려면 **프롬프트에서 명시적으로 언급**해야 합니다.

**기본 호출 패턴**:
```
[역할 이름]

[Skill 이름] Skill을 참조하여 [작업 설명]

요구사항:
- [구체적 요구사항]
- [출력 형식]

Think → Implement → Review
```

**예시 1: 템플릿 생성**
```
[Backend Developer 역할]

CR 평가 기준 Skill을 참조하여
backend/templates/claude-sonnet-4/straight-news.md 파일을 생성해주세요.

요구사항:
- CR 8차원 평가 기준 체크리스트
- 각 차원별 구체적 질문 (5-7개)
- 스트레이트 뉴스에 중점을 둔 차원 강조 (진실성, 정확성, 투명성)
- 평가 방법 가이드
- JSON 출력 형식 예시

Think → Implement → Review
```

**예시 2: 복수 템플릿 생성**
```
CR 평가 기준 Skill을 활용하여
다음 템플릿들을 생성해주세요:

1. backend/templates/claude-sonnet-4/analysis.md
   - 중점 차원: 공정성, 맥락, 독립성

2. backend/templates/chatgpt-4o/straight-news.md
   - 중점 차원: 진실성, 정확성, 투명성

각 템플릿:
- 해당 AI 서비스 특성에 맞는 프롬프트 스타일
- 기사 유형별 중점 차원 강조
```

**예시 3: Skill을 참조하여 코드 검증**
```
[Code Reviewer 역할]

CR 평가 기준 Skill의 8차원을 참조하여
backend/templates/ 디렉토리의 모든 템플릿을 검토해주세요.

확인 사항:
- 8개 차원이 모두 포함되어 있는지
- 기사 유형별 중점 차원이 적절히 강조되었는지
- 각 차원별 체크리스트가 구체적이고 실행 가능한지
```

### Skills 준비 과정 (간략)

**Week 5 이전에 준비**:

1. **로컬에서 Skill 폴더 생성**
   ```
   cr-evaluation-criteria/
   ├── SKILL.md              # 필수: Skill 메타데이터 및 내용
   └── examples/             # 선택: 예시 파일들
       ├── straight-news-example.md
       └── analysis-example.md
   ```

2. **SKILL.md 작성**
   - 메타데이터 (name, description, version, author)
   - CR 8차원 평가 기준 상세 설명
   - 기사 유형별 중점 차원 매핑
   - 활용 예시

3. **ZIP 파일 생성**
   ```bash
   # macOS/Linux
   zip -r cr-evaluation-criteria.zip cr-evaluation-criteria/

   # Windows (PowerShell)
   Compress-Archive -Path cr-evaluation-criteria -DestinationPath cr-evaluation-criteria.zip
   ```

4. **웹에서 업로드**
   - Claude.ai → Settings → Capabilities
   - "Code execution and file creation" 활성화
   - Skills 섹션에서 "Upload custom skill"
   - ZIP 파일 선택 및 업로드
   - 활성화 확인

**중요 사항**:
- ⚠️ **Pro/Max 플랜 필요**: 무료 사용자는 Skills 사용 불가
- ⚠️ **Code Execution 필수**: Skills는 컴퓨터 사용 기능 필요
- ⚠️ **명시적 호출**: 프롬프트에서 Skill 이름 정확히 언급
- ⚠️ **파일 구조**: SKILL.md가 ZIP 파일 루트에 있어야 함

### Skills 문제 해결

**Q: Skill이 적용되지 않는 것 같아요**
```
A: 프롬프트에서 명시적으로 언급하세요:
"CR 평가 기준 Skill의 [섹션명]을 참조하여..."
```

**Q: 여러 Skills를 동시에 사용할 수 있나요?**
```
A: 네, 프롬프트에서 모두 언급하면 됩니다:
"CR 평가 기준 Skill과 언론사 구조 Skill을 활용하여..."
```

**Q: Skill 업데이트는 어떻게 하나요?**
```
A:
1. 기존 Skill 비활성화
2. 기존 Skill 삭제
3. 수정된 ZIP 파일로 재업로드
4. 활성화
```

### Skills와 역할의 조화

**효과적인 조합 예시**:

```
[Backend Developer 역할]  ← 워크플로우 (어떻게 일할 것인가)
+
CR 평가 기준 Skill       ← 도메인 지식 (무엇을 알아야 하는가)
↓
고품질 템플릿 생성
```

**Week 5 템플릿 생성 작업 시**:
1. `[Backend Developer 역할]` 호출 → Think-Implement-Review 워크플로우 적용
2. `CR 평가 기준 Skill` 참조 → 8차원 평가 기준 활용
3. claude.md의 "코드 표준" 준수 → Python/마크다운 스타일 가이드
4. 결과: 일관되고 전문적인 템플릿

---

## 기술 스택

### Backend
- **프레임워크**: FastAPI 0.104+
- **웹 스크래핑**: BeautifulSoup4, requests
- **AI API**: Anthropic Claude (Haiku for classification)
- **언어**: Python 3.10+
- **환경변수**: python-dotenv
- **검증**: Pydantic v2

### Frontend
- **프레임워크**: Next.js 14 (App Router)
- **언어**: TypeScript 5.0+
- **스타일링**: TailwindCSS 3.3+
- **UI 컴포넌트**: Headless UI (필요 시)
- **상태 관리**: React hooks (useState, useEffect)
- **빌드 도구**: Turbopack

### Infrastructure
- **Frontend 배포**: Vercel
- **Backend 배포**: Railway 또는 Render
- **버전 관리**: GitHub
- **CI/CD**: GitHub Actions (Phase 2)
- **피드백 수집**: Google Forms

### Development Tools
- **Claude Code**: 웹 버전 (환경 분리, 자동 PR)
- **린터**: ESLint, Pylint
- **포매터**: Prettier, Black
- **테스트**: pytest (Backend), Jest (Frontend)

---

## 프로젝트 구조

```
cr-template-hub/
├── frontend/                    # Next.js 프론트엔드
│   ├── app/
│   │   ├── page.tsx            # 1단계: URL 입력
│   │   ├── analysis/
│   │   │   └── page.tsx        # 2단계: 분류 결과 확인/수정
│   │   ├── download/
│   │   │   └── page.tsx        # 3단계: 템플릿 다운로드
│   │   ├── layout.tsx          # 공통 레이아웃
│   │   └── globals.css         # 글로벌 스타일
│   ├── components/             # 재사용 컴포넌트
│   │   ├── ArticleTypeSelect.tsx
│   │   ├── LoadingSpinner.tsx
│   │   └── ErrorMessage.tsx
│   ├── lib/                    # 유틸리티 함수
│   │   ├── api.ts              # API 호출 함수
│   │   └── validators.ts       # 검증 함수
│   ├── public/                 # 정적 파일
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.ts
│
├── backend/                     # FastAPI 백엔드
│   ├── main.py                 # FastAPI 앱 엔트리포인트
│   ├── scraper.py              # 기사 스크래핑 모듈
│   ├── classifier.py           # 기사 유형 분류 모듈
│   ├── template_service.py     # 템플릿 매핑 서비스
│   ├── models.py               # Pydantic 모델
│   ├── config.py               # 설정 및 환경변수
│   ├── templates/              # 평가 템플릿 저장소
│   │   ├── claude-sonnet-4/
│   │   │   ├── straight-news.md
│   │   │   ├── analysis.md
│   │   │   ├── interview.md
│   │   │   └── opinion.md
│   │   ├── chatgpt-4o/
│   │   │   └── ...
│   │   └── gemini-pro/
│   │       └── ...
│   ├── requirements.txt
│   └── .env.example            # 환경변수 예시
│
├── data/                        # 정적 데이터
│   └── template_mapping.json   # 기사 유형 → 템플릿 매핑
│
├── tests/                       # 테스트 (Phase 2)
│   ├── backend/
│   └── frontend/
│
├── docs/                        # 문서
│   ├── api.md                  # API 문서
│   └── deployment.md           # 배포 가이드
│
├── claude.md                    # 프로젝트 중심 문서 (이 파일)
├── README.md                    # 프로젝트 소개
├── .gitignore
└── LICENSE
```

---

## 코드 표준

### Python (Backend)

#### 스타일 가이드
- **PEP 8** 준수
- 들여쓰기: 4칸 스페이스
- 최대 줄 길이: 88자 (Black 기본값)
- 네이밍:
  - 함수/변수: `snake_case`
  - 클래스: `PascalCase`
  - 상수: `UPPER_SNAKE_CASE`

#### 타입 힌트 (필수)
```python
from typing import Optional, Dict, Any

def scrape_article(url: str) -> Dict[str, Any]:
    """기사 URL에서 내용을 스크래핑합니다.

    Args:
        url: 기사 URL

    Returns:
        title, content, author 등을 포함한 딕셔너리

    Raises:
        ValueError: URL이 유효하지 않은 경우
        requests.RequestException: 네트워크 에러
    """
    pass
```

#### Docstring (Google Style, 필수)
```python
def classify_article(title: str, content: str) -> Dict[str, Any]:
    """Claude API를 사용하여 기사 유형을 분류합니다.

    Args:
        title: 기사 제목
        content: 기사 본문 (최대 3000자)

    Returns:
        {
            "article_type": "straight_news" | "analysis" | ...,
            "confidence": 0.95,
            "reasoning": "분류 근거"
        }

    Raises:
        anthropic.APIError: Claude API 호출 실패
        ValueError: 입력값이 비어있는 경우
    """
    pass
```

#### 에러 처리
```python
import logging

logger = logging.getLogger(__name__)

try:
    result = scrape_article(url)
except requests.Timeout:
    logger.error(f"Timeout scraping {url}")
    raise HTTPException(status_code=408, detail="Request timeout")
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

#### 환경변수
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    allowed_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
```

---

### TypeScript (Frontend)

#### 스타일 가이드
- **ESLint + Prettier** 사용
- 들여쓰기: 2칸 스페이스
- 세미콜론: 사용
- 따옴표: 작은따옴표 (')
- 네이밍:
  - 변수/함수: `camelCase`
  - 컴포넌트: `PascalCase`
  - 상수: `UPPER_SNAKE_CASE`

#### TypeScript strict mode (필수)
```typescript
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}
```

#### 타입 정의
```typescript
// types/article.ts
export interface Article {
  title: string;
  content: string;
  author: string;
  publishedDate: string;
  url: string;
}

export type ArticleType =
  | 'straight_news'
  | 'analysis'
  | 'interview'
  | 'opinion'
  | 'other';

export interface ClassificationResult {
  articleType: ArticleType;
  confidence: number;
  reasoning: string;
}
```

#### 컴포넌트 스타일
```typescript
'use client'; // Client Component인 경우 명시

import { useState, useEffect } from 'react';

interface Props {
  articleUrl: string;
  onSubmit: (url: string) => void;
}

export default function ArticleUrlForm({ articleUrl, onSubmit }: Props) {
  const [url, setUrl] = useState(articleUrl);
  const [error, setError] = useState<string | null>(null);

  // 함수 로직

  return (
    <form onSubmit={handleSubmit}>
      {/* JSX */}
    </form>
  );
}
```

#### 에러 처리
```typescript
try {
  const response = await fetch('/api/scrape', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = await response.json();
  return data;
} catch (error) {
  console.error('Error scraping article:', error);
  setError(error instanceof Error ? error.message : 'Unknown error');
}
```

---

## 아키텍처 철학

### 마법사 방식 UI (Wizard Flow)

사용자가 단계별로 진행하며 각 단계에서 결과를 확인하고 수정할 수 있는 방식:

**1단계: URL 입력** (`app/page.tsx`)
- 기사 URL 입력 폼
- 유효성 검증 (한국 주요 언론사만)
- "분석 시작" 버튼
- → 스크래핑 실행 → 2단계로 이동

**2단계: 분류 결과** (`app/analysis/page.tsx`)
- AI 분류 결과 표시
- 사용자가 결과 수정 가능 (드롭다운)
- AI 서비스 선택 (Claude Sonnet 4, ChatGPT-4o, Gemini Pro)
- "템플릿 받기" 버튼
- → 3단계로 이동

**3단계: 다운로드** (`app/download/page.tsx`)
- 템플릿 미리보기
- 다운로드 버튼 (.md, .txt)
- 클립보드 복사 버튼
- Google Forms 피드백 링크
- "처음부터 다시" 버튼

**진행 상태 표시**:
```
[1. URL 입력] → [2. 분류 확인] → [3. 다운로드]
   완료            현재 단계          대기 중
```

### API 설계 원칙

#### RESTful 설계
```
POST   /api/scrape              # 기사 스크래핑
POST   /api/classify            # 기사 분류
GET    /api/templates/{type}/{ai}  # 템플릿 조회
GET    /api/health              # 헬스 체크
```

#### HTTP 상태 코드
- `200`: 성공
- `400`: 잘못된 요청 (유효하지 않은 URL, 빈 값)
- `404`: 리소스 없음 (기사 없음, 템플릿 없음)
- `408`: 요청 타임아웃
- `500`: 서버 내부 오류

#### 에러 응답 형식
```json
{
  "error": {
    "code": "INVALID_URL",
    "message": "유효하지 않은 URL 형식입니다",
    "details": "URL은 http:// 또는 https://로 시작해야 합니다"
  }
}
```

#### 성공 응답 형식
```json
{
  "success": true,
  "data": {
    "title": "기사 제목",
    "content": "본문 내용...",
    "metadata": { ... }
  }
}
```

---

## 환경 관리 전략 (웹 버전)

### 환경 분리

**1. cr-dev (기본 개발 환경)**
- 용도: 일반적인 개발 작업
- 설정: Python, Node.js 기본 설치
- 사용 시점: 초기 프로토타이핑, 실험

**2. backend-dev (백엔드 전용)**
- 용도: API 개발 집중
- 설정: FastAPI, BeautifulSoup4, Anthropic SDK 설치
- 사용 시점: Week 1-2 (스크래핑, 분류 모듈)

**3. frontend-dev (프론트엔드 전용)**
- 용도: UI 개발 집중
- 설정: Next.js, TailwindCSS 설치
- 사용 시점: Week 3 (페이지 구현)

**4. testing (테스트 환경)**
- 용도: 통합 테스트
- 설정: pytest, Jest, Mock 데이터
- 사용 시점: Week 5-6 (전체 플로우 검증)

**5. pre-production (배포 준비)**
- 용도: 최종 검증
- 설정: 프로덕션 설정 적용
- 사용 시점: Week 6 (배포 전)

### 환경 전환 시나리오

**시나리오 1: 백엔드 개발 → 프론트엔드 개발**
```
1. backend-dev 환경에서 API 개발
2. PR 생성: feature/api-scraper
3. frontend-dev 환경으로 전환
4. API 연동 UI 개발
5. PR 생성: feature/ui-scraper
```

**시나리오 2: 병렬 개발**
```
탭 1: backend-dev 환경
- 템플릿 서비스 구현

탭 2: frontend-dev 환경
- 다운로드 페이지 구현

→ 두 작업 독립적으로 진행 후 각각 PR 생성
```

---

## PR 생성 가이드 (웹 버전)

### 브랜치 명명 규칙

```
feature/[기능명]       # 새 기능
fix/[버그명]          # 버그 수정
refactor/[개선명]     # 리팩토링
docs/[문서명]         # 문서화
test/[테스트명]       # 테스트 추가
```

**예시:**
- `feature/article-scraper`
- `feature/classification-api`
- `fix/timeout-handling`
- `refactor/error-messages`
- `docs/api-documentation`

### PR 제목 형식

```
[타입] 간단한 설명 (50자 이내)
```

**예시:**
- `[Feature] Add article classification API`
- `[Fix] Handle timeout in scraper`
- `[Refactor] Improve error handling in API endpoints`
- `[Docs] Add API documentation`

### PR 설명 구조

```markdown
## 변경 사항 (Changes)
- 주요 변경 내용을 bullet point로 나열
- 새로 추가된 파일/기능
- 수정된 기능

## 테스트 (Testing)
- 수동 테스트 방법
- 테스트한 시나리오
- 예상 결과

## 스크린샷 (Screenshots)
- UI 변경 시 스크린샷 첨부
- Before/After 비교

## 체크리스트 (Checklist)
- [ ] 코드 표준 준수 (claude.md 참조)
- [ ] 테스트 추가/통과
- [ ] 문서 업데이트 (필요시)
- [ ] Breaking changes 없음
- [ ] 환경변수 변경사항 문서화 (필요시)
```

### 자동 PR 생성 워크플로우

1. 코드 작성 완료
2. 화면 하단 브랜치 이름 필드 확인/수정
3. "PR 생성" 버튼 클릭
4. GitHub에서 자동으로:
   - ✅ 브랜치 생성
   - ✅ 변경사항 커밋
   - ✅ PR 생성
   - ✅ PR 제목/설명 작성

---

## 의사결정 로그

### 2025-11-14: 웹 버전 Claude Code 선택

**결정**: 웹 버전 사용

**이유**:
1. **자동 PR 생성**: Git 명령어 없이 클릭 한 번으로 PR 생성
2. **환경 분리**: UI로 쉽게 여러 환경 관리 (backend-dev, frontend-dev 등)
3. **클라우드 VM**: 팀원 간 일관된 개발 환경, 설정 불필요
4. **모바일 접근**: iOS 앱으로 이동 중에도 코드 리뷰/수정 가능
5. **GitHub 통합**: 저장소 연결 및 자동 동기화

**트레이드오프**:
- 로컬 서버 접근 제한 → Vercel Preview로 해결
- MCP 서버 미지원 → Phase 1에서는 불필요

---

### 2025-11-14: SubAgent vs 역할 정의

**결정**: claude.md에 역할 통합 (SubAgent 방식 대신)

**이유**:
1. **웹 버전 호환성**: `.claude/agents/` 파일 방식이 웹에서 불확실
2. **유지보수 용이**: 한 파일(claude.md)만 관리
3. **명시적 제어**: 프롬프트에서 역할을 명시적으로 호출
4. **유연성**: 역할 조합 및 커스터마이징 자유로움

**역할 구조**:
- Backend Developer: API 개발 전문
- Frontend Developer: UI 개발 전문
- Code Reviewer: 품질 검증 전문

---

### 2025-11-14: Claude Haiku for Classification

**결정**: 기사 분류에 Claude Haiku 사용

**이유**:
1. **비용 효율**: Sonnet 대비 20배 저렴
2. **속도**: 10배 빠른 응답 시간
3. **충분한 성능**: 5개 카테고리 분류는 단순 작업
4. **목표 달성**: 70% 정확도로 충분 (MVP)

**카테고리**:
- straight_news (스트레이트 뉴스)
- analysis (해설/분석)
- interview (인터뷰)
- opinion (사설/칼럼)
- other (기타)

---

### 2025-11-14: Phase 1에서 DB 미사용

**결정**: JSON 파일로 템플릿 매핑 관리

**이유**:
1. **단순성**: MVP에서는 정적 데이터만 필요
2. **빠른 개발**: DB 설정/관리 오버헤드 회피
3. **버전 관리**: Git으로 템플릿 변경 추적 가능

**데이터 구조** (`data/template_mapping.json`):
```json
{
  "straight_news": {
    "claude-sonnet-4": "templates/claude-sonnet-4/straight-news.md",
    "chatgpt-4o": "templates/chatgpt-4o/straight-news.md",
    "gemini-pro": "templates/gemini-pro/straight-news.md"
  },
  ...
}
```

**Phase 2 계획**: 사용자 피드백 저장 시 PostgreSQL 도입

---

### 2025-11-14: 마법사 방식 UI

**결정**: 단계별 진행 (Wizard Flow) 방식 채택

**이유**:
1. **학습 곡선 낮음**: 한 번에 한 가지 작업만 집중
2. **검증 가능**: 각 단계에서 결과 확인 및 수정 가능
3. **오류 감소**: 단계별 검증으로 잘못된 입력 방지
4. **사용자 제어**: 자동 분류 결과를 수정할 수 있는 자유

**단계**:
1. URL 입력 → 2. 분류 확인 → 3. 템플릿 다운로드

---

### 2025-11-14: Vercel + Railway 배포

**결정**: Frontend(Vercel) + Backend(Railway) 분리 배포

**이유**:
1. **Frontend (Vercel)**:
   - Next.js 최적화
   - 자동 빌드 및 배포
   - Edge Functions 지원
   - 무료 플랜으로 충분

2. **Backend (Railway)**:
   - Python 지원
   - 환경변수 관리 용이
   - GitHub 연동 자동 배포
   - 합리적인 가격

**대안 고려**:
- Render: Railway와 유사하지만 콜드 스타트 이슈
- Heroku: 무료 플랜 종료

---

## 환경변수 관리

### Backend (.env)

```bash
# Claude API
ANTHROPIC_API_KEY=sk-ant-xxxxx

# CORS 설정
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app

# 로깅
LOG_LEVEL=INFO

# 타임아웃 (초)
SCRAPING_TIMEOUT=10
API_TIMEOUT=30
```

### Frontend (.env.local)

```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Google Analytics (선택)
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX

# Google Forms 피드백 URL
NEXT_PUBLIC_FEEDBACK_URL=https://forms.gle/xxxxx
```

---

## Phase 1 (MVP) 범위

### ✅ 포함 기능

1. **기사 스크래핑**
   - 조선일보, 중앙일보, 한겨레
   - 제목, 본문, 저자, 날짜, URL 추출

2. **기사 분류**
   - Claude Haiku API 사용
   - 5개 카테고리 분류
   - 신뢰도 점수 제공

3. **템플릿 제공**
   - 3개 AI 서비스 (Claude, ChatGPT, Gemini)
   - 5개 기사 유형
   - 다운로드 (.md, .txt)
   - 클립보드 복사

4. **마법사 UI**
   - 3단계 워크플로우
   - 반응형 디자인
   - 기본 에러 처리

5. **피드백 수집**
   - Google Forms 연동

### ❌ Phase 2로 연기

1. 데이터베이스 (PostgreSQL)
2. 사용자 인증/로그인
3. 평가 이력 저장
4. 언론사 확장 (10개 이상)
5. 고급 분석 (감정 분석, 편향 탐지)
6. 관리자 대시보드
7. API Rate Limiting
8. 단위 테스트 (80% 커버리지)

---

## 다음 단계

### Week 1 Day 4-5: 스크래핑 모듈 구현

```
[Backend Developer 역할]

backend/scraper.py 구현:

요구사항:
- 조선일보, 중앙일보, 한겨레 스크래핑
- 출력: JSON (title, content, author, published_date, url)
- 에러 처리: 404, timeout, paywall
- 타입 힌트 및 docstring 필수

Think → Implement → Review
```

### Week 1 완료 후 체크리스트

- [ ] claude.md 작성 완료
- [ ] backend/scraper.py 구현 및 테스트
- [ ] Think→Implement→Review 워크플로우 익힘
- [ ] 웹 버전 자동 PR 생성 경험
- [ ] 3개 언론사 스크래핑 성공 (수동 테스트)

---

**문서 버전**: 1.1
**최종 수정일**: 2025-11-14
**관리**: 이 문서는 프로젝트의 모든 개발 활동의 기준입니다. 주요 의사결정이나 변경사항이 있을 때마다 업데이트합니다.

**변경 이력**:
- v1.1 (2025-11-14): Skills 활용 가이드 섹션 추가 (친구 K 피드백 반영)
- v1.0 (2025-11-14): 초기 버전 작성
