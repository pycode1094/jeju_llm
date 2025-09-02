# 🚀 제주 LLM 실습환경 설정 가이드

## 📋 사전 준비사항

### 1. Python 설치
- [Python 공식 사이트](https://www.python.org/downloads/)에서 Python 3.10 이상 다운로드
- 설치 시 **"Add Python to PATH"** 체크박스 반드시 선택
- 설치 완료 후 재부팅 권장

### 2. VS Code 설치
- [VS Code 공식 사이트](https://code.visualstudio.com/)에서 다운로드
- 설치 완료 후 실행

### 3. VS Code 확장 프로그램 설치
VS Code 실행 후 다음 확장 프로그램들을 설치:
- **Python** (Microsoft)
- **Jupyter** (Microsoft)
- **Jupyter Keymap** (Microsoft)
- **Jupyter Slide Show** (Microsoft)

## 🎯 실습환경 설정 (1회만 실행)

### 방법 1: 자동 설정 (권장)
1. `setup` 폴더의 **`install_environment.bat`** 파일을 **더블클릭**
2. 자동으로 모든 설정이 완료됩니다
3. "설정이 완료되었습니다!" 메시지가 나오면 성공

### 방법 2: 수동 설정
만약 자동 설정에 문제가 있다면:
1. 명령 프롬프트(cmd) 실행
2. 프로젝트 폴더로 이동: `cd "C:\Users\살구\Desktop\jeju_llm - 복사본"`
3. 다음 명령어들을 순서대로 실행:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r setup\requirements.txt
   python -m ipykernel install --user --name=jeju-llm-venv --display-name="Jeju LLM (Python 3.10)"
   ```

## 🎮 실습 시작하기

### 1. VS Code에서 프로젝트 열기
- VS Code 실행
- **File → Open Folder** 선택
- `jeju_llm - 복사본` 폴더 선택

### 2. Jupyter 노트북 열기
- `code/study_practice/` 폴더의 `.ipynb` 파일들 중 하나 열기
- 예: `02_Blev_Agent.ipynb`

### 3. 커널 선택
- 노트북 우측 상단의 **커널 선택** 버튼 클릭
- **"Jeju LLM (Python 3.10)"** 선택
- ✅ 표시가 나타나면 성공!

### 4. 환경 테스트
- `setup/test_environment.py` 파일을 실행해서 모든 패키지가 제대로 설치되었는지 확인
- 터미널에서: `python setup/test_environment.py`
- 모든 패키지가 ✅ 표시와 함께 나오면 성공!

### 5. 실습 시작
- 이제 모든 코드 셀을 실행할 수 있습니다
- `Shift + Enter`로 셀 실행
- `Ctrl + Enter`로 셀 실행 (다음 셀로 이동하지 않음)

## 🔧 문제 해결

### 문제 1: 커널이 보이지 않음
**해결방법:**
- `install_environment.bat` 다시 실행
- VS Code 재시작

### 문제 2: 패키지 import 오류
**해결방법:**
- 올바른 커널("Jeju LLM (Python 3.10)") 선택했는지 확인
- `install_environment.bat` 다시 실행

### 문제 3: Python이 인식되지 않음
**해결방법:**
- Python 재설치 (PATH 설정 확인)
- 컴퓨터 재부팅

### 문제 4: yfinance SSL 에러 발생
**에러 메시지:** `SSLError: Failed to perform, curl: (77) error setting certificate verify locations`
**해결방법:**
1. **방법 1**: `python setup/ssl_fix.py` 실행 후 yfinance 사용
2. **방법 2 (권장)**: `python setup/yahoo_finance_alternative.py`로 대체 API 사용
3. **방법 3**: `install_environment.bat` 다시 실행

## 📚 포함된 주요 라이브러리

### AI/LLM
- **OpenAI**: GPT 모델 API 사용
- **PyMuPDF**: PDF 파일 처리 및 분석

### 웹 개발
- **Streamlit**: 데이터 앱 빠른 개발
- **Gradio**: AI 모델 인터페이스
- **FastAPI**: 고성능 웹 API

### 데이터 분석
- **Pandas, NumPy**: 데이터 처리 및 수치 계산
- **Matplotlib, Seaborn, Plotly**: 데이터 시각화
- **yfinance**: Yahoo Finance 주식 데이터 수집

### 유틸리티
- **python-dotenv**: 환경변수 관리
- **Requests**: HTTP 요청 처리
- **Rich**: 터미널 출력 개선

## 💡 팁

- **한 번만 설정하면 됩니다!** 매번 실행할 필요 없음
- VS Code에서 Jupyter 확장 프로그램이 제대로 작동하는지 확인
- 문제가 생기면 `install_environment.bat`을 다시 실행해보세요.

**즐거운 실습 되세요! 🎉**
