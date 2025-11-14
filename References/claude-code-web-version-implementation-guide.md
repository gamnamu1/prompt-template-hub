# CR 템플릿 허브 구현 전략 (웹 버전)

> **Claude Code 웹 버전을 활용한 단계적 개발 가이드**

---

## 목차

1. [개요 및 목표](#1-개요-및-목표)
2. [웹 버전 vs CLI 버전 핵심 차이](#2-웹-버전-vs-cli-버전-핵심-차이)
3. [개발 전략의 핵심 원칙](#3-개발-전략의-핵심-원칙)
4. [아키텍처 설계](#4-아키텍처-설계)
5. [개발 환경 설정 (웹 버전)](#5-개발-환경-설정-웹-버전)
6. [단계별 구현 로드맵](#6-단계별-구현-로드맵)
7. [품질 관리 및 테스트](#7-품질-관리-및-테스트)
8. [성공 지표 및 평가](#8-성공-지표-및-평가)
9. [위험 관리 전략](#9-위험-관리-전략)
10. [실전 체크리스트](#10-실전-체크리스트)

---

## 1. 개요 및 목표

### 1.1 프로젝트 목적

CR 템플릿 허브는 한국 언론 기사의 저널리즘 윤리를 평가하기 위한 자동화된 도구입니다. 주요 목표는 다음과 같습니다:

- **자동화**: 기사 URL 입력 시 자동 스크래핑 및 유형 분류
- **최적화**: 기사 유형과 AI 서비스에 맞는 평가 템플릿 제공
- **확장성**: 다양한 언론사와 AI 서비스 지원
- **사용자 참여**: 평가 결과 피드백을 통한 지속적 개선

### 1.2 웹 버전 Claude Code 선택 이유

이 프로젝트는 **Claude Code 웹 버전**을 사용하여 구현합니다. 주요 이점:

- ✅ **자동 PR 생성**: Git 명령어 없이 클릭 한 번으로 PR 생성
- ✅ **환경 분리**: 개발/테스트/배포 환경을 독립적으로 관리
- ✅ **클라우드 VM**: 일관된 개발 환경, 설정 불필요
- ✅ **모바일 접근**: iOS 앱으로 이동 중에도 작업 가능
- ✅ **GitHub 통합**: 저장소 연결 및 자동 동기화

### 1.3 기대 효과

- **개발 기간**: 5-6주 내 MVP 출시
- **품질**: 역할 기반 개발로 일관된 코드 품질 유지
- **확장성**: 단계적 기능 확장을 통한 안정적 성장
- **학습 효과**: 웹 버전 Claude Code의 효율적 활용법 습득

---

## 2. 웹 버전 vs CLI 버전 핵심 차이

### 2.1 주요 차이점 요약

| 항목 | CLI 버전 | 웹 버전 | 영향 |
|------|---------|---------|------|
| **SubAgent 설정** | `.claude/agents/*.md` 파일 | `claude.md` 내 역할 통합 | 🔴 설정 방식 변경 필수 |
| **Skills 활용** | 디렉토리 복사 | ZIP 업로드 | 🔴 준비 방식 변경 필수 |
| **개발 환경** | 로컬 터미널 | 클라우드 VM | 🟡 명령어 일부 수정 |
| **PR 생성** | 수동 git 명령어 | 자동 PR 버튼 | 🟢 워크플로우 간소화 |
| **환경 관리** | 수동 설정 | UI로 여러 환경 관리 | 🟢 병렬 개발 용이 |

### 2.2 웹 버전 고유 장점

**환경 분리**:
```
backend-dev 환경     → API 개발 집중
frontend-dev 환경    → UI 개발 집중
testing 환경         → 통합 테스트
pre-production 환경  → 배포 전 검증
```

**자동 PR 생성**:
```
전통적 방식:              웹 버전:
git add .                클릭 한 번
git commit -m "..."      ↓
git push                 자동 생성
GitHub에서 PR 생성       ↓
PR 제목/설명 작성        AI가 자동 작성
```

---

## 3. 개발 전략의 핵심 원칙

### 3.1 "Start Simple, Scale Smart"

복잡한 도구를 처음부터 모두 도입하지 않고, 필요에 따라 점진적으로 확장하는 전략을 따릅니다.

**Week 1-2: Foundation First**
- claude.md 파일로 프로젝트 컨텍스트 정립
- Think→Implement→Review 워크플로우 습득
- 핵심 모듈 구현 (스크래핑, 분류)
- 웹 버전 기본 기능 익히기

**Week 3-4: Accelerate Strategically**
- 환경 분리로 병렬 작업 시작
- Backend + Frontend 동시 개발
- 자동 PR 생성 활용
- claude.md를 중심 참조 문서로 유지

**Week 5-6: Optimize & Scale**
- Skills 도입으로 반복 작업 최적화
- 역할 기반 Code Review로 품질 자동화
- 배포 자동화 구축
- 실측 데이터로 효과 검증

### 3.2 개발 워크플로우

모든 기능 개발은 다음 3단계를 따릅니다:

1. **Think**: 설계 전략 제안 및 검토
2. **Implement**: 설계를 바탕으로 코드 구현
3. **Review**: 엣지 케이스 및 개선점 검토

이 워크플로우는 역할 전환 시에도 동일하게 적용됩니다.

### 3.3 웹 버전 활용 전략

```
Week 1-2: claude.md + Think→Implement→Review + 웹 버전 익히기
Week 3-4: + 환경 분리 (backend/frontend) + 자동 PR 생성
Week 5-6: + Skills 업로드 + 역할 기반 리뷰
Week 7+:  + 고급 환경 관리 + 배포 자동화
```

---

## 4. 아키텍처 설계

### 4.1 전체 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────┐
│              claude.md (프로젝트 중심 문서)              │
│         - 모든 역할이 참조하는 단일 진실 소스            │
│         - 웹 버전에서 역할 정의 통합 관리                │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
   │Backend  │        │Frontend │        │Reviewer │
   │역할     │        │역할     │        │역할     │
   └─────────┘        └─────────┘        └─────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    Think→Implement→Review
                      워크플로우 적용
```

### 4.2 기술 스택

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
- GitHub: 버전 관리 및 CI/CD

### 4.3 프로젝트 구조

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
├── claude.md                     # 프로젝트 중심 문서 (웹 버전)
└── README.md
```

---

## 5. 개발 환경 설정 (웹 버전)

### 5.1 claude.md 템플릿 (웹 버전 특화)

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

### 역할 전환 활용 시점
다음 상황에서 명시적으로 역할을 호출합니다:
- ✅ 백엔드 API 개발: [Backend Developer 역할]
- ✅ 프론트엔드 UI 개발: [Frontend Developer 역할]
- ✅ 코드 품질 검증: [Code Reviewer 역할]
- ❌ 단순한 버그 수정이나 문서 작성 시에는 불필요

## 개발 역할 정의

### 역할 1: Backend Developer
**호출 방법**: 프롬프트에서 "[Backend Developer 역할]"로 시작

**전문 분야**:
- FastAPI 라우팅 및 미들웨어
- Pydantic 데이터 검증
- 비동기 처리 (async/await)
- 외부 API 통합 (Claude API)
- 에러 처리 및 로깅

**준수 사항**:
- claude.md의 "코드 표준 (Python)" 섹션 준수
- Think → Implement → Review 워크플로우 적용
- 프로젝트 구조에 맞는 파일 배치

**응답 형식**:
1. Think: 설계 전략 제시
2. Implement: 코드 구현
3. Review: 엣지 케이스 검토

---

### 역할 2: Frontend Developer
**호출 방법**: 프롬프트에서 "[Frontend Developer 역할]"로 시작

**전문 분야**:
- Next.js 14 App Router
- Server Components vs Client Components
- TailwindCSS 반응형 디자인
- 폼 처리 및 검증
- 상태 관리 (React hooks)

**준수 사항**:
- claude.md의 "코드 표준 (TypeScript)" 섹션 준수
- "아키텍처 철학 (마법사 방식 UI)" 참조
- Think → Implement → Review 워크플로우 적용

**응답 형식**:
1. Think: UI/UX 설계 전략
2. Implement: 컴포넌트 구현
3. Review: 접근성 및 반응형 검토

---

### 역할 3: Code Reviewer
**호출 방법**: 프롬프트에서 "[Code Reviewer 역할]"로 시작

**리뷰 체크리스트**:
1. ✅ claude.md의 코드 표준 준수 여부
2. ✅ 엣지 케이스 처리 (에러, 빈 값, 타임아웃)
3. ✅ 보안 취약점 (SQL 인젝션, XSS, API 키 하드코딩)
4. ✅ 성능 최적화 가능성
5. ✅ 타입 안정성 (타입 힌트, TypeScript strict mode)
6. ✅ 테스트 가능성 (코드 구조, 의존성 주입)

**출력 형식**:
```markdown
## 코드 리뷰 결과

### Critical Issues (즉시 수정 필요)
- [이슈 설명]
  - 파일: `파일명`
  - 라인: `라인 번호`
  - 수정 방안: [구체적 제안]

### High Priority (수정 권장)
...

### Medium Priority (개선 제안)
...

### Low Priority (최적화 제안)
...
```

## 기술 스택
- Backend: FastAPI, BeautifulSoup4, Claude API
- Frontend: Next.js 14, TypeScript, TailwindCSS
- Infrastructure: Vercel, Railway, GitHub

## 프로젝트 구조
[프로젝트 구조 포함]

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

## PR 생성 가이드 (웹 버전)

### PR 제목 형식
[타입] 간단한 설명

예시:
- [Feature] Add article classification API
- [Fix] Handle timeout in scraper
- [Refactor] Improve error handling

### PR 설명 구조
1. Changes (변경 사항)
2. Testing (테스트 방법)
3. Screenshots (UI 변경 시)
4. Checklist (체크리스트)

### 체크리스트
- [ ] 코드 표준 준수 (claude.md 참조)
- [ ] 테스트 추가/통과
- [ ] 문서 업데이트 (필요시)
- [ ] Breaking changes 없음

## 의사결정 로그

### 2025-11-14: 왜 웹 버전 Claude Code를 사용하는가?
**결정**: 웹 버전 사용
**이유**:
- 자동 PR 생성으로 Git 워크플로우 간소화
- 환경 분리로 병렬 개발 용이
- 클라우드 VM으로 일관된 개발 환경
- 모바일 접근으로 유연한 작업 가능

### 2025-11-14: SubAgent vs 역할 정의
**결정**: claude.md에 역할 통합
**이유**:
- 웹 버전에서 파일 기반 SubAgent 불확실
- 한 파일 관리로 유지보수 용이
- 명시적 호출로 더 높은 제어 가능
- 역할 조합 및 커스터마이징 자유로움

### 2025-11-14: 왜 Claude Haiku를 분류에 사용하는가?
**결정**: Haiku 사용
**이유**:
- 기사 유형 분류는 단순 작업 (5개 카테고리)
- 속도와 비용 효율성이 중요
- Sonnet 대비 10배 빠르고 20배 저렴

### 2025-11-14: 왜 Phase 1에서 DB를 사용하지 않는가?
**결정**: JSON 파일 사용
**이유**:
- MVP에서는 템플릿 매핑 데이터만 필요 (정적 데이터)
- 데이터베이스 설정 및 관리 오버헤드 회피
- Phase 2에서 사용자 피드백 저장 시 DB 도입 예정
```

### 5.2 역할 사용 예시

**Backend 개발 요청**:
```
[Backend Developer 역할]

claude.md의 Backend Developer 역할 정의를 참조하여
다음 작업을 수행해주세요:

Task: 기사 스크래핑 API 엔드포인트 구현
- 경로: POST /api/scrape
- 입력: { "url": "기사 URL" }
- 출력: Article JSON
- 에러 처리: 404, timeout, paywall

Think → Implement → Review 단계로 진행해주세요.
```

**Frontend 개발 요청**:
```
[Frontend Developer 역할]

claude.md의 Frontend Developer 역할과
"아키텍처 철학 (마법사 방식 UI)"를 참조하여

app/page.tsx 구현:
- URL 입력 폼
- 유효성 검증 (한국 언론사 URL만)
- 로딩 상태 표시
- 에러 메시지 처리

Think → Implement → Review 단계로 진행해주세요.
```

**코드 리뷰 요청**:
```
[Code Reviewer 역할]

다음 파일들을 리뷰해주세요:
- backend/scraper.py
- backend/classifier.py
- app/page.tsx

claude.md의 코드 표준을 기준으로
보안, 성능, 타입 안정성을 중점 검토해주세요.
```

### 5.3 Skills 설정 (웹 버전)

웹 버전에서 Skills를 사용하려면 **로컬에서 준비 → ZIP 업로드 → 웹에서 활용** 순서로 진행합니다.

#### Step 1: 로컬에서 Skill 준비

**디렉토리 구조 생성**:
```
cr-evaluation-criteria/
├── SKILL.md              # 필수: Skill 메타데이터 및 내용
└── examples/             # 선택: 예시 파일들
    ├── straight-news.md
    └── analysis.md
```

**SKILL.md 작성**:
```markdown
---
name: CR Evaluation Criteria
description: 한국 언론 기사를 8차원 평가 기준으로 분석
version: 1.0.0
author: CR Project Team
---

# CR 프로젝트 8차원 평가 기준

이 Skill은 한국 언론 기사의 저널리즘 윤리를 평가하기 위한 8가지 차원의 기준을 제공합니다.

## 사용 방법

프롬프트에서 다음과 같이 호출:
```
"CR 평가 기준 Skill을 활용하여 [기사 유형]에 맞는 평가 템플릿을 작성해주세요."
```

## 평가 8차원

### 1. 진실성 (Truth)

**평가 포인트**:
- 사실과 의견 구분이 명확한가?
- 검증 가능한 출처를 제시하는가?
- 확인되지 않은 정보를 명시하는가?

**체크리스트**:
- [ ] 사실 진술과 의견이 명확히 구분됨
- [ ] 주요 주장에 대한 출처 제시
- [ ] 추정/예상 내용에 "~로 보인다" 등 명시

### 2. 정확성 (Accuracy)

**평가 포인트**:
- 숫자와 통계가 정확한가?
- 인용이 정확한가?
- 맥락이 왜곡되지 않았는가?

[... 나머지 차원들 ...]

## 기사 유형별 중점 차원

| 기사 유형 | 중점 평가 차원 |
|----------|--------------|
| **스트레이트 뉴스** | 진실성, 정확성, 투명성 |
| **해설/분석** | 공정성, 맥락, 독립성 |
| **인터뷰** | 공정성, 투명성, 인권 존중 |
| **사설/칼럼** | 논리성, 독립성, 책임성 |
| **탐사 보도** | 진실성, 정확성, 투명성, 책임성 |
```

#### Step 2: ZIP 파일 생성

**로컬에서 압축**:
```bash
# macOS/Linux
cd /path/to/parent-directory
zip -r cr-evaluation-criteria.zip cr-evaluation-criteria/

# Windows (PowerShell)
Compress-Archive -Path cr-evaluation-criteria -DestinationPath cr-evaluation-criteria.zip
```

**확인 사항**:
- [ ] SKILL.md 파일이 루트에 있음
- [ ] 압축 파일 크기가 적절함 (< 10MB)
- [ ] 불필요한 파일 제외 (.DS_Store, __pycache__ 등)

#### Step 3: 웹에서 업로드

1. **Claude.ai 접속** → 상단 설정 아이콘 클릭
2. **Capabilities** 탭 선택
3. **"Code execution and file creation"** 활성화 (필수)
4. **Skills** 섹션으로 스크롤
5. **"Upload custom skill"** 클릭
6. `cr-evaluation-criteria.zip` 파일 선택
7. 업로드 완료 대기 (수 초 소요)
8. Skill 목록에서 활성화 확인

#### Step 4: Skills 활용

**프롬프트 예시**:
```
[Backend Developer 역할]

CR 평가 기준 Skill을 참조하여
backend/templates/claude-sonnet-4/straight-news.md 파일을 생성해주세요.

포함 사항:
1. CR 8차원 평가 기준 체크리스트
2. 각 차원별 구체적 질문 (5-7개)
3. 평가 방법 가이드
4. 출력 형식 예시 (JSON)

Think → Implement → Review 단계로 진행해주세요.
```

### 5.4 환경 관리 전략 (웹 버전 전용)

웹 버전 Claude Code의 **Environment 관리 기능**을 활용하여 개발/테스트/배포 환경을 분리합니다.

#### 환경 분리 전략

**1. 개발 환경 (Default)**
- **목적**: 일반적인 기능 개발
- **설정**: Python 3.10+, Node.js 18+ (자동 제공)
- **사용 시점**: 새로운 기능 프로토타이핑, 코드 실험

**2. 백엔드 환경 (backend-dev)**
- **목적**: 백엔드 집중 개발
- **설정**: FastAPI, BeautifulSoup4, Anthropic SDK 설치
- **사용 시점**: API 엔드포인트 개발, 스크래핑 로직 구현

**3. 프론트엔드 환경 (frontend-dev)**
- **목적**: 프론트엔드 집중 개발
- **설정**: Next.js 14, TypeScript, TailwindCSS
- **사용 시점**: UI 컴포넌트 개발, 페이지 라우팅 구현

**4. 테스트 환경 (testing)**
- **목적**: 통합 테스트 및 에러 시나리오 검증
- **설정**: pytest, Jest 설치, Mock 데이터 준비
- **사용 시점**: 전체 플로우 테스트, 에러 처리 검증

**5. 배포 준비 환경 (pre-production)**
- **목적**: 배포 전 최종 확인
- **설정**: 프로덕션 설정 적용, 환경 변수 검증
- **사용 시점**: 최종 검증, 프로덕션 빌드 테스트

#### 환경별 초기 설정

**backend-dev 환경**:
```bash
# 첫 실행 시
pip install fastapi uvicorn beautifulsoup4 anthropic python-dotenv --break-system-packages

# 확인
python -c "import fastapi; import anthropic; print('Backend ready')"
```

**frontend-dev 환경**:
```bash
# 첫 실행 시
cd frontend
npm install

# 확인
npm run build
```

**testing 환경**:
```bash
# Backend 테스트
pip install pytest pytest-cov pytest-asyncio --break-system-packages

# Frontend 테스트
cd frontend
npm install --save-dev jest @testing-library/react
```

### 5.5 자동 PR 생성 워크플로우 (웹 버전 강점)

웹 버전의 **자동 PR 생성 기능**을 활용하여 Git 워크플로우를 간소화합니다.

#### 기본 워크플로우

**1. 기능 개발 시작**
```
1. Claude Code 웹 접속
2. GitHub 저장소 선택: gamnamu1/prompt-template-hub
3. 환경 선택 (예: backend-dev)
4. 작업 시작
```

**2. 코드 작성**
```
프롬프트:
"[Backend Developer 역할]

backend/scraper.py 구현:
- 기사 URL에서 제목, 내용 추출
- 조선일보, 중앙일보, 한겨레 지원
- 에러 처리 포함"

→ Claude가 코드 생성
→ 파일 생성 확인
```

**3. PR 생성**
```
1. 화면 하단 브랜치 이름 필드 확인
   - 자동 생성: "claude/implement-article-scraper"
   - 원하면 수정 가능: "feature/article-scraper"

2. "PR 생성" 버튼 클릭

3. GitHub에서 자동으로:
   ✅ 브랜치 생성
   ✅ 변경사항 커밋
   ✅ PR 생성
   ✅ PR 제목/설명 작성
```

#### 브랜치 명명 규칙

**팀 규칙 반영**:
```
feature/[기능명]       # 새 기능
fix/[버그명]          # 버그 수정
refactor/[개선명]     # 리팩토링
docs/[문서명]         # 문서화
test/[테스트명]       # 테스트 추가
```

---

## 6. 단계별 구현 로드맵

### 6.1 Week 1: Foundation (웹 버전)

#### Day 1: 초기 설정

**환경 준비**:
```
체크리스트:
- [ ] Claude.ai Pro 또는 Max 플랜 가입
- [ ] Code Execution 기능 활성화
- [ ] GitHub 저장소 생성: gamnamu1/prompt-template-hub
- [ ] Claude Code 웹 접속: claude.com/code
- [ ] 저장소 연결 및 권한 확인
```

**첫 환경 생성**:
```
1. 환경 이름: "cr-dev"
2. GitHub 저장소 선택
3. 초기 구조 확인:
   - README.md
   - .gitignore
   - LICENSE
```

#### Day 2-3: claude.md 작성 (웹 버전 특화)

**프롬프트 예시**:
```
"CR 템플릿 허브 프로젝트를 위한 claude.md 파일을 작성해주세요.

웹 버전 Claude Code 사용을 전제로:

1. 프로젝트 컨텍스트
   - 목표: 한국 언론 기사 저널리즘 윤리 평가 자동화
   - 핵심 가치: 투명성, 객관성, 접근성

2. 개발 역할 정의
   - Backend Developer 역할
   - Frontend Developer 역할
   - Code Reviewer 역할
   (각 역할별 전문 분야, 준수 사항, 응답 형식 포함)

3. 환경 관리 전략
   - 개발/테스트/배포 환경 분리
   - 환경별 사용 시점 및 설정

4. 자동 PR 워크플로우
   - 브랜치 명명 규칙
   - PR 템플릿 및 가이드라인

5. 기술 스택
   - Backend: FastAPI, BeautifulSoup4, Claude API
   - Frontend: Next.js 14, TypeScript, TailwindCSS

6. 코드 표준
   - Python (PEP 8, 타입 힌트, docstring)
   - TypeScript (ESLint, Prettier, strict mode)

7. 의사결정 로그
   - 주요 기술 선택 이유 기록

파일 생성 위치: ./claude.md"
```

**생성 후 확인**:
```
- [ ] claude.md 파일 생성 완료
- [ ] 모든 섹션 포함 확인
- [ ] 역할 정의가 명확한지 검토
```

**PR 생성**:
```
브랜치: docs/project-setup
제목: [Docs] Add project claude.md configuration
설명: Initialize project with comprehensive claude.md
```

#### Day 4-5: 핵심 모듈 개발

**스크래핑 모듈 구현**:
```
[Backend Developer 역할]

claude.md의 Backend Developer 역할 정의를 참조하여
다음 작업을 수행해주세요:

Task: backend/scraper.py 구현

요구사항:
- 한국 주요 언론사 기사 스크래핑
  * 조선일보: chosun.com
  * 중앙일보: joongang.co.kr
  * 한겨레: hani.co.kr

- 출력 형식:
  {
    "title": "기사 제목",
    "content": "본문 내용",
    "author": "기자명",
    "published_date": "2025-11-14",
    "url": "원본 URL"
  }

- 에러 처리:
  * 404 Not Found
  * Timeout (10초)
  * Paywall 기사

- 코드 표준 준수:
  * 타입 힌트 필수
  * Google Style docstring
  * 에러 로깅 포함

Think → Implement → Review 단계로 진행해주세요.
```

**PR 생성**:
```
브랜치: feature/article-scraper
(자동 생성 또는 수동으로 이름 지정)

PR 자동 생성:
- 제목: [Feature] Implement article scraper
- 설명: (Claude가 자동 생성)
- 리뷰어: (GitHub에서 수동 지정)
```

**성과 체크**:
- [ ] claude.md 파일 완성
- [ ] 스크래핑 모듈 작동 (3개 언론사 테스트)
- [ ] Think→Implement→Review 워크플로우 습득
- [ ] 웹 버전 자동 PR 생성 경험

### 6.2 Week 2: Classification & API (웹 버전)

#### 환경 전환

```
기존 "cr-dev" 환경에서 계속 진행
또는
"backend-dev" 환경 새로 생성하여 백엔드 집중
```

#### 분류 모듈 구현

```
[Backend Developer 역할]

backend/classifier.py 구현:

기능:
- Claude Haiku를 사용한 기사 유형 분류
- 5개 카테고리: 스트레이트, 해설, 인터뷰, 사설, 기타

입력:
{
  "title": "...",
  "content": "..."
}

출력:
{
  "article_type": "straight_news",
  "confidence": 0.92,
  "reasoning": "..."
}

Think → Implement → Review
```

#### API 엔드포인트 구현

```
[Backend Developer 역할]

backend/main.py에 FastAPI 엔드포인트 추가:

1. POST /api/scrape
   - 입력: { "url": "기사 URL" }
   - 출력: 스크래핑 결과

2. POST /api/classify
   - 입력: { "title": "...", "content": "..." }
   - 출력: 분류 결과

3. GET /api/health
   - 헬스 체크

Pydantic 모델로 검증
에러 처리 포함
```

**성과 체크**:
- [ ] 기사 분류 API 작동 (테스트 5건 이상)
- [ ] FastAPI 엔드포인트 3개 완성
- [ ] API 문서 (OpenAPI) 자동 생성 확인
- [ ] PR 자동 생성으로 Git 워크플로우 간소화 체감

### 6.3 Week 3: Frontend Development (웹 버전)

#### 환경 전환

```
새 환경 생성: "frontend-dev"
또는
기존 환경에서 프론트엔드 작업
```

#### UI 개발

**메인 페이지**:
```
[Frontend Developer 역할]

claude.md의 Frontend Developer 역할과
"아키텍처 철학 (마법사 방식 UI)"를 참조하여

app/page.tsx 구현:

기능:
- URL 입력 폼
- 유효성 검증 (한국 언론사 URL)
- 로딩 상태 표시
- 에러 메시지 처리
- 다음 단계로 이동 버튼

디자인:
- TailwindCSS 사용
- 반응형 (모바일/데스크톱)
- 접근성 (a11y) 고려

Think → Implement → Review
```

**분석 결과 페이지**:
```
[Frontend Developer 역할]

app/analysis/page.tsx 구현:

기능:
- 분류 결과 표시
- 사용자가 결과 수정 가능 (드롭다운)
- AI 서비스 선택 (Claude, ChatGPT, Gemini)
- 다운로드 페이지로 이동

Think → Implement → Review
```

**다운로드 페이지**:
```
[Frontend Developer 역할]

app/download/page.tsx 구현:

기능:
- 템플릿 미리보기
- 다운로드 버튼 (.md, .txt)
- 클립보드 복사
- Google Forms 피드백 링크

Think → Implement → Review
```

**성과 체크**:
- [ ] 환경 분리 경험 (선택 사항)
- [ ] 3개 페이지 구현 완료
- [ ] 반응형 디자인 확인
- [ ] 각 페이지별 PR 생성 (3개)

### 6.4 Week 4: Parallel Development (웹 버전 활용)

#### 병렬 작업 전략

**방법 1: 환경 분리**
```
탭/창 1: backend-dev 환경
Task: 템플릿 매핑 시스템 구현

탭/창 2: frontend-dev 환경
Task: UI 개선 및 폴리싱

각각 독립적으로 작업 후 PR 생성
```

**방법 2: 순차적 역할 전환**
```
오전: [Backend Developer 역할]
- 템플릿 서비스 구현
- PR 생성

오후: [Frontend Developer 역할]
- 다운로드 페이지 개선
- PR 생성
```

#### Backend: 템플릿 매핑

```
[Backend Developer 역할]

data/template_mapping.json 설계 및
backend/template_service.py 구현:

기능:
- 기사 유형 + AI 서비스 → 템플릿 경로 매핑
- GET /api/templates/{article_type}/{ai_service}
- 템플릿 파일 읽기 및 반환

Think → Implement → Review
```

#### Frontend: UI 개선

```
[Frontend Developer 역할]

다운로드 페이지 개선:
- 템플릿 미리보기 기능
- 복사 버튼 (클립보드 API)
- 다운로드 통계 표시
- 애니메이션 효과

Think → Implement → Review
```

**성과 체크**:
- [ ] 병렬 작업 경험 (환경 분리 또는 역할 전환)
- [ ] 동시에 2개 PR 생성
- [ ] 개발 속도 향상 체감
- [ ] 웹 버전 장점 활용

### 6.5 Week 5: Skills & Quality (웹 버전)

#### Skills 준비 (로컬에서)

**Day 1: Skill 생성**
```
로컬 컴퓨터에서:

1. 폴더 생성: cr-evaluation-criteria/
2. SKILL.md 작성 (CR 8차원 평가 기준)
3. 예시 파일 추가: examples/
4. ZIP 압축
```

**Day 2: Skill 업로드**
```
Claude.ai 웹 → Settings → Skills
→ cr-evaluation-criteria.zip 업로드
→ 활성화 확인
```

#### Code Review (역할 활용)

**Day 3-4: 전체 리뷰**
```
[Code Reviewer 역할]

전체 프로젝트 코드를 리뷰해주세요:

Backend 파일:
- backend/scraper.py
- backend/classifier.py
- backend/main.py
- backend/template_service.py

Frontend 파일:
- app/page.tsx
- app/analysis/page.tsx
- app/download/page.tsx

중점 검토:
1. claude.md 코드 표준 준수
2. 보안 취약점 (API 키, XSS, 입력 검증)
3. 성능 병목
4. 에러 처리 충분성
5. 타입 안정성
6. 테스트 가능성

각 파일별로 Critical/High/Medium/Low 이슈 분류
```

#### 템플릿 생성 (Skills 활용)

**Day 5: 템플릿 생성**
```
CR 평가 기준 Skill을 참조하여
다음 템플릿들을 생성해주세요:

1. backend/templates/claude-sonnet-4/straight-news.md
2. backend/templates/claude-sonnet-4/analysis-article.md
3. backend/templates/chatgpt-4o/straight-news.md
4. backend/templates/gemini-pro/straight-news.md

각 템플릿:
- CR 8차원 체크리스트
- 차원별 세부 질문 (5-7개)
- 평가 방법 가이드
- JSON 출력 형식
```

**성과 체크**:
- [ ] CR 평가 기준 Skill 생성 및 업로드
- [ ] 역할 기반 전체 리뷰 완료
- [ ] 주요 이슈 10개 이상 발견 및 수정
- [ ] Skills 활용으로 템플릿 생성 완료

### 6.6 Week 6: 배포 (웹 버전 최적화)

#### 배포 준비

```
"pre-production" 환경 생성
→ 프로덕션 설정 테스트
→ 환경 변수 검증
→ 빌드 테스트
```

#### Vercel 배포 (Frontend)

```
방법 1: GitHub 연동 (권장)
1. Vercel에서 GitHub 저장소 연결
2. main 브랜치 자동 배포 설정
3. PR마다 Preview 배포 자동 생성

방법 2: 웹에서 직접 배포
cd frontend
vercel --prod
```

#### Railway 배포 (Backend)

```
방법 1: GitHub 연동 (권장)
1. Railway에서 GitHub 저장소 연결
2. main 브랜치 자동 배포
3. 환경 변수 설정

방법 2: 웹에서 직접 배포
cd backend
railway up
```

#### 최종 PR

```
브랜치: release/v1.0.0
제목: [Release] CR Template Hub v1.0.0
설명:
- 전체 기능 구현 완료
- 테스트 통과 확인
- 배포 환경 설정 완료
```

**성과 체크**:
- [ ] 배포 환경 설정 완료
- [ ] 전체 플로우 테스트 통과
- [ ] Vercel + Railway 배포 성공
- [ ] HTTPS 및 CORS 설정 확인

---

## 7. 품질 관리 및 테스트

### 7.1 테스트 전략

**Backend 테스트**:
```bash
# pytest 설치
pip install pytest pytest-cov pytest-asyncio --break-system-packages

# 테스트 실행
cd backend
pytest tests/ -v

# 커버리지 리포트
pytest tests/ --cov=backend --cov-report=html
```

**Frontend 테스트**:
```bash
cd frontend

# 단위 테스트
npm run test

# 커버리지
npm run test -- --coverage

# 빌드 테스트
npm run build
```

### 7.2 보안 체크리스트

**백엔드 보안**:
- [ ] API 키 환경변수 관리 (.env 파일, .gitignore)
- [ ] 입력 검증 (Pydantic 모델)
- [ ] CORS 설정 (허용된 도메인만)
- [ ] Rate limiting (API 호출 제한)

**프론트엔드 보안**:
- [ ] XSS 방어 (사용자 입력 sanitize)
- [ ] HTTPS 사용 (배포 환경)
- [ ] 민감 정보 클라이언트 노출 방지

---

## 8. 성공 지표 및 평가

### 8.1 개발 과정 지표

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| **MVP 출시 기간** | 5-6주 | 프로젝트 시작~배포 날짜 |
| **코드 커버리지** | 80% | pytest-cov, Jest coverage |
| **PR 생성 시간** | < 1분 | 자동 PR 기능 활용 |
| **claude.md 업데이트 빈도** | 주 2회 | Git commit 히스토리 |
| **환경 분리 활용** | 3개 이상 | 생성된 환경 수 |

### 8.2 최종 결과물 품질 지표

**Phase 1 (MVP) 성공 기준**:
- [ ] 기사 스크래핑 성공률 90% 이상 (주요 3개 언론사)
- [ ] 기사 분류 정확도 70% 이상
- [ ] 전체 플로우 완료 시간 3분 이내
- [ ] 모바일/데스크톱 모두 정상 작동
- [ ] 템플릿 다운로드 기능 작동
- [ ] Google Forms 피드백 수집 가능

---

## 9. 위험 관리 전략

### 9.1 기술적 위험

| 위험 | 발생 확률 | 영향도 | 완화 전략 |
|------|----------|--------|----------|
| **웹 VM 제약** | 중간 | 중간 | 로컬 테스트 병행, 배포 환경 활용 |
| **API 호출 실패** | 높음 | 중간 | Retry 로직, 타임아웃 설정 |
| **스크래핑 실패** | 높음 | 높음 | 다중 파싱 전략, 에러 로깅 |
| **성능 병목** | 중간 | 중간 | 프로파일링, 캐싱, 비동기 처리 |

### 9.2 웹 버전 특수 이슈

**Q: 로컬 서버 접근이 제한적이에요**
```
A: 권장 대안:
- Vercel Preview 환경에서 테스트
- Railway 스테이징 환경 활용
- 데스크톱 앱으로 로컬 테스트 후 웹에서 배포
```

**Q: Skills가 적용되지 않는 것 같아요**
```
A: 프롬프트에서 명시적으로 언급하세요:
"CR 평가 기준 Skill의 [섹션명]을 참조하여..."
```

**Q: 환경 간 코드 동기화는 어떻게 하나요?**
```
A: 모든 환경이 같은 GitHub 저장소에 연결되어 있으므로:
1. 한 환경에서 PR 생성
2. 다른 환경에서 git pull
3. 자동 동기화됨
```

---

## 10. 실전 체크리스트

### 10.1 Week 1 시작 전

```
초기 설정:
- [ ] Claude.ai Pro/Max 플랜 가입
- [ ] Code Execution 기능 활성화
- [ ] GitHub 계정 및 저장소 준비
- [ ] Claude API 키 발급
- [ ] 이 가이드 문서 전체 읽기
```

### 10.2 Week 1-2 (Foundation)

```
claude.md 작성:
- [ ] 프로젝트 컨텍스트 정의
- [ ] 개발 역할 정의 (3개 역할)
- [ ] 환경 관리 전략
- [ ] 자동 PR 워크플로우
- [ ] 기술 스택 및 코드 표준
- [ ] 의사결정 로그 시작

핵심 모듈:
- [ ] backend/scraper.py 구현 및 테스트
- [ ] backend/classifier.py 구현
- [ ] API 엔드포인트 3개 완성
- [ ] Think→Implement→Review 워크플로우 5회 이상 사용
- [ ] 자동 PR 생성 경험
```

### 10.3 Week 3 (Frontend Development)

```
환경 설정:
- [ ] "frontend-dev" 환경 생성 (선택)
- [ ] Next.js 프로젝트 초기화

UI 개발:
- [ ] app/page.tsx 완성
- [ ] app/analysis/page.tsx 완성
- [ ] app/download/page.tsx 완성
- [ ] 반응형 디자인 확인 (모바일/데스크톱)
- [ ] 접근성 (a11y) 기본 준수

PR 관리:
- [ ] 각 페이지별 PR 생성 (3개)
- [ ] PR 설명 자동 생성 확인
- [ ] 리뷰 및 머지
```

### 10.4 Week 4 (Parallel Development)

```
병렬 작업:
- [ ] Backend: 템플릿 매핑 시스템
- [ ] Frontend: UI 개선
- [ ] 독립적인 2개 PR 동시 생성
- [ ] 환경 분리 또는 역할 전환 활용

효과 측정:
- [ ] 개발 속도 향상 체감
- [ ] 웹 버전 장점 활용도 평가
```

### 10.5 Week 5 (Skills & Quality)

```
Skills 준비:
- [ ] 로컬에서 cr-evaluation-criteria 폴더 생성
- [ ] SKILL.md 작성 (CR 8차원)
- [ ] ZIP 파일 생성
- [ ] Claude.ai 웹에서 업로드
- [ ] 활성화 확인

코드 리뷰:
- [ ] [Code Reviewer 역할]로 전체 리뷰
- [ ] Critical 이슈 모두 수정
- [ ] High 이슈 80% 이상 수정
- [ ] 리팩토링 PR 생성

템플릿 생성:
- [ ] CR 평가 기준 Skill 활용
- [ ] 최소 6개 템플릿 생성
- [ ] 템플릿 PR 생성
```

### 10.6 Week 6 (Deployment)

```
배포 준비:
- [ ] "pre-production" 환경에서 최종 테스트
- [ ] 환경 변수 검증
- [ ] 프로덕션 빌드 테스트
- [ ] 성능 테스트 (동시 사용자 10명)

배포 실행:
- [ ] Vercel: Frontend 배포
- [ ] Railway: Backend 배포
- [ ] HTTPS 설정 확인
- [ ] CORS 설정 확인
- [ ] 도메인 연결 (선택)

최종 검증:
- [ ] 전체 플로우 테스트 (URL → 다운로드)
- [ ] 에러 시나리오 테스트
- [ ] 모바일 테스트
- [ ] Google Forms 연동 확인
- [ ] 베타 사용자 3-5명 테스트
```

### 10.7 MVP 출시 전 최종 체크

```
기능:
- [ ] 기사 스크래핑 성공률 90% 이상
- [ ] 기사 분류 정확도 70% 이상
- [ ] 전체 플로우 완료 시간 3분 이내
- [ ] 템플릿 다운로드 정상 작동
- [ ] 피드백 수집 시스템 작동

보안:
- [ ] API 키 환경변수 관리
- [ ] 입력 검증 (Pydantic)
- [ ] CORS 설정
- [ ] Rate limiting
- [ ] XSS 방어

문서:
- [ ] README.md 업데이트
- [ ] API 문서 작성
- [ ] 사용자 가이드 작성
- [ ] claude.md 최종 업데이트
```

---

## 부록

### A. 웹 버전 주요 명령어

#### 의존성 설치

**Backend**:
```bash
# Python 패키지
pip install -r requirements.txt --break-system-packages

# 개별 설치
pip install fastapi uvicorn beautifulsoup4 anthropic --break-system-packages
```

**Frontend**:
```bash
cd frontend
npm install
```

**중요**: 웹 버전에서는 `--break-system-packages` 플래그 필수 (pip)

#### 개발 서버 실행

**Backend (FastAPI)**:
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend (Next.js)**:
```bash
cd frontend
npm run dev
```

**주의사항**:
- 웹 VM에서는 `localhost` 직접 접근이 제한적
- **권장**: Vercel Preview 또는 Railway 스테이징 환경에서 테스트

#### 환경 변수 설정

**Backend (.env 파일)**:
```bash
cat > backend/.env <<EOF
ANTHROPIC_API_KEY=your_api_key_here
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
LOG_LEVEL=INFO
EOF
```

**Frontend (.env.local)**:
```bash
cat > frontend/.env.local <<EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GA_ID=your_ga_id
EOF
```

### B. 웹 버전 vs CLI 버전 장단점

| 항목 | 웹 버전 | CLI 버전 |
|------|--------|---------|
| **PR 생성** | ✅ 자동 (클릭 1번) | ❌ 수동 (git 명령어) |
| **환경 관리** | ✅ UI로 쉽게 분리 | ❌ 수동 설정 |
| **모바일 접근** | ✅ iOS 앱 지원 | ❌ 불가능 |
| **로컬 서버** | ❌ 제한적 | ✅ 직접 접근 |
| **파일 시스템** | ❌ VM 환경 | ✅ 로컬 파일 |
| **MCP 서버** | ❌ 미지원 | ✅ 지원 |

**권장 조합**: 웹 버전 주 개발 + 데스크톱 앱 로컬 테스트

### C. 개발 속도 비교 (예상)

| 작업 | 전통적 방식 | 웹 버전 | 시간 절감 |
|------|----------|---------|----------|
| **PR 생성** | 5분 | 30초 | 90% |
| **환경 설정** | 30분 | 5분 | 83% |
| **Frontend 3페이지** | 3일 | 2.5일 | 17% |
| **Backend API 3개** | 2일 | 1.8일 | 10% |
| **코드 리뷰** | 1일 | 0.5일 | 50% |

---

**문서 버전**: 2.0 (웹 버전 특화)
**최종 수정일**: 2025-11-14
**작성 목적**: CR 템플릿 허브 웹 버전 구현 가이드

**라이선스**: CR 프로젝트 내부 사용
