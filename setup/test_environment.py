#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
print("=" * 60)
print("🔍 제주 LLM 실습환경 테스트 시작")
print("=" * 60)
print()

# 1. 기본 Python 환경 확인
print("1️⃣ Python 환경 확인 중...")
print(f"   Python 버전: {sys.version}")
print(f"   Python 경로: {sys.executable}")
print("   ✅ Python 환경 확인 완료")
print()

# 2. AI/LLM 패키지 테스트
print("2️⃣ AI/LLM 패키지 테스트 중...")
try:
    import openai
    print(f"   OpenAI: {openai.__version__} ✅")
except ImportError as e:
    print(f"   OpenAI: ❌ {e}")

try:
    import pymupdf
    print(f"   PyMuPDF: {pymupdf.__version__} ✅")
except ImportError as e:
    print(f"   PyMuPDF: ❌ {e}")

print("   ✅ AI/LLM 패키지 테스트 완료")
print()

# 3. 웹 개발 패키지 테스트
print("3️⃣ 웹 개발 패키지 테스트 중...")
try:
    import streamlit
    print(f"   Streamlit: {streamlit.__version__} ✅")
except ImportError as e:
    print(f"   Streamlit: ❌ {e}")

try:
    import gradio
    print(f"   Gradio: {gradio.__version__} ✅")
except ImportError as e:
    print(f"   Gradio: ❌ {e}")

try:
    import fastapi
    print(f"   FastAPI: {fastapi.__version__} ✅")
except ImportError as e:
    print(f"   FastAPI: ❌ {e}")

try:
    import uvicorn
    print(f"   Uvicorn: {uvicorn.__version__} ✅")
except ImportError as e:
    print(f"   Uvicorn: ❌ {e}")

print("   ✅ 웹 개발 패키지 테스트 완료")
print()

# 4. 데이터 분석 패키지 테스트
print("4️⃣ 데이터 분석 패키지 테스트 중...")
try:
    import pandas as pd
    print(f"   Pandas: {pd.__version__} ✅")
except ImportError as e:
    print(f"   Pandas: ❌ {e}")

try:
    import numpy as np
    print(f"   NumPy: {np.__version__} ✅")
except ImportError as e:
    print(f"   NumPy: ❌ {e}")

try:
    import matplotlib
    print(f"   Matplotlib: {matplotlib.__version__} ✅")
except ImportError as e:
    print(f"   Matplotlib: ❌ {e}")

try:
    import seaborn as sns
    print(f"   Seaborn: {sns.__version__} ✅")
except ImportError as e:
    print(f"   Seaborn: ❌ {e}")

try:
    import plotly
    print(f"   Plotly: {plotly.__version__} ✅")
except ImportError as e:
    print(f"   Plotly: ❌ {e}")

try:
    import yfinance
    print(f"   yfinance: {yfinance.__version__} ✅")
except ImportError as e:
    print(f"   yfinance: ❌ {e}")

print("   ✅ 데이터 분석 패키지 테스트 완료")
print()

# 5. 유틸리티 패키지 테스트
print("5️⃣ 유틸리티 패키지 테스트 중...")
try:
    from dotenv import load_dotenv
    print("   python-dotenv: ✅")
except ImportError as e:
    print(f"   python-dotenv: ❌ {e}")

try:
    import requests
    print(f"   Requests: {requests.__version__} ✅")
except ImportError as e:
    print(f"   Requests: ❌ {e}")

try:
    import rich
    print("   Rich: ✅")
except ImportError as e:
    print(f"   Rich: ❌ {e}")

try:
    import tqdm
    print(f"   TQDM: {tqdm.__version__} ✅")
except ImportError as e:
    print(f"   TQDM: ❌ {e}")

print("   ✅ 유틸리티 패키지 테스트 완료")
print()

# 6. 최종 결과
print("=" * 60)
print("🎉 패키지 테스트 완료!")
print("=" * 60)
print()

print("📋 다음 단계:")
print("1. VS Code에서 Jupyter 노트북(.ipynb) 열기")
print("2. 우측 상단 커널 선택에서 'Jeju LLM (Python 3.10)' 선택")
print("3. 실습 시작!")
print()

print("💡 팁:")
print("- 모든 패키지가 ✅ 표시와 함께 나오면 성공!")
print("- ❌ 표시가 있다면 'install_environment.bat'을 다시 실행해보세요")
print("- 문제가 지속되면 강사에게 문의하세요")
print()

print("즐거운 실습 되세요! ��")
print("=" * 60)
