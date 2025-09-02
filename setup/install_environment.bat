@echo off
chcp 65001 >nul
echo ========================================
echo    제주 LLM 실습환경 자동 설정
echo ========================================
echo.

echo [1/5] Python 가상환경 생성 중...
if exist "venv" (
    echo 기존 가상환경을 제거합니다...
    rmdir /s /q "venv" 2>nul
)
python -m venv venv
if errorlevel 1 (
    echo 오류: Python이 설치되지 않았습니다.
    echo Python 3.10 이상을 설치해주세요.
    pause
    exit /b 1
)
echo ✓ 가상환경 생성 완료

echo.
echo [2/5] 가상환경 활성화 중...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo 오류: 가상환경 활성화에 실패했습니다.
    pause
    exit /b 1
)
echo ✓ 가상환경 활성화 완료

echo.
echo [3/5] 필요한 패키지 설치 중...
python -m pip install --upgrade pip
pip install -r setup\requirements.txt
if errorlevel 1 (
    echo 오류: 패키지 설치에 실패했습니다.
    pause
    exit /b 1
)
echo ✓ 패키지 설치 완료

echo.
echo [3.5/5] 추가 금융 데이터 패키지 설치 중...
pip install yfinance
if errorlevel 1 (
    echo 경고: yfinance 설치에 실패했습니다. (계속 진행)
)
echo ✓ 추가 패키지 설치 완료

echo.
echo [4/5] Jupyter 커널 등록 중...
python -m ipykernel install --user --name=jeju-llm-venv --display-name="Jeju LLM (Python 3.10)"
if errorlevel 1 (
    echo 오류: Jupyter 커널 등록에 실패했습니다.
    pause
    exit /b 1
)
echo ✓ Jupyter 커널 등록 완료

echo.
echo [5/5] 환경 설정 완료!
echo.
echo ========================================
echo    설정이 완료되었습니다!
echo ========================================
echo.
echo 사용 방법:
echo 1. VS Code에서 Jupyter 노트북(.ipynb) 열기
echo 2. 우측 상단 커널 선택에서 "Jeju LLM (Python 3.10)" 선택
echo 3. 실습 시작!
echo.
echo 주의사항:
echo - 이 배치 파일은 한 번만 실행하면 됩니다
echo - VS Code에서 Jupyter 확장 프로그램이 필요합니다
echo.
pause
