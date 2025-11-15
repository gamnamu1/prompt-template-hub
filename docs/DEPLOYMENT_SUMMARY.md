# CR Template Hub - 배포 요약 및 프로젝트 문서

**문서 버전:** 1.0  
**작성일:** 2025년 11월 15일  
**작성자:** Manus AI

---

## 1. 프로젝트 개요

**CR Template Hub**는 한국 주요 언론사 기사를 스크래핑하고, Anthropic의 Claude API를 활용하여 8가지 차원(정확성, 편향성, 완전성 등)에서 기사를 평가하는 웹 애플리케이션입니다. 사용자는 기사 URL을 입력하여 실시간으로 스크래핑 및 AI 평가 결과를 확인할 수 있습니다.

- **목표:** MVP(Minimum Viable Product) 배포 및 기능 검증
- **상태:** 성공적으로 배포 완료 및 정상 작동 확인

## 2. 최종 배포 URL

| 서비스 | URL |
|---|---|
| **프론트엔드 (Vercel)** | `https://cr-prompt-template-hub.vercel.app` |
| **백엔드 (Railway)** | `https://prompt-template-hub-production.up.railway.app` |

## 3. 기술 스택 및 아키텍처

본 프로젝트는 **헤드리스/분리형(Headless/Decoupled) 아키텍처**를 채택하여 프론트엔드와 백엔드를 독립적으로 개발, 배포, 확장할 수 있도록 설계되었습니다.

| 계층 | 기술 | 호스팅 | 역할 |
|---|---|---|---|
| **프론트엔드** | Next.js, React, TypeScript | Vercel | 사용자 인터페이스(UI) 제공, 백엔드 API 호출 |
| **백엔드** | FastAPI, Python | Railway | 기사 스크래핑, Claude API 연동, 데이터 처리 |
| **AI 모델** | Anthropic Claude | Anthropic | 기사 내용 8차원 평가 |
| **소스코드** | Git | GitHub | 버전 관리 및 CI/CD 트리거 |

## 4. 환경 변수 설정

### 4.1. Railway (백엔드)

| 변수명 | 값 | 설명 |
|---|---|---|
| `ANTHROPIC_API_KEY` | `sk-ant-api03-...` (보안) | Claude API 호출을 위한 인증 키 |
| `ALLOWED_ORIGINS` | `https://cr-prompt-template-hub.vercel.app` | CORS 정책에 따라 허용할 프론트엔드 URL |

### 4.2. Vercel (프론트엔드)

| 변수명 | 값 | 설명 |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `https://prompt-template-hub-production.up.railway.app` | 프론트엔드가 호출할 백엔드 API의 주소 |

## 5. 주요 배포 설정

### 5.1. 모노레포(Monorepo) 설정

- **Vercel Root Directory:** `frontend`
- **Railway Root Directory:** `backend`

### 5.2. `vercel.json` 설정

- Vercel UI에서 환경 변수를 설정했으므로, `frontend/vercel.json` 파일의 `env` 섹션은 충돌을 방지하기 위해 삭제되었습니다.

## 6. 트러블슈팅 및 해결 과정 요약

| 문제 상황 | 원인 | 해결 방법 |
|---|---|---|
| **Railway 빌드 실패** | 모노레포 구조에서 Root Directory 미지정 | Railway 설정에서 Root Directory를 `backend`로 지정 |
| **Vercel 빌드 실패 (이름 중복)** | 동일한 프로젝트 이름 존재 | 프로젝트 이름을 `cr-prompt-template-hub`로 변경 |
| **Vercel 빌드 실패 (환경 변수)** | `vercel.json`의 `env` 형식 오류 | `vercel.json`에서 `env` 섹션 삭제 후 Vercel UI에서 재설정 |
| **API 호출 실패 (Failed to fetch)** | CORS 정책 위반 | Railway에 `ALLOWED_ORIGINS` 환경 변수 추가 |
| **API 호출 실패 (404, Method Not Allowed)** | 브라우저 캐시 문제 | 시크릿 모드 또는 강력 새로고침으로 해결 |

---

이 문서는 향후 프로젝트를 다시 시작하거나 다른 환경에서 배포할 때 참고 자료로 활용할 수 있습니다.
