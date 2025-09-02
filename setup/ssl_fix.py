#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSL 인증서 문제 해결 스크립트
yfinance 사용 시 SSL 에러가 발생하는 경우 이 스크립트를 먼저 실행하세요.
"""

import os
import ssl
import certifi
import requests

def fix_ssl_issues():
    """SSL 인증서 문제를 해결합니다."""
    print("🔧 SSL 인증서 문제 해결 중...")
    
    # 1. certifi 경로 확인
    cert_path = certifi.where()
    print(f"   SSL 인증서 경로: {cert_path}")
    
    # 2. 환경변수 설정
    os.environ['REQUESTS_CA_BUNDLE'] = cert_path
    os.environ['SSL_CERT_FILE'] = cert_path
    os.environ['CURL_CA_BUNDLE'] = cert_path
    
    print("   환경변수 설정 완료")
    
    # 3. SSL 컨텍스트 생성
    try:
        ssl_context = ssl.create_default_context(cafile=cert_path)
        print("   SSL 컨텍스트 생성 성공")
    except Exception as e:
        print(f"   SSL 컨텍스트 생성 실패: {e}")
        return False
    
    # 4. requests 세션 설정
    try:
        session = requests.Session()
        session.verify = cert_path
        print("   requests 세션 설정 완료")
    except Exception as e:
        print(f"   requests 세션 설정 실패: {e}")
        return False
    
    print("   ✅ SSL 문제 해결 완료!")
    return True

def test_yfinance():
    """yfinance가 제대로 작동하는지 테스트합니다."""
    print("\n🧪 yfinance 테스트 중...")
    
    try:
        import yfinance as yf
        print(f"   yfinance 버전: {yf.__version__}")
        
        # 간단한 테스트
        msft = yf.Ticker("MSFT")
        info = msft.info
        print("   Microsoft 주식 정보 가져오기 성공!")
        print(f"   회사명: {info.get('longName', 'N/A')}")
        print(f"   현재가: ${info.get('currentPrice', 'N/A')}")
        
        print("   ✅ yfinance 테스트 성공!")
        return True
        
    except Exception as e:
        print(f"   ❌ yfinance 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 SSL 인증서 문제 해결 도구")
    print("=" * 60)
    
    # SSL 문제 해결
    if fix_ssl_issues():
        # yfinance 테스트
        test_yfinance()
    else:
        print("   ❌ SSL 문제 해결에 실패했습니다.")
    
    print("\n" + "=" * 60)
    print("💡 사용법:")
    print("1. 이 스크립트를 먼저 실행: python setup/ssl_fix.py")
    print("2. 그 다음 yfinance를 사용하는 코드 실행")
    print("3. 문제가 지속되면 강사에게 문의")
    print("=" * 60)
