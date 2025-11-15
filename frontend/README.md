# CR Template Hub - Frontend

한국 주요 언론사 기사 평가 플랫폼의 프론트엔드 애플리케이션입니다.

## 기술 스택

- **Next.js 14** - React 프레임워크 (App Router)
- **TypeScript** - 타입 안전성
- **Tailwind CSS** - 유틸리티 기반 스타일링
- **React 18** - UI 라이브러리

## 주요 기능

- 기사 URL 입력 및 스크래핑 요청
- 실시간 로딩 상태 표시
- 스크래핑 결과 표시 (제목, 본문, 메타데이터)
- 다크 모드 지원
- 반응형 디자인

## 설치 및 실행

### 1. 의존성 설치

```bash
npm install
# 또는
yarn install
```

### 2. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성합니다:

```bash
cp .env.example .env
```

`.env` 파일 내용:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. 개발 서버 실행

```bash
npm run dev
# 또는
yarn dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000)을 열어 확인합니다.

### 4. 프로덕션 빌드

```bash
npm run build
npm run start
```

## 프로젝트 구조

```
frontend/
├── app/
│   ├── globals.css          # 글로벌 스타일
│   ├── layout.tsx           # 루트 레이아웃
│   └── page.tsx             # 메인 페이지
├── components/
│   ├── ArticleForm.tsx      # URL 입력 폼
│   ├── ArticleResult.tsx    # 결과 표시
│   └── LoadingSpinner.tsx   # 로딩 스피너
├── next.config.js           # Next.js 설정
├── tailwind.config.js       # Tailwind CSS 설정
├── tsconfig.json            # TypeScript 설정
└── package.json             # 의존성 관리
```

## 지원 언론사

- 네이버 뉴스 (n.news.naver.com)
- 다음 뉴스 (v.daum.net)
- 연합뉴스 (www.yna.co.kr)
- 조선일보 (www.chosun.com)
- 중앙일보 (www.joongang.co.kr)
- 한겨레 (www.hani.co.kr)
- 한국경제 (www.hankyung.com)

## API 연동

백엔드 API 서버가 실행 중이어야 합니다:

```bash
cd ../backend
./run.sh
```

API 서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.

## 개발 참고사항

- TypeScript strict 모드 사용
- Tailwind CSS를 이용한 유틸리티 기반 스타일링
- 다크 모드 자동 감지 (prefers-color-scheme)
- 접근성(a11y) 고려한 시맨틱 HTML
