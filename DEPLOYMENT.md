# 배포 가이드 (Deployment Guide)

CR Template Hub 프로젝트를 프로덕션 환경에 배포하기 위한 단계별 가이드입니다.

## 목차

- [개요](#개요)
- [배포 아키텍처](#배포-아키텍처)
- [백엔드 배포 (Railway)](#백엔드-배포-railway)
- [프론트엔드 배포 (Vercel)](#프론트엔드-배포-vercel)
- [환경 변수 설정](#환경-변수-설정)
- [배포 후 확인](#배포-후-확인)
- [문제 해결](#문제-해결)

---

## 개요

이 프로젝트는 다음과 같은 구조로 배포됩니다:

- **백엔드 (FastAPI)**: Railway에 배포
- **프론트엔드 (Next.js)**: Vercel에 배포

### 필수 요구사항

- GitHub 계정
- Railway 계정 ([railway.app](https://railway.app))
- Vercel 계정 ([vercel.com](https://vercel.com))
- Anthropic API 키 ([console.anthropic.com](https://console.anthropic.com))

---

## 배포 아키텍처

```
┌─────────────────┐
│   사용자 브라우저   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   Vercel (Frontend)     │
│   - Next.js             │
│   - React               │
│   - Tailwind CSS        │
└────────┬────────────────┘
         │ HTTP/HTTPS
         ▼
┌─────────────────────────┐
│   Railway (Backend)     │
│   - FastAPI             │
│   - Uvicorn             │
│   - Scraper Module      │
│   - Claude API          │
└─────────────────────────┘
```

---

## 백엔드 배포 (Railway)

### 1. Railway 프로젝트 생성

1. [Railway 대시보드](https://railway.app/dashboard)에 로그인
2. "New Project" 클릭
3. "Deploy from GitHub repo" 선택
4. 이 저장소(`prompt-template-hub`) 선택
5. "Deploy Now" 클릭

### 2. 서비스 설정

1. 배포된 서비스 클릭
2. **Settings** 탭으로 이동
3. 다음 설정 확인:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path**: `/health`

### 3. 환경 변수 설정

**Variables** 탭에서 다음 환경 변수를 추가:

```bash
# 필수
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# 선택 (기본값 사용 가능)
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:3000

# 스크래핑 설정
SCRAPING_TIMEOUT=10
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
```

**중요:**
- `ANTHROPIC_API_KEY`: Anthropic Console에서 발급받은 실제 API 키
- `ALLOWED_ORIGINS`: 프론트엔드 Vercel URL로 업데이트 (CORS 설정)

### 4. 배포 확인

1. Railway가 자동으로 빌드 및 배포 시작
2. **Deployments** 탭에서 진행 상황 확인
3. 배포 완료 후 **Settings** > **Networking**에서 도메인 확인
   - 예: `https://your-backend-app.railway.app`
4. 헬스체크 확인:
   ```bash
   curl https://your-backend-app.railway.app/health
   ```
   응답 예시:
   ```json
   {
     "status": "healthy",
     "service": "CR Template Hub API",
     "version": "1.0.0"
   }
   ```

### 5. API 문서 확인

배포된 백엔드의 API 문서:
- **Swagger UI**: `https://your-backend-app.railway.app/docs`
- **ReDoc**: `https://your-backend-app.railway.app/redoc`

---

## 프론트엔드 배포 (Vercel)

### 1. Vercel 프로젝트 생성

1. [Vercel 대시보드](https://vercel.com/dashboard)에 로그인
2. "Add New..." > "Project" 클릭
3. GitHub 저장소 `prompt-template-hub` 선택
4. "Import" 클릭

### 2. 프로젝트 설정

**Configure Project** 화면에서:

1. **Framework Preset**: Next.js (자동 감지됨)
2. **Root Directory**: `frontend`
3. **Build and Output Settings** (기본값 사용):
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

### 3. 환경 변수 설정

**Environment Variables** 섹션에서 추가:

```bash
NEXT_PUBLIC_API_URL=https://your-backend-app.railway.app
```

**중요:**
- Railway 백엔드 URL로 정확히 설정
- `https://` 프로토콜 포함
- 마지막에 슬래시(`/`) 없이 입력

### 4. 배포 시작

1. "Deploy" 버튼 클릭
2. Vercel이 자동으로 빌드 및 배포 시작
3. 진행 상황은 대시보드에서 실시간 확인 가능

### 5. 배포 확인

1. 배포 완료 후 Vercel이 자동으로 도메인 할당
   - 예: `https://prompt-template-hub.vercel.app`
2. 브라우저에서 접속하여 동작 확인
3. 기사 URL 입력 → 스크래핑 → 평가 전체 플로우 테스트

### 6. 커스텀 도메인 설정 (선택)

1. Vercel 프로젝트 **Settings** > **Domains** 이동
2. "Add" 버튼 클릭
3. 원하는 도메인 입력
4. DNS 레코드 설정 안내에 따라 도메인 등록 서비스에서 설정

---

## 환경 변수 설정

### 백엔드 (Railway)

| 변수명 | 필수 여부 | 설명 | 예시 값 |
|--------|----------|------|---------|
| `ANTHROPIC_API_KEY` | ✅ 필수 | Claude API 키 | `sk-ant-xxxxx` |
| `ALLOWED_ORIGINS` | ⚠️ 권장 | CORS 허용 도메인 | `https://your-app.vercel.app` |
| `HOST` | 선택 | 서버 호스트 | `0.0.0.0` (기본값) |
| `PORT` | 선택 | 서버 포트 | Railway 자동 설정 |
| `LOG_LEVEL` | 선택 | 로그 레벨 | `INFO` (기본값) |
| `SCRAPING_TIMEOUT` | 선택 | 스크래핑 타임아웃 | `10` (기본값) |
| `USER_AGENT` | 선택 | HTTP User-Agent | Mozilla/5.0... |

### 프론트엔드 (Vercel)

| 변수명 | 필수 여부 | 설명 | 예시 값 |
|--------|----------|------|---------|
| `NEXT_PUBLIC_API_URL` | ✅ 필수 | 백엔드 API URL | `https://your-backend.railway.app` |

---

## 배포 후 확인

### 체크리스트

- [ ] **백엔드 헬스체크 통과**
  ```bash
  curl https://your-backend-app.railway.app/health
  ```

- [ ] **백엔드 API 문서 접근 가능**
  - Swagger UI: `https://your-backend-app.railway.app/docs`

- [ ] **프론트엔드 페이지 로드**
  - `https://your-frontend.vercel.app`

- [ ] **전체 플로우 테스트**
  1. 기사 URL 입력 (예: 네이버 뉴스)
  2. "평가하기" 버튼 클릭
  3. 스크래핑 결과 표시 확인
  4. AI 평가 결과 표시 확인

- [ ] **CORS 설정 확인**
  - 프론트엔드에서 백엔드 API 호출 시 오류 없음

- [ ] **에러 처리 확인**
  - 잘못된 URL 입력 시 에러 메시지 표시
  - API 키 없이 평가 요청 시 적절한 에러

---

## 문제 해결

### 백엔드 문제

#### 1. 502 Bad Gateway

**원인**: 서버가 시작되지 않음

**해결방법**:
1. Railway 로그 확인:
   - Deployments 탭 > 최신 배포 클릭 > View Logs
2. 환경 변수 확인:
   - `ANTHROPIC_API_KEY` 설정 여부
3. 의존성 설치 확인:
   - `requirements.txt` 파일 존재 여부

#### 2. CORS 오류

**증상**:
```
Access to fetch at 'https://backend.railway.app/scrape' from origin 'https://frontend.vercel.app'
has been blocked by CORS policy
```

**해결방법**:
1. Railway 환경 변수에서 `ALLOWED_ORIGINS` 확인
2. 프론트엔드 Vercel URL 정확히 포함되어 있는지 확인
3. 예시:
   ```
   ALLOWED_ORIGINS=https://your-app.vercel.app,http://localhost:3000
   ```

#### 3. API 키 오류

**증상**: `/evaluate` 엔드포인트에서 400 에러

**해결방법**:
1. Railway Variables 탭에서 `ANTHROPIC_API_KEY` 확인
2. API 키가 유효한지 [Anthropic Console](https://console.anthropic.com) 에서 확인
3. API 키 형식: `sk-ant-` 로 시작

### 프론트엔드 문제

#### 1. API 호출 실패

**원인**: `NEXT_PUBLIC_API_URL` 잘못 설정

**해결방법**:
1. Vercel 프로젝트 **Settings** > **Environment Variables** 확인
2. Railway 백엔드 URL 정확히 입력되어 있는지 확인
3. 변경 후 재배포:
   - Vercel Deployments 탭 > 최신 배포 > "Redeploy"

#### 2. 빌드 실패

**원인**: TypeScript 에러 또는 의존성 문제

**해결방법**:
1. Vercel 빌드 로그 확인
2. 로컬에서 빌드 테스트:
   ```bash
   cd frontend
   npm install
   npm run build
   ```
3. 에러 해결 후 다시 배포

#### 3. 환경 변수 미적용

**해결방법**:
1. Vercel에서 환경 변수 변경 후 **반드시 재배포** 필요
2. Deployments 탭 > "Redeploy" 클릭

---

## 배포 업데이트

코드 변경 후 배포 업데이트 방법:

### 자동 배포 (권장)

1. GitHub에 코드 Push:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```

2. Railway와 Vercel이 자동으로 감지하여 재배포

### 수동 배포

**Railway:**
1. 대시보드 > 프로젝트 선택
2. Deployments 탭 > "Deploy" 클릭

**Vercel:**
1. 대시보드 > 프로젝트 선택
2. Deployments 탭 > "Redeploy" 클릭

---

## 모니터링

### Railway 로그 확인

```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 연결
railway link

# 실시간 로그 확인
railway logs
```

### Vercel 로그 확인

1. Vercel 대시보드 > 프로젝트 선택
2. "Functions" 탭에서 서버사이드 함수 로그 확인
3. "Runtime Logs" 탭에서 실시간 로그 확인

---

## 보안 권장사항

1. **API 키 보호**
   - 절대 GitHub에 커밋하지 마세요
   - 환경 변수로만 관리

2. **CORS 설정**
   - 프로덕션 도메인만 허용
   - 와일드카드(`*`) 사용 금지

3. **HTTPS 사용**
   - Railway와 Vercel 모두 자동으로 HTTPS 제공
   - 커스텀 도메인도 무료 SSL 인증서 제공

4. **환경별 설정 분리**
   - 개발: localhost
   - 스테이징: staging.vercel.app
   - 프로덕션: 커스텀 도메인

---

## 비용

### Railway

- **Free Tier**: $5 무료 크레딧/월
- **Pro Plan**: $20/월 (사용량 기반)
- [가격 정보](https://railway.app/pricing)

### Vercel

- **Hobby (무료)**: 개인 프로젝트용
- **Pro**: $20/월 (팀 협업용)
- [가격 정보](https://vercel.com/pricing)

### Anthropic API

- **Claude API**: 사용량 기반 과금
- [가격 정보](https://www.anthropic.com/pricing)

---

## 추가 리소스

- [Railway 문서](https://docs.railway.app/)
- [Vercel 문서](https://vercel.com/docs)
- [Next.js 배포 가이드](https://nextjs.org/docs/deployment)
- [FastAPI 배포 가이드](https://fastapi.tiangolo.com/deployment/)

---

## 지원

문제가 발생하면 다음을 확인하세요:

1. 이 문서의 [문제 해결](#문제-해결) 섹션
2. Railway/Vercel 로그
3. GitHub Issues

---

**마지막 업데이트**: 2025-11-15
**작성자**: CR Template Hub Team
