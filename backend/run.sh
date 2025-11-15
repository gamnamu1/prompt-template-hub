#!/bin/bash

# FastAPI 서버 실행 스크립트
# uvicorn을 사용하여 API 서버를 시작합니다.

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== CR Template Hub API 서버 시작 ===${NC}"
echo ""

# .env 파일 확인
if [ ! -f .env ]; then
    echo -e "${YELLOW}Warning: .env 파일이 없습니다. .env.example을 참고하여 생성해주세요.${NC}"
    echo ""
fi

# 가상환경 확인 및 권장
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Note: 가상환경이 활성화되지 않았습니다.${NC}"
    echo -e "${YELLOW}권장: python3 -m venv venv && source venv/bin/activate${NC}"
    echo ""
fi

# 의존성 설치 확인
echo "의존성 확인 중..."
pip install -r requirements.txt --quiet

# 환경 변수 설정 (기본값)
export HOST=${HOST:-"0.0.0.0"}
export PORT=${PORT:-"8000"}
export LOG_LEVEL=${LOG_LEVEL:-"info"}

echo -e "${GREEN}서버 설정:${NC}"
echo "  - Host: $HOST"
echo "  - Port: $PORT"
echo "  - Log Level: $LOG_LEVEL"
echo ""
echo -e "${GREEN}API 문서:${NC}"
echo "  - Swagger UI: http://localhost:$PORT/docs"
echo "  - ReDoc: http://localhost:$PORT/redoc"
echo ""
echo -e "${GREEN}서버 시작 중...${NC}"
echo ""

# uvicorn으로 서버 실행
# --reload: 코드 변경 시 자동 재시작 (개발 모드)
# --host: 바인딩할 호스트
# --port: 바인딩할 포트
# --log-level: 로그 레벨
uvicorn main:app \
    --host "$HOST" \
    --port "$PORT" \
    --reload \
    --log-level "$LOG_LEVEL"
