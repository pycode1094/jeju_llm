@echo off
chcp 65001 >nul
echo ========================================
echo    제주 LLM 실습환경 자동 설정
echo ========================================
echo.

echo [1/5] Python 가상환경 확인 중...
if exist "venv" (
    echo ✓ 기존 가상환경이 존재합니다. 건너뜁니다.
) else (
    echo 가상환경을 생성합니다...
    echo Python 경로 확인 중...
    python --version
    if errorlevel 1 (
        echo 오류: Python이 설치되지 않았거나 PATH에 등록되지 않았습니다.
        echo Python 3.10 이상을 설치하고 PATH에 등록해주세요.
        pause
        exit /b 1
    )
    python -m venv venv
    if errorlevel 1 (
        echo 오류: 가상환경 생성에 실패했습니다.
        echo Python이 올바르게 설치되었는지 확인해주세요.
        pause
        exit /b 1
    )
    echo ✓ 가상환경 생성 완료
)

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
echo pip 업그레이드 완료
pip install -r setup\requirements.txt --upgrade
if errorlevel 1 (
    echo 경고: 일부 패키지 설치에 실패했습니다. (계속 진행)
) else (
    echo ✓ 패키지 설치 완료
)

echo.
echo [3.5/5] 추가 금융 데이터 패키지 설치 중...
pip install yfinance
if errorlevel 1 (
    echo 경고: yfinance 설치에 실패했습니다. (계속 진행)
)
echo ✓ 추가 패키지 설치 완료

echo.
echo [4/5] Jupyter 커널 등록 중...
python -m ipykernel install --user --name=jeju-llm-venv --display-name="Jeju LLM (Python 3.10)" --force
if errorlevel 1 (
    echo 경고: Jupyter 커널 등록에 실패했습니다. (계속 진행)
) else (
    echo ✓ Jupyter 커널 등록 완료
)

echo.
echo [4.5/5] VSCode용 Python 인터프리터 설정...
echo VSCode에서 다음 경로를 Python 인터프리터로 선택하세요:
echo %CD%\venv\Scripts\python.exe
echo.

echo.
echo [5/5] 환경 설정 완료!
echo.
echo ========================================
echo    설정이 완료되었습니다!
echo ========================================
echo.
echo 사용 방법:
echo 1. VS Code에서 Jupyter 확장 프로그램 설치 (Ctrl+Shift+X)
echo 2. VS Code에서 Python 인터프리터 선택 (Ctrl+Shift+P → "Python: Select Interpreter")
echo 3. 위에 표시된 경로의 python.exe 선택
echo 4. Jupyter 노트북(.ipynb) 열기
echo 5. 우측 상단 커널 선택에서 "Jeju LLM (Python 3.10)" 선택
echo 6. 실습 시작!
echo.
echo 주의사항:
echo - 이 배치 파일은 여러 번 실행해도 안전합니다 (기존 설정 유지)
echo - VS Code에서 Jupyter 확장 프로그램이 필요합니다
echo - 이미 설치된 패키지들은 건너뛰고 필요한 것만 업데이트합니다
echo - Python 3.10 이상이 시스템에 설치되어 있어야 합니다
echo - Python이 PATH 환경변수에 등록되어 있어야 합니다
echo.
pause
