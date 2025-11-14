# Claude Code 웹 버전 구현 가이드

> **CR 템플릿 허브 설계도의 웹 버전 적응 방안**
> 
> 작성일: 2025-11-14  
> 목적: CLI 기반 설계를 웹 버전 Claude Code에 맞게 수정

---

## 목차

1. [개요](#1-개요)
2. [웹 버전 vs CLI 버전 핵심 차이](#2-웹-버전-vs-cli-버전-핵심-차이)
3. [필수 수정 항목 요약](#3-필수-수정-항목-요약)
4. [섹션별 상세 수정 사항](#4-섹션별-상세-수정-사항)
5. [추가 활용 전략](#5-추가-활용-전략)
6. [수정된 개발 로드맵](#6-수정된-개발-로드맵)
7. [실전 체크리스트](#7-실전-체크리스트)

---

## 1. 개요

### 1.1 검토 결과

기존 `CR_PTH__통합_최적_전략_CC.md` 설계도는 **Claude Code CLI 버전**을 전제로 작성되었습니다. 웹 버전으로 구현 시 **전체의 85%는 그대로 사용 가능**하지만, 나머지 15%는 웹 버전의 특성에 맞게 수정이 필요합니다.

### 1.2 구현 가능성

#### ✅ 웹 버전으로 완전히 구현 가능한 부분 (85%)
- FastAPI 백엔드 개발
- Next.js 프론트엔드 개발
- GitHub 저장소 연결 및 코드 작성
- 자동 PR 생성
- 기본 개발 워크플로우
- 환경 분리 및 테스트
- 배포 프로세스

#### ⚠️ 수정이 필요한 부분 (15%)
- SubAgent 설정 방식
- Skills 활용 방법
- 로컬 파일 시스템 기반 명령어
- 개발 환경 초기 설정

---

## 2. 웹 버전 vs CLI 버전 핵심 차이

### 2.1 SubAgent 설정

| 항목 | CLI 버전 | 웹 버전 |
|------|---------|---------|
| **설정 위치** | `.claude/agents/*.md` 파일 | `claude.md` 내 역할 통합 |
| **활성화 방식** | 자동 인식 | 프롬프트에서 명시적 호출 |
| **컨텍스트 공유** | 각 파일 독립 | claude.md 중심 공유 |
| **설정 난이도** | 높음 (파일 구조 필요) | 낮음 (문서 작성만) |

### 2.2 Skills 활용

| 항목 | CLI 버전 | 웹 버전 |
|------|---------|---------|
| **설치 방식** | 디렉토리 복사 | .ZIP 파일 업로드 |
| **저장 위치** | `~/.claude/skills/` | 클라우드 저장소 |
| **공유 방식** | Git 저장소 | 웹 UI 업로드 |
| **업데이트** | 파일 수정 | 재업로드 |

### 2.3 개발 환경

| 항목 | CLI 버전 | 웹 버전 |
|------|---------|---------|
| **실행 환경** | 로컬 터미널 | 클라우드 VM |
| **파일 접근** | 직접 파일 시스템 접근 | VM 내 파일 시스템 |
| **포트 확인** | localhost 직접 접근 | 제한적 (배포 환경 권장) |
| **Git 작업** | 수동 git 명령어 | 자동 PR 생성 |

### 2.4 웹 버전만의 고유 기능

| 기능 | 설명 | 활용도 |
|------|------|--------|
| **환경 관리** | UI로 여러 환경 생성/전환 | ⭐⭐⭐⭐⭐ |
| **자동 PR 생성** | 클릭 한 번으로 PR 생성 | ⭐⭐⭐⭐⭐ |
| **모바일 접근** | iOS 앱으로 코드 작업 | ⭐⭐⭐⭐ |
| **격리된 VM** | 프로젝트별 독립 환경 | ⭐⭐⭐⭐ |

---

## 3. 필수 수정 항목 요약

### 3.1 즉시 수정 필요 (Critical)

| 우선순위 | 섹션 | 원본 내용 | 수정 필요 이유 |
|---------|------|----------|---------------|
| 🔴 P0 | 4.2 SubAgent 설정 | `.claude/agents/*.md` 파일 기반 | 웹 버전에서 작동 안 함 |
| 🔴 P0 | 4.3 Skills 설정 | 디렉토리 복사 명령어 | 웹 버전은 .ZIP 업로드 |
| 🟡 P1 | 부록 C. 주요 명령어 | 로컬 명령어 (`cd`, `uvicorn`) | 웹 VM 환경 차이 |
| 🟡 P1 | 5.1-5.5 Week별 로드맵 | CLI 워크플로우 | 웹 버전 워크플로우로 |

### 3.2 보강 권장 (Important)

| 우선순위 | 내용 | 추가 이유 |
|---------|------|----------|
| 🟢 P2 | 4.4 환경 관리 섹션 추가 | 웹 버전 고유 기능 활용 |
| 🟢 P2 | 4.5 자동 PR 워크플로우 추가 | 웹 버전 장점 극대화 |
| 🟢 P2 | 8.3 웹 버전 특수 이슈 | 문제 해결 가이드 |

---

## 4. 섹션별 상세 수정 사항

### 4.1 Section 4.2: SubAgent 설정 (🔴 P0 수정)

#### 원본 내용
```markdown
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
...
```

#### 문제점
- 웹 버전에서 `.claude/agents/` 디렉토리가 정상 작동하지 않을 가능성 높음
- 파일 기반 설정이 클라우드 VM 환경에 부적합

#### 수정 내용

```markdown
### 4.2 역할 기반 개발 (웹 버전)

웹 버전에서는 **claude.md 파일에 모든 역할을 통합 정의**하고, 프롬프트에서 명시적으로 역할을 호출합니다.

#### claude.md에 역할 정의 통합

`claude.md` 파일에 다음 섹션 추가:

```markdown
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
```

#### 사용 방법

**예시 1: Backend 개발 요청**
```
[Backend Developer 역할]

claude.md의 Backend Developer 역할 정의를 참조하여
다음 작업을 수행해주세요:

Task: 기사 스크래핑 API 엔드포인트 구현
- 경로: POST /api/scrape
- 입력: { "url": "기사 URL" }
- 출력: { "title": "...", "content": "...", ... }
- 에러 처리: 404, timeout, paywall

Think → Implement → Review 단계로 진행해주세요.
```

**예시 2: Frontend 개발 요청**
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

**예시 3: 코드 리뷰 요청**
```
[Code Reviewer 역할]

다음 파일들을 리뷰해주세요:
- backend/scraper.py
- backend/classifier.py
- app/page.tsx

claude.md의 코드 표준을 기준으로
보안, 성능, 타입 안정성을 중점 검토해주세요.
```

#### 장단점 비교

| 구분 | CLI 방식 (.claude/agents/) | 웹 방식 (claude.md 통합) |
|------|---------------------------|-------------------------|
| **설정** | 복잡 (여러 파일) | 간단 (한 파일) |
| **유지보수** | 파일 여러 개 수정 | claude.md만 수정 |
| **명시성** | 낮음 (자동 인식) | 높음 (명시적 호출) |
| **유연성** | 제한적 | 높음 (역할 조합 가능) |
| **웹 버전 호환** | ❌ 불확실 | ✅ 보장됨 |
```

---

### 4.2 Section 4.3: Skills 설정 (🔴 P0 수정)

#### 원본 내용
```markdown
### 4.3 Skills 설정 (Week 5 이후)

**CR 평가 기준 Skill 생성**:

```bash
# Skill_Seekers 디렉토리에서 작업
cd Skill_Seekers

# CR 평가 기준 문서 준비
cat > cr-evaluation-criteria.md <<EOF
...
EOF

# Skill 패키징
mkdir -p output/cr-criteria
cp cr-evaluation-criteria.md output/cr-criteria/
python3 cli/package_skill.py output/cr-criteria/

# Claude Code에 업로드 (웹 인터페이스에서 수동)
```

#### 문제점
- CLI 명령어로 작성됨
- 웹 버전은 .ZIP 파일 업로드 방식 사용
- 디렉토리 구조가 아닌 파일 업로드

#### 수정 내용

```markdown
### 4.3 Skills 활용 (웹 버전)

웹 버전에서 Skills를 사용하려면 **로컬에서 준비 → .ZIP 업로드 → 웹에서 활용** 순서로 진행합니다.

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

**문제 사례**:
- "정부가 부정행위를 저질렀다" (검증 없이 단정)
- "전문가들은 반대한다" (구체적 출처 없음)

---

### 2. 정확성 (Accuracy)

**평가 포인트**:
- 숫자와 통계가 정확한가?
- 인용이 정확한가?
- 맥락이 왜곡되지 않았는가?

**체크리스트**:
- [ ] 통계 수치의 출처 명시
- [ ] 인용 부호 내용이 원문과 일치
- [ ] 비교 대상이 적절함 (사과 vs 사과)

**문제 사례**:
- "작년 대비 10배 증가" (기준 수치가 너무 작아 왜곡)
- "전문가는 '위험하다'고 말했다" (맥락 생략으로 의미 왜곡)

---

### 3. 공정성 (Fairness)

**평가 포인트**:
- 다양한 관점을 균형 있게 다루는가?
- 특정 입장에 편향되지 않았는가?
- 반론 기회를 제공했는가?

**체크리스트**:
- [ ] 양측 입장을 모두 소개
- [ ] 비판 대상에게 해명 기회 제공
- [ ] 균형 잡힌 분량 할애

---

### 4. 투명성 (Transparency)

**평가 포인트**:
- 정보 출처가 명확한가?
- 이해관계를 공개했는가?
- 취재 방법을 설명했는가?

**체크리스트**:
- [ ] "~에 따르면" 출처 명시
- [ ] 광고/협찬인 경우 명시
- [ ] 익명 출처 사용 시 이유 설명

---

### 5. 맥락 (Context)

**평가 포인트**:
- 배경 정보를 충분히 제공하는가?
- 역사적/사회적 맥락을 고려하는가?
- 결과와 영향을 설명하는가?

**체크리스트**:
- [ ] 사건의 배경 설명
- [ ] 이전 경과 요약
- [ ] 예상 영향 분석

---

### 6. 인권 존중 (Human Rights)

**평가 포인트**:
- 인권을 침해하지 않는가?
- 취약 집단을 존중하는가?
- 차별적 표현이 없는가?

**체크리스트**:
- [ ] 범죄 피해자 신원 보호
- [ ] 장애/성소수자 등 존중 표현
- [ ] 선정적 표현 자제

---

### 7. 책임성 (Accountability)

**평가 포인트**:
- 오류 정정 절차가 있는가?
- 피해 구제 방안을 제시하는가?
- 기자/매체 정보가 명확한가?

**체크리스트**:
- [ ] 기자명 표시
- [ ] 정정 요청 방법 안내
- [ ] 문의처 제공

---

### 8. 독립성 (Independence)

**평가 포인트**:
- 외부 압력으로부터 자유로운가?
- 광고주/후원자의 영향이 없는가?
- 정치적 독립성을 유지하는가?

**체크리스트**:
- [ ] 이해관계 공개
- [ ] 광고와 기사 구분
- [ ] 정치적 중립 유지

---

## 템플릿 생성 가이드

각 기사 유형별 템플릿 작성 시 다음 구조 권장:

```markdown
# [기사 유형] 평가 템플릿

## 1단계: 기본 정보 수집
- 기사 제목:
- 언론사:
- 작성일:
- 기자명:

## 2단계: 8차원 평가

### 진실성
[체크리스트 항목]

### 정확성
[체크리스트 항목]

...

## 3단계: 종합 평가
- 주요 강점:
- 개선 필요 사항:
- 전체 평가:
```

---

## 기사 유형별 중점 차원

| 기사 유형 | 중점 평가 차원 |
|----------|--------------|
| **스트레이트 뉴스** | 진실성, 정확성, 투명성 |
| **해설/분석** | 공정성, 맥락, 독립성 |
| **인터뷰** | 공정성, 투명성, 인권 존중 |
| **사설/칼럼** | 논리성, 독립성, 책임성 |
| **탐사 보도** | 진실성, 정확성, 투명성, 책임성 |

---

## 활용 예시

### 예시 1: 스트레이트 뉴스 템플릿 생성 요청
```
CR 평가 기준 Skill을 활용하여 
스트레이트 뉴스용 Claude Sonnet 4 평가 템플릿을 작성해주세요.

중점:
- 진실성, 정확성, 투명성 차원 강화
- 체크리스트 형식
- 각 항목당 3-5개 질문
```

### 예시 2: 해설 기사 템플릿 생성 요청
```
CR 평가 기준 Skill을 참조하여
해설 기사용 ChatGPT-4o 평가 템플릿을 만들어주세요.

중점:
- 공정성, 맥락, 독립성
- 다양한 관점 균형 체크
- 논리 전개 평가
```
```

#### Step 2: .ZIP 파일 생성

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

#### 주의사항

- [ ] **Pro/Max 플랜 필요**: 무료 사용자는 Skills 사용 불가
- [ ] **Code Execution 활성화**: Skills는 컴퓨터 사용 기능이 필요
- [ ] **Skill 이름 명시**: 프롬프트에서 정확한 Skill 이름 언급
- [ ] **재업로드 시**: 기존 Skill 비활성화 → 삭제 → 새로 업로드

#### 문제 해결

**Q: Skill이 적용되지 않는 것 같아요**
```
A: 프롬프트에서 명시적으로 언급하세요:
"CR 평가 기준 Skill의 [섹션명]을 참조하여..."
```

**Q: Skill 업로드가 실패해요**
```
A: 체크 사항:
- SKILL.md 파일이 루트에 있는지 확인
- 파일 크기가 10MB 이하인지 확인
- Code Execution이 활성화되었는지 확인
```

**Q: 여러 Skill을 동시에 사용할 수 있나요?**
```
A: 네, 프롬프트에서 모두 언급하면 됩니다:
"CR 평가 기준 Skill과 도메인 전문가 Skill을 활용하여..."
```

---

### Skills vs 역할 정의 비교

| 구분 | claude.md 역할 정의 | Skills (.ZIP 업로드) |
|------|-------------------|---------------------|
| **용도** | 워크플로우, 코드 표준 | 도메인 지식, 데이터 |
| **크기** | 작음 (< 100KB) | 클 수 있음 (< 10MB) |
| **업데이트** | GitHub으로 버전 관리 | 재업로드 필요 |
| **적합 사례** | 개발 역할, 리뷰 기준 | 평가 기준, 참조 문서 |

**권장 조합**:
- `claude.md`: Backend/Frontend Developer, Code Reviewer 역할
- `Skills`: CR 평가 기준, 언론사별 HTML 구조, 기사 샘플 등
```

---

### 4.3 Section 4.4 추가: 웹 버전 환경 관리 (🟢 P2 추가)

```markdown
### 4.4 환경 관리 전략 (웹 버전 전용)

웹 버전 Claude Code의 **Environment 관리 기능**을 활용하여 개발/테스트/배포 환경을 분리합니다.

#### 환경 분리 전략

**1. 개발 환경 (Default)**
- **목적**: 일반적인 기능 개발
- **설정**: 
  - Python 3.10+, Node.js 18+ (자동 제공)
  - 빠른 반복 개발
- **사용 시점**: 
  - 새로운 기능 프로토타이핑
  - 코드 실험
  - 빠른 테스트

**2. 백엔드 환경 (backend-dev)**
- **목적**: 백엔드 집중 개발
- **설정**:
  - FastAPI, BeautifulSoup4, Anthropic SDK 설치
  - API 서버 실행 환경
- **사용 시점**:
  - API 엔드포인트 개발
  - 스크래핑 로직 구현
  - Claude API 통합

**3. 프론트엔드 환경 (frontend-dev)**
- **목적**: 프론트엔드 집중 개발
- **설정**:
  - Next.js 14, TypeScript, TailwindCSS
  - 개발 서버 실행
- **사용 시점**:
  - UI 컴포넌트 개발
  - 페이지 라우팅 구현
  - 스타일링 작업

**4. 테스트 환경 (testing)**
- **목적**: 통합 테스트 및 에러 시나리오 검증
- **설정**:
  - pytest, Jest 설치
  - Mock 데이터 준비
- **사용 시점**:
  - 전체 플로우 테스트
  - 에러 처리 검증
  - 성능 테스트

**5. 배포 준비 환경 (pre-production)**
- **목적**: 배포 전 최종 확인
- **설정**:
  - 프로덕션 설정 적용
  - 환경 변수 검증
- **사용 시점**:
  - 최종 검증
  - 프로덕션 빌드 테스트
  - 배포 전 체크리스트 확인

#### 환경 전환 워크플로우

**시나리오 1: 백엔드 → 프론트엔드 순차 개발**
```
1. "backend-dev" 환경 선택
2. API 엔드포인트 개발
3. PR 생성: feature/api-scraper
4. "frontend-dev" 환경으로 전환
5. API 연동 UI 개발
6. PR 생성: feature/ui-scraper
```

**시나리오 2: 병렬 개발 (환경 분리)**
```
세션 1: "backend-dev" 환경
- 템플릿 매핑 시스템 구현
- 작업 완료 후 PR 생성

세션 2: "frontend-dev" 환경 (새 탭/창)
- 다운로드 페이지 구현
- 작업 완료 후 PR 생성

두 작업이 독립적이므로 동시 진행 가능
```

**시나리오 3: 테스트 → 배포**
```
1. "testing" 환경에서 통합 테스트
2. 모든 테스트 통과 확인
3. "pre-production" 환경으로 전환
4. 프로덕션 빌드 검증
5. main 브랜치 PR 생성 → 자동 배포
```

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

#### 환경 관리 장점

| 장점 | 설명 |
|------|------|
| **격리성** | 각 환경이 독립된 VM이므로 충돌 없음 |
| **재현성** | 동일한 설정으로 일관된 환경 유지 |
| **안전성** | 실험이 다른 환경에 영향 주지 않음 |
| **속도** | 환경 전환이 빠름 (수 초) |
| **클린업** | 환경 삭제로 완전 초기화 가능 |

#### 주의사항

- [ ] **환경별 의존성 관리**: 각 환경에서 필요한 패키지 설치 필요
- [ ] **환경 변수**: .env 파일을 각 환경에 별도로 설정
- [ ] **Git 동기화**: 모든 환경이 같은 GitHub 저장소 연결됨
- [ ] **세션 지속**: 브라우저 탭을 닫아도 환경은 유지됨 (일정 시간)
- [ ] **리소스 제한**: 동시에 너무 많은 환경 생성 시 성능 저하 가능
```

---

### 4.4 Section 4.5 추가: 자동 PR 워크플로우 (🟢 P2 추가)

```markdown
### 4.5 자동 PR 생성 워크플로우 (웹 버전 강점)

웹 버전의 **자동 PR 생성 기능**을 활용하여 Git 워크플로우를 간소화합니다.

#### 기본 워크플로우

**1. 기능 개발 시작**
```
1. Claude Code 웹 접속
2. GitHub 저장소 선택: gamnamu/prompt-template-hub
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

**4. PR 내용 확인**
```
GitHub PR 자동 생성 예시:

제목: Implement article scraper for major Korean news sites

설명:
## Changes
- Added `backend/scraper.py` with support for 3 major news sites
- Implemented error handling for 404, timeout, and paywall scenarios
- Added type hints and docstrings

## Testing
- Manual testing with sample URLs
- Error cases validated

## Next Steps
- Add unit tests
- Expand to more news sites
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

**예시**:
```
feature/article-classifier
fix/scraper-timeout-error
refactor/api-error-handling
docs/api-documentation
test/scraper-integration
```

#### 주간 개발 흐름 예시

**Week 2: Classification & API**

```
월요일:
- backend-dev 환경
- classifier.py 구현
- PR: feature/article-classifier

화요일:
- backend-dev 환경
- main.py API 엔드포인트 추가
- PR: feature/classification-api

수요일:
- testing 환경
- 통합 테스트 작성
- PR: test/classification-integration

목요일-금요일:
- Code Review 진행
- PR 머지
- main 브랜치 자동 배포
```

#### PR 템플릿 커스터마이징

**claude.md에 PR 가이드라인 추가**:
```markdown
## PR 생성 가이드

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
```

**프롬프트에서 활용**:
```
"claude.md의 'PR 생성 가이드'를 참조하여
현재 작업에 대한 PR을 생성해주세요."
```

#### 협업 시나리오

**시나리오 1: 리뷰 요청**
```
1. PR 생성 (자동)
2. GitHub에서 리뷰어 지정
3. 피드백 받기
4. 웹에서 수정 사항 반영
5. 자동으로 PR 업데이트
```

**시나리오 2: 충돌 해결**
```
1. main 브랜치와 충돌 발생
2. 웹 환경에서 main 브랜치 pull
3. 충돌 해결
4. PR 업데이트 (자동)
```

#### 장점 정리

| 전통적 방식 | 웹 버전 자동 PR |
|------------|----------------|
| `git add .` | 클릭 한 번 |
| `git commit -m "..."` | 자동 생성 |
| `git push` | 자동 실행 |
| GitHub에서 PR 수동 생성 | 자동 생성 |
| PR 제목/설명 작성 | AI가 자동 작성 |

**시간 절약**: 개발자가 Git 명령어 대신 **코딩에만 집중** 가능

#### 주의사항

- [ ] **브랜치 이름**: 팀 규칙에 맞게 수정 후 PR 생성
- [ ] **PR 설명**: 자동 생성된 내용 확인 및 보완
- [ ] **리뷰어 지정**: GitHub에서 수동으로 지정 필요
- [ ] **머지 권한**: 저장소 권한 설정 확인
- [ ] **CI/CD 연동**: PR 생성 시 자동 테스트 실행 설정 권장
```

---

### 4.5 부록 C: 주요 명령어 모음 (🟡 P1 수정)

#### 원본 내용
```markdown
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

#### 문제점
- 로컬 명령어 기준
- 웹 VM 환경 차이 미반영

#### 수정 내용

```markdown
### C. 주요 명령어 모음 (웹 버전)

#### 개발 서버 실행

**Backend (FastAPI)**:
```bash
# 웹 VM 터미널에서
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 백그라운드 실행 (선택)
nohup python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
```

**Frontend (Next.js)**:
```bash
# 새 터미널 탭/창에서
cd frontend
npm run dev

# 또는 포트 지정
npm run dev -- --port 3000
```

**주의사항**:
- 웹 VM에서는 `localhost` 직접 접근이 제한적
- **권장**: Vercel Preview 또는 Railway 스테이징 환경에서 테스트
- **대안**: 데스크톱 앱에서 로컬 테스트 후 웹에서 배포

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

# 특정 패키지
npm install next react react-dom
```

**중요**: 웹 버전에서는 `--break-system-packages` 플래그 필수 (pip)

#### 테스트 실행

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

#### 린트 및 포맷

**Backend (Python)**:
```bash
# Black 포매터
pip install black pylint --break-system-packages
black backend/

# Pylint
pylint backend/ --rcfile=.pylintrc
```

**Frontend (TypeScript)**:
```bash
cd frontend

# ESLint
npm run lint

# Prettier
npm run format

# 자동 수정
npm run lint -- --fix
```

#### 환경 변수 설정

**Backend (.env 파일)**:
```bash
# .env 파일 생성
cat > backend/.env <<EOF
ANTHROPIC_API_KEY=your_api_key_here
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
LOG_LEVEL=INFO
EOF

# 확인
cat backend/.env
```

**Frontend (.env.local)**:
```bash
# .env.local 파일 생성
cat > frontend/.env.local <<EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GA_ID=your_ga_id
EOF

# 확인
cat frontend/.env.local
```

#### 배포

**Frontend (Vercel)**:
```bash
# Vercel CLI 설치
npm install -g vercel

# 로그인
vercel login

# 배포
cd frontend
vercel --prod
```

**Backend (Railway)**:
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 배포
cd backend
railway up
```

**주의사항**:
- 웹 버전에서는 글로벌 npm 패키지 설치 가능
- 하지만 권장: GitHub Actions로 CI/CD 자동화

#### 프로젝트 초기화 (첫 실행 시)

```bash
# 저장소 구조 확인
ls -la

# Backend 초기화
cd backend
pip install -r requirements.txt --break-system-packages
python -c "import fastapi; print('Backend ready')"

# Frontend 초기화
cd ../frontend
npm install
npm run build
echo "Frontend ready"

# 전체 프로젝트 준비 완료
cd ..
echo "Project initialized"
```

#### Git 작업 (웹 버전에서는 자동)

**참고**: 웹 버전에서는 PR 생성 버튼으로 자동화되지만,
필요시 수동으로도 가능:

```bash
# 현재 브랜치 확인
git branch

# 변경사항 확인
git status

# 스테이징
git add .

# 커밋
git commit -m "feat: implement article scraper"

# 푸시
git push origin feature/article-scraper
```

**권장**: 웹 UI의 "PR 생성" 버튼 사용 (자동화됨)

#### 로그 확인

**Backend 로그**:
```bash
# 실시간 로그
tail -f backend/app.log

# 에러만 필터
tail -f backend/app.log | grep ERROR
```

**Frontend 로그**:
```bash
# 빌드 로그
npm run build 2>&1 | tee build.log

# 개발 서버 로그
npm run dev 2>&1 | tee dev.log
```

#### 문제 해결 명령어

**포트 사용 중 에러**:
```bash
# 포트 8000 사용 프로세스 찾기
lsof -i :8000

# 프로세스 종료
kill -9 [PID]
```

**캐시 정리**:
```bash
# Python 캐시
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Node 캐시
cd frontend
rm -rf node_modules .next
npm install
```

**의존성 재설치**:
```bash
# Backend
pip uninstall -y -r requirements.txt
pip install -r requirements.txt --break-system-packages

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```
```

---

## 5. 추가 활용 전략

### 5.1 웹 버전 고유 기능 최대 활용

#### 환경 분리 활용

**병렬 개발 전략**:
```
탭 1: backend-dev 환경
- API 엔드포인트 개발
- 백그라운드 서버 실행

탭 2: frontend-dev 환경  
- UI 컴포넌트 개발
- API 연동 테스트

각 탭에서 독립적으로 PR 생성 가능
```

#### 모바일 접근 활용

**이동 중 작업 예시**:
```
시나리오: 출퇴근 중 코드 리뷰

1. iOS Claude 앱 실행
2. PR 알림 확인
3. 변경사항 검토
4. 간단한 수정사항 반영
5. PR 승인 또는 코멘트

→ 데스크톱 없이도 프로젝트 진행 가능
```

### 5.2 하이브리드 접근 (웹 + 데스크톱)

**최적 워크플로우**:
```
주 개발: 웹 버전
- 빠른 개발 및 PR 생성
- 환경 분리로 병렬 작업
- GitHub 통합 활용

로컬 테스트: 데스크톱 앱
- http://localhost:3000 직접 접근
- 로컬 파일 시스템 작업
- MCP 서버 연결 (필요시)

배포: 웹 버전
- PR 머지 후 자동 배포
- Vercel/Railway 연동
```

### 5.3 팀 협업 전략

**PR 기반 협업**:
```
1. 각 팀원이 웹에서 작업
2. 기능 완성 시 PR 생성 (자동)
3. GitHub에서 리뷰
4. 웹에서 피드백 반영
5. PR 머지 → 자동 배포

장점:
- Git 명령어 불필요
- 일관된 PR 포맷
- 빠른 반복 주기
```

---

## 6. 수정된 개발 로드맵

### 6.1 Week 1: Foundation (웹 버전)

#### Day 1: 초기 설정

**환경 준비**:
```
체크리스트:
- [ ] Claude.ai Pro 또는 Max 플랜 가입
- [ ] Code Execution 기능 활성화
- [ ] GitHub 저장소 생성: gamnamu/prompt-template-hub
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

2. 개발 역할 정의 (SubAgent 대체)
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

**테스트**:
```
프롬프트:
"backend/scraper.py를 테스트하기 위한 
간단한 테스트 스크립트를 작성해주세요.

테스트 케이스:
1. 정상 URL
2. 404 에러
3. Timeout
4. 각 언론사별 샘플 URL"
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

#### 통합 테스트

```
[Backend Developer 역할]

전체 플로우 테스트:
1. URL 입력
2. 스크래핑
3. 분류
4. 결과 반환

테스트 스크립트 작성
```

#### PR 생성

```
PR 1: feature/article-classifier
PR 2: feature/fastapi-endpoints
PR 3: test/backend-integration
```

### 6.3 Week 3: Frontend Development (웹 버전)

#### 환경 전환

```
새 환경 생성: "frontend-dev"
또는
기존 환경에서 프론트엔드 작업
```

#### UI 개발

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

#### 각 페이지별 PR 생성

```
PR 1: feature/url-input-page
PR 2: feature/analysis-page
PR 3: feature/download-page
```

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

#### PR 생성

```
동시에 2개 PR 생성:
PR 1: feature/template-mapping
PR 2: feature/ui-enhancements
```

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

#### PR 생성

```
PR 1: refactor/code-quality-improvements
PR 2: feature/evaluation-templates
```

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

---

## 7. 실전 체크리스트

### 7.1 Week 1 시작 전

```
초기 설정:
- [ ] Claude.ai Pro/Max 플랜 가입
- [ ] Code Execution 기능 활성화
- [ ] GitHub 계정 및 저장소 준비
- [ ] Claude API 키 발급
- [ ] 이 가이드 문서 전체 읽기
```

### 7.2 Week 1-2 (Foundation)

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
- [ ] API 엔드포인트 2개 완성
- [ ] Think→Implement→Review 워크플로우 5회 이상 사용
```

### 7.3 Week 3 (Frontend Development)

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

### 7.4 Week 4 (Parallel Development)

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

### 7.5 Week 5 (Skills & Quality)

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

### 7.6 Week 6 (Deployment)

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

### 7.7 MVP 출시 전 최종 체크

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

## 8. 마무리

### 8.1 핵심 요약

**웹 버전으로 충분히 구현 가능**:
- ✅ 전체 개발 프로세스
- ✅ GitHub 연동 및 자동 PR
- ✅ 환경 분리 및 병렬 작업
- ✅ Skills 활용
- ✅ 배포 자동화

**주요 수정 사항**:
- ⚠️ SubAgent → claude.md 역할 통합
- ⚠️ Skills 디렉토리 → ZIP 업로드
- ⚠️ 로컬 명령어 → 웹 VM 명령어

### 8.2 웹 버전 장점 활용

1. **자동 PR 생성**: Git 명령어 불필요
2. **환경 분리**: 병렬 개발 용이
3. **모바일 접근**: 이동 중에도 작업 가능
4. **클라우드 VM**: 일관된 개발 환경

### 8.3 다음 단계

이 가이드를 바탕으로:
1. 원본 설계서 수정
2. Week 1부터 웹 버전으로 개발 시작
3. 각 단계별 체크리스트 활용
4. 문제 발생 시 이 문서 참조

### 8.4 지원

- 원본 설계서: `CR_PTH__통합_최적_전략_CC.md`
- 이 가이드: `claude-code-web-version-implementation-guide.md`
- GitHub: `gamnamu/prompt-template-hub`

---

**문서 버전**: 1.0  
**작성일**: 2025-11-14  
**작성자**: CR Project Team  
**목적**: 웹 버전 Claude Code 구현 가이드

**라이선스**: CR 프로젝트 내부 사용
