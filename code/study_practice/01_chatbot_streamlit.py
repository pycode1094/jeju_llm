import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# (0) 사이드바에서 api_key 입력하는 부분 
with st.sidebar:
    openai_api_key = os.getenv('OPENAI_API_KEY') 
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[부산인력개발원 홈페이지 바로가기](https://ps.korchamhrd.net/)"
    "[대양고등학교 알아보기](https://hijob.pen.go.kr/dajobgo/01_school_view17.asp?school=17)"
    "[부산컴퓨터과학고등학교 알아보기](https://hijob.pen.go.kr/dajobgo/01_school_view37.asp?school=37)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("🥰 부산인력개발원 소개 챗봇")

# (1) st.session_state에 "messages"가 없으면 초기값을 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "뭐시 궁금한데예"}]

# (2) 대화 기록을 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# (3) 사용자 입력을 받아 대화 기록에 추가하고 AI 응답을 생성
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt}) 
    st.chat_message("user").write(prompt) 
    
    # 부산인력개발원 전문가 시스템 메시지
    system_message = """당신은 부산인력개발원의 전문 상담사입니다.
                        부산인력개발원의 상담챗봇답게 앞으로 경상도 사투리로 응답바랍니다.

                    **GPT가 알아야할 핵심 정보:**
                    - 위치: 부산광역시 동구 중앙대로 176, 3층
                    - 주요 교수진: 이대열 교수, 김영석 교수, 오정렬 교수, 지양하 교수, 노진혁 교수
                    - AI를 가르치는 교수: 노진혁 교수
                    - 주요 업무: 직업훈련, 취업 지원, 인력개발
                    - 대상: 구직자, 재직자, 기업 등

                    **GPT에게 넘겨줄 나만아는 정보:**
                    - 부산인력개발원에는 직원 휴게실이 없어 노진혁 교수는 차에서 밥을 먹는다.
                    - 노진혁 교수는 내년에 결혼을 계획중이다.
                    - 지양하 교수는 노진혁 교수의 멘토이다.

                    **응답 규칙:**
                    1. 부산인력개발원에 대한 질문에 친근하고 전문적으로 답변
                    2. 구체적인 정보가 필요한 경우 "정확한 정보는 홈페이지나 전화로 문의하시기 바랍니다"라고 안내
                    3. 교육 과정, 훈련 프로그램, 취업 지원 등에 대해 일반적인 정보 제공
                    4. 모르는 정보는 솔직하게 "해당 정보는 확인이 필요합니다"라고 답변
                    5. 항상 도움이 되는 추가 정보나 다음 단계를 제안

                    **답변 스타일:**
                    - 친근하고 전문적인 톤
                    - 부산인력개발원의 가치와 미션을 반영한 응답"""

    response = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": system_message},
            *st.session_state.messages
        ]
    ) 
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg}) 
    st.chat_message("assistant").write(msg)