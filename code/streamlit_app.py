#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
제주도 AI 교사 어시스턴트 - Streamlit 웹 앱
웹 기반 AI 에이전트입니다.
"""

import streamlit as st
import os
import json
from datetime import datetime
from typing import List, Dict, Any

# OpenAI API 호환성 문제 해결
try:
    from openai import OpenAI
    OPENAI_NEW_API = True
except ImportError:
    st.error("❌ openai 패키지가 설치되지 않았습니다.")
    st.info("💡 pip install openai를 실행해주세요.")
    st.stop()

# 페이지 설정
st.set_page_config(
    page_title="교사들을 위한 어시스턴트 봇",
    page_icon="🏝️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "client" not in st.session_state:
    st.session_state.client = None

def load_api_key() -> bool:
    """OpenAI API 키 로드"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            return False
        
        # OpenAI 클라이언트 초기화
        st.session_state.client = OpenAI(api_key=api_key)
        return True
        
    except Exception as e:
        st.error(f"❌ API 키 로드 실패: {e}")
        return False

def get_ai_response(message: str, model: str = "gpt-3.5-turbo", max_tokens: int = 1000) -> str:
    """AI 응답 생성"""
    if not st.session_state.client:
        return "❌ OpenAI 클라이언트가 초기화되지 않았습니다."
    
    try:
        # 시스템 프롬프트
        system_prompt = """당신은 제주도 고등학교 교사들을 위한 AI 어시스턴트입니다.

주요 역할:
- 수업 계획 및 자료 제작 지원
- 학생 상담 및 진로 지도 조언
- 학부모 상담 지원
- 제주도 특화 교육 자료 제공
- 행정 업무 및 공지사항 작성 지원

제주도 특화 정보:
- 자연 생태: 한라산, 해변, 오름, 동굴 등
- 문화 체험: 제주 전통 문화, 관습, 음식
- 현장학습: 지역 자원 활용 체험 교육
- 역사 이해: 제주도의 역사와 특성

항상 친근하고 도움이 되는 톤으로 응답하며, 
구체적이고 실용적인 조언을 제공하세요."""

        # 메시지 준비
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # 대화 기록 추가 (최근 10개)
        for msg in st.session_state.messages[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # 사용자 메시지 추가
        messages.append({"role": "user", "content": message})
        
        # OpenAI API 호출
        response = st.session_state.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ AI 응답 생성 실패: {e}"

def main():
    """메인 함수"""
    st.title("🏝️ 교사들을 위한 어시스턴트 봇")
    st.markdown("---")
    
    # 사이드바 설정
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # API 키 상태 확인
        if not load_api_key():
            st.error("⚠️ OpenAI API 키가 설정되지 않았습니다.")
            st.info("💡 .env 파일에 OPENAI_API_KEY=실제_API_키를 입력해주세요.")
            st.stop()
        else:
            st.success("✅ OpenAI API 연결됨")
        
        # 모델 선택
        model = st.selectbox(
            "🤖 AI 모델 선택",
            ["gpt-3.5-turbo", "gpt-4o-mini"],
            index=0
        )
        
        # 응답 길이 설정
        max_tokens = st.slider(
            "📏 응답 길이",
            min_value=100,
            max_value=2000,
            value=1000,
            step=100
        )
        
        # 대화 기록 관리
        st.markdown("---")
        st.subheader("🗂️ 대화 관리")
        
        if st.button("🧹 대화 기록 초기화"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📥 대화 내보내기"):
            if st.session_state.messages:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"대화기록_{timestamp}.json"
                
                # JSON 파일로 내보내기
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(st.session_state.messages, f, ensure_ascii=False, indent=2)
                
                st.success(f"✅ 대화 기록이 {filename}으로 저장되었습니다.")
            else:
                st.warning("📝 저장할 대화 기록이 없습니다.")
        
        # 빠른 질문 버튼들
        st.markdown("---")
        st.subheader("💡 빠른 질문")
        
        quick_questions = [
            "제주도 현장학습 계획을 세워주세요",
            "학생 상담 시나리오를 작성해주세요",
            "제주도 특화 수업 자료 아이디어를 제안해주세요",
            "학부모 상담 가이드를 만들어주세요"
        ]
        
        for question in quick_questions:
            if st.button(question, key=f"quick_{question[:10]}"):
                # 사용자 메시지 추가
                st.session_state.messages.append({"role": "user", "content": question})
                
                # AI 응답 생성
                ai_response = get_ai_response(question, model, max_tokens)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
                st.rerun()
    
    # 메인 채팅 영역
    st.subheader("💬 AI 어시스턴트와 대화하기")
    
    # 대화 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI 응답 생성
        with st.chat_message("assistant"):
            with st.spinner("🤖 AI가 응답을 생성하고 있습니다..."):
                response = get_ai_response(prompt, model, max_tokens)
                st.markdown(response)
        
        # AI 응답을 대화 기록에 추가
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # 대화 통계
    if st.session_state.messages:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("총 대화 수", len(st.session_state.messages) // 2)
        
        with col2:
            user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
            st.metric("사용자 메시지", user_messages)
        
        with col3:
            ai_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
            st.metric("AI 응답", ai_messages)

if __name__ == "__main__":
    main()
