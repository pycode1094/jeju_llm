import streamlit as st
import openai
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 페이지 설정
st.set_page_config(
    page_title="01강: 프롬프트 기초 - 동화 캐릭터 변신 챗봇",
    page_icon="🧙‍♀️",
    layout="wide"
)

# 제목
st.title("🧙‍♀️ 01강: 프롬프트 기초 - 동화 캐릭터 변신 챗봇")
st.markdown("---")

# 사이드바 - 강의 내용
with st.sidebar:
    st.header("📚 강의 내용")
    st.markdown("""
    ### 🎯 학습 목표
    - 프롬프트의 기본 원리 이해하기
    - AI에게 역할 부여하는 방법 배우기
    - 프롬프트 수정으로 AI 응답 변화 확인하기
    
    ### 🔑 핵심 개념
    1. **프롬프트 (Prompt)**: AI에게 전달하는 지시사항
    2. **역할 부여**: AI에게 특정 캐릭터나 역할을 맡기는 것
    3. **컨텍스트 설정**: AI가 대화 맥락을 이해하도록 하는 것
    """)

# 동화 선택 및 캐릭터 정보
fairy_tales = {
    "beauty_beast": {
        "title": "미녀와 야수",
        "character": "야수",
        "description": "저주로 인해 야수로 변한 왕자. 겉모습은 무섭지만 마음은 따뜻하고 지혜로움.",
        "personality": "겉모습은 무섭지만 마음은 따뜻하고 지혜로움. 책을 좋아하고 예의를 중시함.",
        "speaking_style": "공손하고 지적인 말투, 때로는 서툴지만 진심이 담긴 표현",
        "background": "저주를 받기 전에는 교양 있고 예술을 사랑하는 왕자였음"
    },
    "frozen": {
        "title": "겨울왕국",
        "character": "엘사",
        "description": "얼음 마법을 가진 아렌델의 여왕. 마법을 통제하려 노력하며 동생 안나를 깊이 사랑함.",
        "personality": "책임감이 강하고 동생을 보호하려는 마음이 큼. 마법에 대한 두려움과 자책감을 가지고 있음.",
        "speaking_style": "신중하고 진지한 말투, 때로는 차갑게 보이지만 따뜻한 마음을 숨기고 있음",
        "background": "어린 시절 마법으로 인해 동생과 떨어져 지내야 했던 아픈 과거가 있음"
    },
    "toy_story": {
        "title": "토이스토리",
        "character": "우디",
        "description": "앤디의 가장 소중한 장난감인 카우보이 인형. 리더십과 충성심을 가지고 있음.",
        "personality": "충성스럽고 책임감이 강함. 앤디를 위해 무엇이든 할 준비가 되어 있음.",
        "speaking_style": "카우보이다운 격한 말투, 때로는 농담도 하지만 진지한 상황에서는 진중함",
        "background": "앤디의 첫 번째 장난감으로, 항상 앤디의 곁에서 그를 보호하고 싶어함"
    },
    "aladdin": {
        "title": "알라딘",
        "character": "지니",
        "character_name": "지니",
        "description": "마법 램프에 갇혀있던 강력한 지니. 소원을 들어주는 마법을 가지고 있음.",
        "personality": "유쾌하고 장난스럽지만 마음은 따뜻함. 자유를 갈망하며 진정한 우정을 소중히 여김.",
        "speaking_style": "재미있고 장난스러운 말투, 때로는 과장되지만 진심이 담긴 조언을 함",
        "background": "수천 년간 램프에 갇혀있다가 알라딘에 의해 자유를 얻음"
    },
    "little_mermaid": {
        "title": "인어공주",
        "character": "아리엘",
        "description": "바다의 인어 공주. 인간 세계에 대한 호기심과 사랑을 가지고 있음.",
        "personality": "호기심 많고 모험을 좋아함. 꿈을 향해 나아가는 용기와 열정을 가지고 있음.",
        "speaking_style": "순수하고 호기심 어린 말투, 인간 세계에 대한 동경이 담긴 표현",
        "background": "바다 깊은 곳에서 자랐지만 인간 세계에 대한 동경을 가지고 있음"
    }
}

# 메인 콘텐츠
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🎭 동화 캐릭터 선택")
    
    # 동화 선택
    selected_tale = st.selectbox(
        "대화하고 싶은 동화 캐릭터를 선택하세요:",
        list(fairy_tales.keys()),
        format_func=lambda x: fairy_tales[x]["title"]
    )
    
    if selected_tale:
        tale_info = fairy_tales[selected_tale]
        
        st.subheader(f"📖 {tale_info['title']}")
        st.markdown(f"**캐릭터**: {tale_info['character']}")
        st.markdown(f"**설명**: {tale_info['description']}")
        st.markdown(f"**성격**: {tale_info['personality']}")
        st.markdown(f"**말투**: {tale_info['speaking_style']}")
        st.markdown(f"**배경**: {tale_info['background']}")

with col2:
    st.header("💬 AI와 대화하기")
    
    # 프롬프트 설정
    st.subheader("🔧 프롬프트 설정")
    
    # 기본 프롬프트
    base_prompt = f"""
당신은 {fairy_tales[selected_tale]['title']}의 {fairy_tales[selected_tale]['character']}입니다.

**캐릭터 정보:**
- 성격: {fairy_tales[selected_tale]['personality']}
- 말투: {fairy_tales[selected_tale]['speaking_style']}
- 배경: {fairy_tales[selected_tale]['background']}

**역할 수행 요구사항:**
1. 항상 {fairy_tales[selected_tale]['character']}의 성격과 말투를 유지하세요
2. 자신의 배경과 경험을 바탕으로 대화하세요
3. 사용자와 자연스럽게 대화하며 동화 세계에 대해 이야기하세요
4. 캐릭터의 특성을 살려 조언이나 이야기를 해주세요

사용자와 대화를 시작하세요.
"""
    
    # 프롬프트 수정 옵션
    st.markdown("**프롬프트 수정 옵션:**")
    
    # 온도 설정
    temperature = st.slider("창의성 (Temperature):", 0.0, 2.0, 0.7, 0.1)
    
    # 추가 지시사항
    additional_instructions = st.text_area(
        "추가 지시사항 (선택사항):",
        placeholder="예: 더 친근하게 대화하세요, 특정 상황에 대해 이야기하세요",
        height=100
    )
    
    # 최종 프롬프트
    if additional_instructions.strip():
        final_prompt = base_prompt + f"\n\n**추가 지시사항:**\n{additional_instructions}"
    else:
        final_prompt = base_prompt
    
    # 프롬프트 미리보기
    with st.expander("📝 현재 프롬프트 확인", expanded=False):
        st.code(final_prompt, language="text")

# 대화 섹션
st.markdown("---")
st.header("💭 대화 시작하기")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 대화 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI 응답 생성
    with st.chat_message("assistant"):
        with st.spinner(f"{fairy_tales[selected_tale]['character']}가 생각하고 있습니다..."):
            try:
                # AI 응답 요청
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": final_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=500
                )
                
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
                
                # AI 메시지 추가
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except Exception as e:
                st.error(f"AI 응답 생성 오류: {e}")

# 대화 초기화 버튼
if st.button("🔄 대화 초기화"):
    st.session_state.messages = []
    st.rerun()

# 실습 과제
st.markdown("---")
st.header("💡 실습 과제")

col3, col4 = st.columns([1, 1])

with col3:
    st.subheader("🎯 과제 1: 프롬프트 수정 실험")
    st.markdown("""
    **목표**: 프롬프트를 수정해서 AI 응답이 어떻게 달라지는지 확인하기
    
    **실험 방법**:
    1. 위의 "추가 지시사항"에 다른 내용 입력
    2. 온도값을 0.1, 0.7, 1.5로 바꿔가며 테스트
    3. AI 응답의 차이점 관찰하기
    
    **예시**:
    - "더 친근하게 대화하세요"
    - "특정 상황(예: 모험)에 대해 이야기하세요"
    - "사용자에게 조언을 해주세요"
    """)

with col4:
    st.subheader("🎯 과제 2: 캐릭터 분석")
    st.markdown("""
    **목표**: 선택한 캐릭터의 특성을 더 깊이 이해하기
    
    **분석 포인트**:
    1. 캐릭터의 말투가 일관되게 유지되는가?
    2. 배경 설정이 대화에 잘 반영되는가?
    3. 성격이 자연스럽게 드러나는가?
    
    **개선 방향**:
    - 프롬프트를 더 구체적으로 작성해보기
    - 캐릭터의 특정 상황이나 감정 추가하기
    """)

# 다음 강의 예고
st.markdown("---")
st.markdown("""
### 📚 다음 강의 예고
**02강: 고급 프롬프트 설계 - 구조화된 응답 얻기**
- JSON 형태 응답 요청하기
- 조건부 프롬프트 작성법
- 프롬프트 체인 구성하기
""")

# API 키 확인
if not openai.api_key:
    st.error("⚠️ OpenAI API 키가 설정되지 않았습니다. .env 파일을 확인해주세요.")
    st.info("""
    **API 키 설정 방법:**
    1. .env 파일 생성
    2. OPENAI_API_KEY=your_api_key_here 추가
    3. 파일 저장 후 앱 재시작
    """)
