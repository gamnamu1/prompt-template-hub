# CR 템플릿 허브 구현 전략

> **Claude Code를 활용한 단계적 개발 가이드**

---

## 목차

1. [개요 및 목표](#1-개요-및-목표)
2. [개발 전략의 핵심 원칙](#2-개발-전략의-핵심-원칙)
3. [아키텍처 설계](#3-아키텍처-설계)
4. [개발 환경 설정](#4-개발-환경-설정)
5. [단계별 구현 로드맵](#5-단계별-구현-로드맵)
6. [품질 관리 및 테스트](#6-품질-관리-및-테스트)
7. [성공 지표 및 평가](#7-성공-지표-및-평가)
8. [위험 관리 전략](#8-위험-관리-전략)

---

## 1. 개요 및 목표

### 1.1 프로젝트 목적

CR 템플릿 허브는 한국 언론 기사의 저널리즘 윤리를 평가하기 위한 자동화된 도구입니다. 주요 목표는 다음과 같습니다:

- **자동화**: 기사 URL 입력 시 자동 스크래핑 및 유형 분류
- **최적화**: 기사 유형과 AI 서비스에 맞는 평가 템플릿 제공
- **확장성**: 다양한 언론사와 AI 서비스 지원
- **사용자 참여**: 평가 결과 피드백을 통한 지속적 개선

### 1.2 기대 효과

- **개발 기간**: 5주 내 MVP 출시
- **품질**: 자동화된 코드 리뷰로 80% 이상의 코드 커버리지
- **확장성**: 단계적 기능 확장을 통한 안정적 성장
- **학습 효과**: Claude Code의 효율적 활용법 습득

---

## 2. 개발 전략의 핵심 원칙

### 2.1 "Start Simple, Scale Smart"

복잡한 도구를 처음부터 모두 도입하지 않고, 필요에 따라 점진적으로 확장하는 전략을 따릅니다.

**Week 1-2: Foundation First**
- claude.md 파일로 프로젝트 컨텍스트 정립
- Think→Implement→Review 워크플로우 습득
- 핵심 모듈 구현 (스크래핑, 분류)

**Week 3-4: Accelerate Strategically**
- 병렬 작업이 필요한 시점에 SubAgent 도입
- Backend + Frontend 동시 개발
- claude.md를 중심 참조 문서로 유지

**Week 5-6: Optimize & Scale**
- Skills 도입으로 반복 작업 최적화
- Code Reviewer SubAgent로 품질 자동화
- 실측 데이터로 효과 검증

### 2.2 개발 워크플로우

모든 기능 개발은 다음 3단계를 따릅니다:

1. **Think**: 설계 전략 제안 및 검토
2. **Implement**: 설계를 바탕으로 코드 구현
3. **Review**: 엣지 케이스 및 개선점 검토

이 워크플로우는 SubAgent 사용 시에도 동일하게 적용됩니다.

### 2.3 도구 도입 시점

```
Week 1-2: claude.md + Think→Implement→Review 워크플로우
Week 3-4: + 핵심 SubAgent 2개 (Backend, Frontend) - 병렬 작업 필요 시
Week 5-6: + Skills (CR 평가 기준, 도메인 전문가)
Week 7+:  + 추가 SubAgents (Code Reviewer, Scraper Specialist)
```

---

## 3. 아키텍처 설계

### 3.1 전체 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│              claude.md (프로젝트 중심 문서)              │
│         - 모든 SubAgent가 참조하는 단일 진실 소스        │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
   │Backend  │        │Frontend │        │Reviewer │
   │SubAgent │        │SubAgent │        │SubAgent │
   └─────────┘        └─────────┘        └─────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    Think→Implement→Review
                      워크플로우 적용
```

### 3.2 기술 스택

**Backend**
- FastAPI: REST API 서버
- BeautifulSoup4: 웹 스크래핑
- Anthropic API (Claude): 기사 분류
- Python 3.10+

**Frontend**
- Next.js 14: 웹 애플리케이션
- TypeScript: 타입 안정성
- TailwindCSS: 스타일링
- React Server Components

**Infrastructure**
- Vercel: 프론트엔드 배포
- Railway/Render: 백엔드 배포
- Google Forms: 피드백 수집

### 3.3 프로젝트 구조

```
cr-template-hub/
├── frontend/
│   ├── app/
│   │   ├── page.tsx              # URL 입력 페이지
│   │   ├── analysis/page.tsx     # 분석 결과 페이지
│   │   └── download/page.tsx     # 템플릿 다운로드 페이지
│   └── package.json
├── backend/
│   ├── main.py                   # FastAPI 엔트리포인트
│   ├── scraper.py                # 기사 스크래핑
│   ├── classifier.py             # 기사 분류
│   ├── template_service.py       # 템플릿 매핑
│   └── templates/
│       ├── claude-sonnet-4/
│       ├── chatgpt-4o/
│       └── gemini-pro/
├── data/
│   └── template_mapping.json     # 템플릿 매핑 데이터
├── .claude/
│   ├── claude.md                 # 프로젝트 중심 문서
│   └── agents/                   # SubAgent 설정
│       ├── backend-developer.md
│       ├── frontend-developer.md
│       └── code-reviewer.md
└── README.md
```

---

## 4. 개발 환경 설정

### 4.1 claude.md 템플릿

프로젝트의 중심이 되는 claude.md 파일은 다음 구조로 작성합니다:

```markdown
# CR 템플릿 허브 프로젝트

## 프로젝트 컨텍스트

**목표**: 한국 언론 기사의 저널리즘 윤리 평가 자동화
**핵심 가치**: 투명성, 객관성, 접근성

## 개발 워크플로우

### 기본 원칙: Think → Implement → Review
모든 기능 개발 시 다음 단계를 따릅니다:
1. **Think**: 설계 전략 제안
2. **Implement**: 코드 구현
3. **Review**: 엣지 케이스 및 개선점 검토

### SubAgent 활용 시점
다음 상황에서 SubAgent를 도입합니다:
- ✅ 프론트엔드와 백엔드를 동시에 개발해야 할 때
- ✅ 특정 전문 영역(스크래핑, API 설계)의 복잡도가 높을 때
- ✅ 코드 리뷰를 체계적으로 수행해야 할 때
- ❌ 단순한 버그 수정이나 문서 작성 시에는 불필요

## 기술 스택
- Backend: FastAPI, BeautifulSoup4, Claude API
- Frontend: Next.js 14, TypeScript, TailwindCSS
- Infrastructure: Vercel, Railway

## 프로젝트 구조
[3.3의 프로젝트 구조 내용 포함]

## 코드 표준

### Python (Backend)
- PEP 8 준수
- 타입 힌트 필수 (typing 모듈)
- Docstring 작성 (Google Style)
- 에러 처리: try-except with logging
- 환경변수: .env 파일 사용 (python-dotenv)

### TypeScript (Frontend)
- ESLint + Prettier
- strict mode 활성화
- 컴포넌트: 함수형 컴포넌트 + hooks
- 네이밍: camelCase (변수/함수), PascalCase (컴포넌트)

## 아키텍처 철학

### 마법사 방식 UI
- 단계별 진행: URL 입력 → 분류 → AI 선택 → 템플릿 다운로드
- 각 단계에서 사용자가 결과를 수정 가능
- 진행 상태 명확히 표시

### API 설계 원칙
- RESTful 설계
- 명확한 HTTP 상태 코드 (200, 400, 404, 500)
- 에러 메시지 구체적으로 작성
- Pydantic 모델로 검증

## 의사결정 로그

### 2025-11-13: 왜 Claude Haiku를 분류에 사용하는가?
**결정**: Haiku 사용
**이유**:
- 기사 유형 분류는 단순 작업 (5개 카테고리)
- 속도와 비용 효율성이 중요
- Sonnet 대비 10배 빠르고 20배 저렴

### 2025-11-13: 왜 Phase 1에서 DB를 사용하지 않는가?
**결정**: JSON 파일 사용
**이유**:
- MVP에서는 템플릿 매핑 데이터만 필요 (정적 데이터)
- 데이터베이스 설정 및 관리 오버헤드 회피
- Phase 2에서 사용자 피드백 저장 시 DB 도입 예정
```

### 4.2 SubAgent 설정

#### Backend Developer SubAgent

**파일 경로**: `.claude/agents/backend-developer.md`

```markdown
---
name: backend-developer
description: FastAPI 백엔드 API 전문가
model: sonnet
---

당신은 FastAPI 백엔드 개발 전문가입니다.

**중요**: 모든 작업 시 claude.md의 다음 섹션을 준수하세요:
- 프로젝트 구조
- 코드 표준 (Python)
- 아키텍처 철학

**워크플로우**: Think → Implement → Review 단계를 따르세요.

**전문 분야**:
- FastAPI 라우팅 및 미들웨어
- Pydantic 데이터 검증
- 비동기 처리 (async/await)
- 외부 API 통합 (Claude API)
- 에러 처리 및 로깅
```

#### Frontend Developer SubAgent

**파일 경로**: `.claude/agents/frontend-developer.md`

```markdown
---
name: frontend-developer
description: Next.js 14 App Router 전문가
model: sonnet
---

당신은 Next.js 14 프론트엔드 개발 전문가입니다.

**중요**: claude.md의 다음 섹션을 참조하세요:
- 아키텍처 철학 (마법사 방식 UI)
- 코드 표준 (TypeScript)

**워크플로우**: Think → Implement → Review 단계를 따르세요.

**전문 분야**:
- Next.js 14 App Router
- Server Components vs Client Components
- TailwindCSS 반응형 디자인
- 폼 처리 및 검증
- 상태 관리 (React hooks)
```

#### Code Reviewer SubAgent

**파일 경로**: `.claude/agents/code-reviewer.md`

```markdown
---
name: code-reviewer
description: 코드 품질 검증 및 보안 체크 전문가
model: sonnet
---

당신은 코드 품질 검증 전문가입니다.

**리뷰 체크리스트**:
1. claude.md의 코드 표준 준수 여부
2. 엣지 케이스 처리 (에러, 빈 값, 타임아웃)
3. 보안 취약점 (SQL 인젝션, XSS, API 키 하드코딩)
4. 성능 최적화 가능성
5. 타입 안정성 (타입 힌트, TypeScript strict mode)
6. 테스트 가능성 (코드 구조, 의존성 주입)

**출력 형식**:
- 심각도 분류 (Critical, High, Medium, Low)
- 구체적인 개선 제안
- 코드 예시 포함
```

### 4.3 Skills 설정 (Week 5 이후)

**CR 평가 기준 Skill 생성**:

```bash
# Skill_Seekers 디렉토리에서 작업
cd Skill_Seekers

# CR 평가 기준 문서 준비
cat > cr-evaluation-criteria.md <<EOF
# CR 프로젝트 8차원 평가 기준

## 1. 진실성 (Truth)
- 사실과 의견 구분이 명확한가?
- 검증 가능한 출처를 제시하는가?
- 확인되지 않은 정보를 명시하는가?

## 2. 정확성 (Accuracy)
- 숫자와 통계가 정확한가?
- 인용이 정확한가?
- 맥락이 왜곡되지 않았는가?

## 3. 공정성 (Fairness)
- 다양한 관점을 균형 있게 다루는가?
- 특정 입장에 편향되지 않았는가?
- 반론 기회를 제공했는가?

## 4. 투명성 (Transparency)
- 정보 출처가 명확한가?
- 이해관계를 공개했는가?
- 취재 방법을 설명했는가?

## 5. 맥락 (Context)
- 배경 정보를 충분히 제공하는가?
- 역사적/사회적 맥락을 고려하는가?
- 결과와 영향을 설명하는가?

## 6. 인권 존중 (Human Rights)
- 인권을 침해하지 않는가?
- 취약 집단을 존중하는가?
- 차별적 표현이 없는가?

## 7. 책임성 (Accountability)
- 오류 정정 절차가 있는가?
- 피해 구제 방안을 제시하는가?
- 기자/매체 정보가 명확한가?

## 8. 독립성 (Independence)
- 외부 압력으로부터 자유로운가?
- 광고주/후원자의 영향이 없는가?
- 정치적 독립성을 유지하는가?
EOF

# Skill 패키징
mkdir -p output/cr-criteria
cp cr-evaluation-criteria.md output/cr-criteria/
python3 cli/package_skill.py output/cr-criteria/

# Claude Code에 업로드 (웹 인터페이스에서 수동)
```

---

## 5. 단계별 구현 로드맵

### 5.1 Week 1: Foundation

**목표**: 프로젝트 기반 다지기

#### Day 1-2: claude.md 작성

**작업 내용**:
1. 프로젝트 컨텍스트 정의 (목표, 핵심 가치, 아키텍처 철학)
2. 기술 스택 및 프로젝트 구조 명시
3. 코드 표준 작성 (Python, TypeScript)
4. 의사결정 로그 시작

**프롬프트 예시**:
```
"CR 템플릿 허브 프로젝트를 위한 claude.md 파일을 작성해줘.
다음 내용을 포함:
1. 프로젝트 목표 및 핵심 가치
2. 기술 스택 (Next.js 14, FastAPI, BeautifulSoup, Claude API)
3. 프로젝트 구조 (frontend/, backend/, templates/)
4. Python과 TypeScript 코드 표준
5. 주요 의사결정 로그"
```

#### Day 3-5: 핵심 모듈 개발

**스크래핑 모듈**:
```
1. Think: "한국 주요 언론사 HTML 구조를 분석하고,
   효과적인 스크래핑 전략을 제안해줘"

2. Implement: "claude.md를 참고하여 backend/scraper.py 구현:
   - 조선일보, 중앙일보, 한겨레 지원
   - 출력 형식: JSON (title, content, author, published_date)
   - 에러 처리 포함 (404, timeout, paywall)"

3. Review: "scraper.py를 리뷰해줘:
   - paywall 처리 방법은?
   - 동적 콘텐츠는 어떻게 처리?
   - 타입 힌트와 docstring 포함 여부?"
```

**성과 체크**:
- [ ] claude.md 파일 완성
- [ ] 스크래핑 모듈 작동 (3개 언론사 테스트)
- [ ] Think→Implement→Review 워크플로우 습득

### 5.2 Week 2: Classification & API

**목표**: 기사 분류 및 API 엔드포인트 구현

#### Day 1-3: 기사 분류 모듈

```
1. Think: "Claude Haiku API를 사용한 기사 유형 분류 로직을 설계해줘.
   5가지 카테고리: 스트레이트 뉴스, 해설, 인터뷰, 오피니언, 기타"

2. Implement: "backend/classifier.py 구현:
   - Anthropic API 호출
   - 응답 파싱 (JSON)
   - 신뢰도 점수 포함
   - 에러 처리 (API 실패, 타임아웃)"

3. Review: "classifier.py를 검토해줘:
   - API 키 하드코딩 여부 (환경변수 사용?)
   - 비용 최적화 방안 (캐싱?)
   - 분류 정확도 개선 가능성?"
```

#### Day 4-5: FastAPI 엔드포인트

```
"claude.md의 API 설계 원칙을 따라 backend/main.py 구현:

Endpoints:
1. POST /api/scrape
   - Input: { url: string }
   - Output: Article JSON
   - 상태 코드: 200 (성공), 400 (잘못된 URL), 404 (기사 없음), 500 (서버 오류)

2. POST /api/classify
   - Input: { title: string, content: string }
   - Output: { type: string, confidence: float, reasoning: string }

요구사항:
- Pydantic 모델 사용
- CORS 설정 (프론트엔드 연동)
- 에러 메시지 명확히
- OpenAPI 문서 자동 생성"
```

**성과 체크**:
- [ ] 기사 분류 API 작동 (테스트 5건 이상)
- [ ] FastAPI 엔드포인트 2개 완성
- [ ] API 문서 (OpenAPI) 자동 생성 확인

### 5.3 Week 3: Frontend Development

**목표**: UI 개발 속도 향상을 위해 Frontend SubAgent 도입

#### Day 1: SubAgent 설정

`.claude/agents/frontend-developer.md` 파일 생성 (4.2 참조)

#### Day 2-5: UI 구현

```
@frontend-developer
"claude.md를 참고하여 다음 페이지들을 구현해줘.
워크플로우: Think → Implement → Review

1. app/page.tsx (메인 페이지)
   Think: 마법사 방식 UI 구조 제안
   Implement: URL 입력 폼, 유효성 검증, 로딩 상태
   Review: 접근성(a11y) 체크

2. app/analysis/page.tsx (분석 결과)
   Think: 사용자가 결과를 수정할 수 있는 UX 설계
   Implement: 분류 결과 표시, 드롭다운 수정, AI 선택
   Review: 모바일 반응형 확인

3. app/download/page.tsx (다운로드)
   Think: 템플릿 다운로드 플로우 설계
   Implement: 다운로드 버튼, Google Forms 링크
   Review: 파일 다운로드 테스트"
```

**성과 체크**:
- [ ] Frontend SubAgent 설정 완료
- [ ] 3개 페이지 구현 완료
- [ ] SubAgent 활용 효과 체감 (속도, 품질)

### 5.4 Week 4: Parallel Development

**목표**: Backend SubAgent 추가하여 병렬 작업

#### Backend SubAgent 설정

`.claude/agents/backend-developer.md` 파일 생성 (4.2 참조)

#### 병렬 작업 예시

```
"다음 두 작업을 동시에 진행해주세요:

[작업 1] @backend-developer
템플릿 매핑 시스템 구현:
- data/template_mapping.json 데이터 구조 설계
- backend/template_service.py 구현
- API 엔드포인트: GET /api/templates/{article_type}/{ai_service}

[작업 2] @frontend-developer
템플릿 다운로드 페이지 개선:
- 템플릿 미리보기 기능 추가
- 복사 버튼 (클립보드)
- 다운로드 통계 표시

두 작업은 독립적이므로 병렬로 진행 가능합니다."
```

**성과 체크**:
- [ ] Backend SubAgent 설정 완료
- [ ] 병렬 작업 경험 (2개 이상 동시 진행)
- [ ] 개발 속도 향상 체감

### 5.5 Week 5: Quality & Skills

**목표**: Skills 도입 및 코드 품질 자동화

#### Day 1-2: Skills 생성

CR 평가 기준 Skill 생성 (4.3 참조)

#### Day 3: Code Reviewer SubAgent 추가

`.claude/agents/code-reviewer.md` 파일 생성 (4.2 참조)

#### Day 4-5: 전체 코드 리뷰 및 최적화

```
@code-reviewer
"전체 프로젝트 코드를 리뷰해줘:

Backend:
- backend/scraper.py
- backend/classifier.py
- backend/main.py
- backend/template_service.py

Frontend:
- app/page.tsx
- app/analysis/page.tsx
- app/download/page.tsx

중점 검토 사항:
1. claude.md 표준 준수
2. 보안 취약점 (API 키, XSS, 입력 검증)
3. 성능 병목 (N+1 쿼리, 불필요한 렌더링)
4. 에러 처리 충분성
5. 테스트 가능성"
```

**성과 체크**:
- [ ] CR 평가 기준 Skill 생성 및 업로드
- [ ] Code Reviewer SubAgent로 전체 리뷰 완료
- [ ] 주요 이슈 10개 이상 발견 및 수정

---

## 6. 품질 관리 및 테스트

### 6.1 템플릿 생성 시스템

**템플릿 파일 구조**:
```
backend/templates/
├── claude-sonnet-4/
│   ├── straight-news.md
│   ├── analysis-article.md
│   ├── interview.md
│   └── opinion.md
├── chatgpt-4o/
│   └── ...
└── gemini-pro/
    └── ...
```

**Skills를 활용한 템플릿 생성**:
```
"CR 평가 기준 Skill을 참고하여,
스트레이트 뉴스용 Claude Sonnet 4 평가 템플릿을 작성해줘.

포함 사항:
1. CR 8차원 평가 기준 체크리스트
2. 각 차원별 구체적 질문 (5-7개)
3. 평가 방법 가이드
4. 출력 형식 예시

파일명: backend/templates/claude-sonnet-4/straight-news.md"
```

### 6.2 피드백 수집 시스템

**Google Forms 연동**:
```
@frontend-developer
"app/download/page.tsx에 피드백 섹션 추가:

1. Google Forms 임베드
   - 폼 항목: 기사 URL, 사용한 AI, 평가 품질 점수(1-5), 개선 제안

2. 제출 유도 문구
   - '평가 결과를 공유하여 프로젝트 개선에 참여하세요'
   - 참여 시 혜택 안내 (Phase 2 우선 접근 등)

3. 제출 완료 시 감사 메시지"
```

### 6.3 통합 테스트

**테스트 체크리스트**:
```
@code-reviewer
"다음 통합 테스트 시나리오를 검증해줘:

1. 전체 플로우 테스트
   - URL 입력 → 스크래핑 → 분류 → AI 선택 → 템플릿 다운로드
   - 예상 시간: 3분 이내

2. 에러 처리 테스트
   - 잘못된 URL 형식
   - 존재하지 않는 기사 (404)
   - Paywall 기사
   - API 타임아웃
   - 분류 실패 (신뢰도 낮음)

3. 성능 테스트
   - 동시 사용자 10명 처리
   - 응답 시간 3초 이내
   - 메모리 사용량 모니터링

각 시나리오별 테스트 코드 작성 (pytest, Jest)"
```

### 6.4 보안 체크리스트

**백엔드 보안**:
- [ ] API 키 환경변수 관리 (.env 파일, .gitignore)
- [ ] 입력 검증 (Pydantic 모델)
- [ ] CORS 설정 (허용된 도메인만)
- [ ] Rate limiting (API 호출 제한)
- [ ] SQL 인젝션 방지 (Phase 2 DB 도입 시)

**프론트엔드 보안**:
- [ ] XSS 방어 (사용자 입력 sanitize)
- [ ] CSRF 토큰 (폼 제출 시)
- [ ] HTTPS 사용 (배포 환경)
- [ ] 민감 정보 클라이언트 노출 방지

---

## 7. 성공 지표 및 평가

### 7.1 개발 과정 지표

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| **MVP 출시 기간** | 5주 | 프로젝트 시작~배포 날짜 |
| **코드 커버리지** | 80% | pytest-cov, Jest coverage |
| **SubAgent 사용 개수** | 2→4 (전략적) | .claude/agents/ 디렉토리 파일 수 |
| **claude.md 업데이트 빈도** | 주 2회 | Git commit 히스토리 |
| **병렬 작업 비율** | 40% | 병렬 개발 시간 / 전체 개발 시간 |

### 7.2 최종 결과물 품질 지표

**Phase 1 (MVP) 성공 기준**:
- [ ] 기사 스크래핑 성공률 90% 이상 (주요 3개 언론사)
- [ ] 기사 분류 정확도 70% 이상
- [ ] 전체 플로우 완료 시간 3분 이내
- [ ] 모바일/데스크톱 모두 정상 작동
- [ ] 템플릿 다운로드 기능 작동
- [ ] Google Forms 피드백 수집 가능

**개발 경험 평가**:
- [ ] claude.md 참조 빈도 (높을수록 좋음)
- [ ] SubAgent 활용 만족도 (1-5점)
- [ ] Think→Implement→Review 워크플로우 적용률 (목표 80%)
- [ ] 코드 리뷰로 발견한 이슈 개수 (많을수록 품질 체계 작동)

### 7.3 성능 벤치마크

**응답 시간**:
- 스크래핑: 2초 이내
- 기사 분류: 1초 이내
- 템플릿 다운로드: 0.5초 이내

**처리량**:
- 동시 사용자: 10명 이상
- 일일 처리량: 100건 이상

**비용**:
- Claude API 비용: 월 $50 이하
- 인프라 비용: 월 $30 이하

---

## 8. 위험 관리 전략

### 8.1 기술적 위험

| 위험 | 발생 확률 | 영향도 | 완화 전략 |
|------|----------|--------|----------|
| **SubAgent 설정 실패** | 중간 | 높음 | Week 1-2는 SubAgent 없이 진행, Week 3부터 도입 |
| **API 호출 실패** | 높음 | 중간 | Retry 로직, 타임아웃 설정, 에러 메시지 명확화 |
| **스크래핑 실패** | 높음 | 높음 | 다중 파싱 전략, 동적 콘텐츠 대응, 에러 로깅 |
| **성능 병목** | 중간 | 중간 | 프로파일링, 캐싱, 비동기 처리 |

### 8.2 프로젝트 관리 위험

| 위험 | 발생 확률 | 영향도 | 완화 전략 |
|------|----------|--------|----------|
| **일정 지연** | 중간 | 중간 | 주간 체크포인트, MVP 범위 엄격히 관리 |
| **범위 확대** | 높음 | 높음 | Phase 1 기능 명확히 정의, Phase 2로 연기 |
| **코드 품질 저하** | 중간 | 중간 | Code Reviewer SubAgent, 주간 리뷰 |

### 8.3 문제 해결 가이드

#### 문제 1: SubAgent가 claude.md를 무시하는 것 같아요

**해결**: SubAgent 설정 파일에 다음 추가
```markdown
**중요**: claude.md 파일의 [섹션명]을 반드시 참조하세요.
작업 시작 전 해당 섹션을 먼저 읽어주세요.
```

#### 문제 2: 개발 속도가 예상보다 느려요

**해결**:
1. Week 3부터 SubAgent 2개 도입 (Frontend, Backend)
2. 병렬 작업 가능한 태스크 식별
3. Skills 도입으로 반복 작업 최적화

#### 문제 3: 코드 스타일이 일관되지 않아요

**해결**:
1. claude.md의 "코드 표준" 섹션 강화
2. Linter 설정 (ESLint, Pylint)
3. Code Reviewer SubAgent 도입
4. Pre-commit hook 설정

#### 문제 4: API 비용이 예상보다 높아요

**해결**:
1. 분류 결과 캐싱 (동일 기사 재분류 방지)
2. Claude Haiku 사용 (Sonnet 대비 저렴)
3. 입력 토큰 최적화 (불필요한 텍스트 제거)

---

## 9. 다음 단계 (Phase 2)

### 9.1 Phase 2 계획

**목표**: 사용자 피드백 기반 개선 (Week 7-12)

**주요 기능**:
1. **데이터베이스 도입**:
   - 사용자 피드백 저장 (PostgreSQL)
   - 평가 이력 조회 기능

2. **AI 성능 비교**:
   - 동일 기사에 대한 3개 AI 평가 결과 비교
   - 품질 점수 시각화

3. **언론사 확장**:
   - 현재 3개 → 10개 이상 주요 언론사 지원
   - 언론사별 HTML 구조 자동 학습

4. **고급 분류**:
   - 기사 유형 세분화 (팩트체크, 데이터 저널리즘 등)
   - 다중 카테고리 분류

### 9.2 장기 비전

**Phase 3**: 커뮤니티 플랫폼 (Month 4-6)
- 사용자 평가 결과 공유
- 언론사/기자별 평가 통계
- 크라우드소싱 템플릿 기여

**Phase 4**: API 서비스 (Month 7+)
- 외부 개발자를 위한 API 제공
- 브라우저 확장 프로그램
- 모바일 앱

---

## 10. 실전 체크리스트

### Week 1 시작 전
- [ ] 개발 환경 설정 (Python 3.10+, Node.js 18+)
- [ ] Claude API 키 발급
- [ ] 기술 스택 학습 (FastAPI, Next.js 14)
- [ ] 이 문서 전체 읽기

### Week 1-2 (Foundation)
- [ ] claude.md 작성 완료
- [ ] Think→Implement→Review 워크플로우 최소 5회 사용
- [ ] 핵심 모듈 1-2개 완성 (스크래핑, 분류)
- [ ] API 엔드포인트 2개 완성

### Week 3 (Acceleration 판단 시점)
- [ ] 병렬 작업 필요성 평가
- [ ] Frontend SubAgent 도입
- [ ] 3개 페이지 구현 완료
- [ ] 효과 측정 (속도, 품질)

### Week 4-5 (Optimization)
- [ ] Backend SubAgent 추가
- [ ] 병렬 작업 경험 2회 이상
- [ ] Skills 도입 검토 (CR 평가 기준)
- [ ] Code Reviewer SubAgent 추가
- [ ] 전체 코드 리뷰 1회 이상

### MVP 출시 전
- [ ] Section 7.2의 성공 기준 모두 충족
- [ ] 통합 테스트 완료
- [ ] 보안 체크리스트 완료
- [ ] 실제 사용자 3-5명 베타 테스트
- [ ] 피드백 수집 시스템 작동 확인
- [ ] 배포 환경 설정 (Vercel, Railway)

---

## 부록

### A. 개발 속도 비교

| 작업 | 기본 방식 | SubAgent 방식 | 시간 절감 |
|------|----------|--------------|----------|
| **Frontend 3페이지** | 3일 | 2일 | 33% |
| **Backend API 2개** | 2일 | 1.5일 | 25% |
| **템플릿 21개 작성** | 7일 | 4일 | 43% |
| **코드 리뷰** | 1일 | 0.5일 | 50% |

### B. 도구 도입 결정 트리

다음 중 2개 이상 해당 시 SubAgent 도입:
- [ ] 프론트엔드와 백엔드 동시 개발 필요
- [ ] 특정 영역의 전문성 필요 (스크래핑, API 설계)
- [ ] 코드 리뷰를 체계적으로 수행하고 싶음
- [ ] 개발 속도 향상이 절실함
- [ ] Claude Code SubAgent 경험 보유

다음 상황에서는 SubAgent 불필요:
- [ ] 단순 버그 수정
- [ ] 문서 작성
- [ ] 설정 파일 수정
- [ ] 간단한 함수 추가

### C. 주요 명령어 모음

**개발 서버 실행**:
```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend
cd frontend
npm run dev
```

**테스트 실행**:
```bash
# Backend
pytest tests/ --cov=backend

# Frontend
npm run test
```

**린트 및 포맷**:
```bash
# Backend
black backend/
pylint backend/

# Frontend
npm run lint
npm run format
```

**배포**:
```bash
# Frontend (Vercel)
vercel --prod

# Backend (Railway)
railway up
```

---

**문서 버전**: 2.0 (통합 최종본)
**최종 수정일**: 2025-11-13
**작성 목적**: CR 템플릿 허브 구현을 위한 실전 기술 가이드

**라이선스**: CR 프로젝트 내부 사용
