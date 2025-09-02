import streamlit as st
import openai
from dotenv import load_dotenv
import os
import json
import pandas as pd

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 페이지 설정
st.set_page_config(
    page_title="02강: 고급 프롬프트 설계 - 구조화된 응답 얻기",
    page_icon="🔮",
    layout="wide"
)

# 제목
st.title("🔮 02강: 고급 프롬프트 설계 - 구조화된 응답 얻기")
st.markdown("---")

# 사이드바 - 강의 내용
with st.sidebar:
    st.header("📚 강의 내용")
    st.markdown("""
    ### 🎯 학습 목표
    - JSON 형태 응답 요청하기
    - 조건부 프롬프트 작성법
    - 프롬프트 체인 구성하기
    
    ### 🔑 핵심 개념
    1. **구조화된 응답**: AI가 정해진 형식으로 응답하게 만들기
    2. **조건부 로직**: 상황에 따라 다른 응답 생성하기
    3. **프롬프트 체인**: 여러 단계를 연결한 복잡한 작업 수행하기
    """)

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📊 JSON 응답", "🎭 조건부 역할", "🔗 프롬프트 체인"])

# 탭 1: JSON 응답
with tab1:
    st.header("📊 JSON 형태 응답 요청하기")
    st.markdown("AI가 자유롭게 대화하는 대신 **구조화된 데이터**로 응답하게 만들어봅시다!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 학생 정보 분석")
        
        # 학생 데이터 리스트
        students_data = {
            "김민수": {
                "name": "김민수",
                "age": 15,
                "grade": "중2",
                "scores": {
                    "math": 85,
                    "korean": 92,
                    "english": 78,
                    "science": 88,
                    "social": 90
                },
                "attendance": 95,
                "personality": "내향적",
                "learning_style": "시각적"
            },
            "이지은": {
                "name": "이지은",
                "age": 15,
                "grade": "중2",
                "scores": {
                    "math": 32,
                    "korean": 95,
                    "english": 89,
                    "science": 41,
                    "social": 87
                },
                "attendance": 98,
                "personality": "외향적",
                "learning_style": "청각적"
            },
            "박준호": {
                "name": "박준호",
                "age": 15,
                "grade": "중2",
                "scores": {
                    "math": 75,
                    "korean": 68,
                    "english": 72,
                    "science": 80,
                    "social": 65
                },
                "attendance": 85,
                "personality": "활발한",
                "learning_style": "실험적"
            },
            "최수진": {
                "name": "최수진",
                "age": 15,
                "grade": "중2",
                "scores": {
                    "math": 88,
                    "korean": 85,
                    "english": 92,
                    "science": 78,
                    "social": 82
                },
                "attendance": 92,
                "personality": "친근한",
                "learning_style": "대화형"
            },
            "정현우": {
                "name": "정현우",
                "age": 15,
                "grade": "중2",
                "scores": {
                    "math": 95,
                    "korean": 78,
                    "english": 85,
                    "science": 92,
                    "social": 75
                },
                "attendance": 96,
                "personality": "차분한",
                "learning_style": "논리적"
            }
        }
        
        # 학생 선택
        selected_student = st.selectbox(
            "분석할 학생을 선택하세요:",
            list(students_data.keys())
        )
        
        if selected_student:
            student_data = students_data[selected_student]
            
            # 선택된 학생 정보 표시
            st.write(f"**📚 {selected_student} 학생 정보**")
            
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.write(f"**나이**: {student_data['age']}세")
                st.write(f"**학년**: {student_data['grade']}")
                st.write(f"**출석률**: {student_data['attendance']}%")
                st.write(f"**성격**: {student_data['personality']}")
                st.write(f"**학습 스타일**: {student_data['learning_style']}")
            
            with col_info2:
                st.write("**📊 과목별 성적**")
                for subject, score in student_data['scores'].items():
                    # 성적에 따른 색상 설정
                    if score >= 90:
                        color = "🟢"
                    elif score >= 80:
                        color = "🟡"
                    elif score >= 70:
                        color = "🟠"
                    else:
                        color = "🔴"
                    
                    st.write(f"{color} {subject}: {score}점")
            
            # JSON 응답 요청
            if st.button("🔍 AI에게 JSON 분석 요청"):
                json_prompt = f"""
다음 학생 정보를 분석하여 JSON 형태로 응답하세요.

**학생 정보:**
{json.dumps(student_data, ensure_ascii=False, indent=2)}

**응답 형식:**
{{
    "analysis": {{
        "overall_performance": "전체적인 성적 수준 (상/중/하)",
        "strengths": ["강점 과목들"],
        "weaknesses": ["약점 과목들"],
        "recommendations": ["개선 방안들"],
        "personality_insights": "성격과 학습 스타일 분석"
    }},
    "study_plan": {{
        "priority_subjects": ["우선 학습 과목들"],
        "weekly_hours": "주간 권장 학습 시간",
        "learning_methods": ["학습 방법들"]
    }}
}}

반드시 위 형식에 맞춰 JSON으로만 응답하세요.
"""
            
            try:
                with st.spinner("AI가 분석 중..."):
                    response = openai.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "당신은 교육 전문가입니다. 항상 요청된 JSON 형식으로만 응답하세요."},
                            {"role": "user", "content": json_prompt}
                        ],
                        temperature=0.3,
                        max_tokens=800
                    )
                    
                    ai_response = response.choices[0].message.content
                    
                    # JSON 파싱 시도
                    try:
                        parsed_response = json.loads(ai_response)
                        st.success("✅ AI가 구조화된 응답을 생성했습니다!")
                        st.json(parsed_response)
                        
                        # 분석 결과 시각화
                        if "analysis" in parsed_response:
                            analysis = parsed_response["analysis"]
                            
                            # 전체 성적 수준을 상단에 강조 표시
                            st.markdown("---")
                            st.subheader("📊 AI 분석 결과")
                            
                            # 전체 성적 수준을 큰 카드로 표시
                            overall_perf = analysis.get("overall_performance", "N/A")
                            if "상" in overall_perf:
                                perf_color = "🟢"
                                perf_bg = "background-color: #d4edda; border: 1px solid #c3e6cb; border-radius: 10px; padding: 20px;"
                            elif "중" in overall_perf:
                                perf_color = "🟡"
                                perf_bg = "background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 10px; padding: 20px;"
                            else:
                                perf_color = "🔴"
                                perf_bg = "background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 10px; padding: 20px;"
                            
                            st.markdown(f"""
                            <div style="{perf_bg}">
                                <h3 style="text-align: center; margin: 0; color: #2c3e50;">
                                    {perf_color} 전체 성적 수준: <strong>{overall_perf}</strong>
                                </h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # 상세 분석을 3개 컬럼으로 나누어 표시
                            col_analysis1, col_analysis2, col_analysis3 = st.columns(3)
                            
                            with col_analysis1:
                                st.markdown("""
                                <div style="background-color: #e8f5e8; border: 1px solid #c8e6c9; border-radius: 10px; padding: 15px; text-align: center;">
                                    <h4 style="color: #2e7d32; margin: 0 0 10px 0;">🎯 강점 과목</h4>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                strengths = analysis.get("strengths", [])
                                if strengths:
                                    for i, strength in enumerate(strengths, 1):
                                        st.markdown(f"""
                                        <div style="background-color: #f1f8e9; border-left: 4px solid #4caf50; padding: 8px 12px; margin: 5px 0; border-radius: 5px;">
                                            <strong>{i}.</strong> {strength}
                                        </div>
                                        """, unsafe_allow_html=True)
                                else:
                                    st.info("강점 과목 정보가 없습니다.")
                            
                            with col_analysis2:
                                st.markdown("""
                                <div style="background-color: #fff3e0; border: 1px solid #ffcc02; border-radius: 10px; padding: 15px; text-align: center;">
                                    <h4 style="color: #ef6c00; margin: 0 0 10px 0;">⚠️ 약점 과목</h4>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                weaknesses = analysis.get("weaknesses", [])
                                if weaknesses:
                                    for i, weakness in enumerate(weaknesses, 1):
                                        st.markdown(f"""
                                        <div style="background-color: #fff8e1; border-left: 4px solid #ff9800; padding: 8px 12px; margin: 5px 0; border-radius: 5px;">
                                            <strong>{i}.</strong> {weakness}
                                        </div>
                                        """, unsafe_allow_html=True)
                                else:
                                    st.info("약점 과목 정보가 없습니다.")
                            
                            with col_analysis3:
                                st.markdown("""
                                <div style="background-color: #e3f2fd; border: 1px solid #90caf9; border-radius: 10px; padding: 15px; text-align: center;">
                                    <h4 style="color: #1565c0; margin: 0 0 10px 0;">💡 개선 방안</h4>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                recommendations = analysis.get("recommendations", [])
                                if recommendations:
                                    for i, rec in enumerate(recommendations, 1):
                                        st.markdown(f"""
                                        <div style="background-color: #f3e5f5; border-left: 4px solid #9c27b0; padding: 8px 12px; margin: 5px 0; border-radius: 5px;">
                                            <strong>{i}.</strong> {rec}
                                        </div>
                                        """, unsafe_allow_html=True)
                                else:
                                    st.info("개선 방안 정보가 없습니다.")
                            
                            # 학습 계획 정보도 추가로 표시
                            if "study_plan" in parsed_response:
                                st.markdown("---")
                                st.subheader("📚 학습 계획")
                                
                                study_plan = parsed_response["study_plan"]
                                col_plan1, col_plan2 = st.columns(2)
                                
                                with col_plan1:
                                    st.markdown("""
                                    <div style="background-color: #fce4ec; border: 1px solid #f8bbd9; border-radius: 10px; padding: 15px;">
                                        <h5 style="color: #c2185b; margin: 0 0 10px 0;">🎯 우선 학습 과목</h5>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    priority_subjects = study_plan.get("priority_subjects", [])
                                    if priority_subjects:
                                        for subject in priority_subjects:
                                            st.markdown(f"""
                                            <div style="background-color: #fdf2f8; padding: 8px 12px; margin: 5px 0; border-radius: 5px; border-left: 4px solid #ec4899;">
                                                🎯 {subject}
                                            </div>
                                            """, unsafe_allow_html=True)
                                
                                with col_plan2:
                                    st.markdown("""
                                    <div style="background-color: #e0f2f1; border: 1px solid #80cbc4; border-radius: 10px; padding: 15px;">
                                        <h5 style="color: #00695c; margin: 0 0 10px 0;">⏰ 주간 학습 시간</h5>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    weekly_hours = study_plan.get("weekly_hours", "N/A")
                                    st.markdown(f"""
                                    <div style="background-color: #f0f9f8; padding: 15px; margin: 5px 0; border-radius: 5px; border-left: 4px solid #26a69a; text-align: center;">
                                        <h4 style="margin: 0; color: #00695c;">⏰ {weekly_hours}</h4>
                                    </div>
                                    """, unsafe_allow_html=True)
                        
                    except json.JSONDecodeError:
                        st.warning("⚠️ AI 응답이 JSON 형식이 아닙니다. 다시 시도해보세요.")
                        st.code(ai_response, language="text")
                        
            except Exception as e:
                st.error(f"AI 응답 생성 오류: {e}")

    with col2:
        st.subheader("💡 JSON 응답의 장점")
        st.markdown("""
        **🎯 정확성**: AI가 자유롭게 대화하는 대신 정확한 정보만 제공
        
        **📊 일관성**: 항상 같은 형식으로 응답하여 데이터 처리 용이
        
        **🔧 자동화**: 프로그래밍으로 응답을 자동으로 파싱하고 활용 가능
        
        **📈 확장성**: 새로운 필드나 형식을 쉽게 추가 가능
        """)
        
        st.subheader("🎨 JSON 응답 활용 예시")
        st.markdown("""
        - **성적 관리 시스템**: 학생별 성적 분석 자동화
        - **보고서 생성**: AI가 분석한 결과를 자동으로 문서화
        - **데이터 시각화**: JSON 데이터를 차트나 그래프로 변환
        - **API 연동**: 다른 시스템과 데이터 교환
        """)

# 탭 2: 조건부 역할
with tab2:
    st.header("🎭 조건부 프롬프트 - 상황별 역할 변신")
    st.markdown("AI가 **상황에 따라 다른 역할**을 자동으로 수행하게 만들어봅시다!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 조건부 역할 설정")
        
        # 학생 성적 입력
        st.write("**학생 성적 입력:**")
        math_score = st.slider("수학 점수", 0, 100, 75)
        korean_score = st.slider("국어 점수", 0, 100, 80)
        english_score = st.slider("영어 점수", 0, 100, 85)
        
        # 평균 계산
        avg_score = (math_score + korean_score + english_score) / 3
        
        st.metric("평균 점수", f"{avg_score:.1f}")
        
        # 조건부 프롬프트 생성
        conditional_prompt = f"""
학생의 성적을 분석하여 상황에 맞는 역할로 응답하세요.

**학생 성적:**
- 수학: {math_score}점
- 국어: {korean_score}점  
- 영어: {english_score}점
- 평균: {avg_score:.1f}점

**조건부 역할 수행:**
1. **평균 90점 이상**: "우수 학생 상담사" 역할로 칭찬과 동기부여
2. **평균 70-89점**: "학습 코치" 역할로 구체적인 개선 방안 제시
3. **평균 50-69점**: "동기부여 전문가" 역할로 격려와 희망 메시지
4. **평균 50점 미만**: "학습 상담사" 역할로 근본적인 문제 해결 방안

**응답 형식:**
{{
    "role": "현재 역할",
    "mood": "전체적인 톤 (긍정적/중립적/우려/긴급)",
    "message": "학생에게 전할 메시지",
    "action_plan": ["구체적인 행동 계획"],
    "encouragement": "격려의 말"
}}

반드시 JSON 형식으로 응답하세요.
"""
        
        if st.button("🎭 AI에게 조건부 역할 요청"):
            try:
                with st.spinner("AI가 역할을 분석 중..."):
                    response = openai.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "당신은 교육 전문가입니다. 조건에 따라 적절한 역할을 수행하고 JSON으로 응답하세요."},
                            {"role": "user", "content": conditional_prompt}
                        ],
                        temperature=0.5,
                        max_tokens=600
                    )
                    
                    ai_response = response.choices[0].message.content
                    
                    try:
                        parsed_response = json.loads(ai_response)
                        st.success("✅ AI가 조건에 맞는 역할로 응답했습니다!")
                        
                        # 역할 정보 표시
                        role_info = parsed_response
                        
                        # 역할별 색상 설정
                        role_colors = {
                            "우수 학생 상담사": "🟢",
                            "학습 코치": "🟡", 
                            "동기부여 전문가": "🟠",
                            "학습 상담사": "🔴"
                        }
                        
                        role_icon = role_colors.get(role_info.get("role", ""), "🎭")
                        
                        st.info(f"{role_icon} **현재 역할**: {role_info.get('role', 'N/A')}")
                        st.info(f"🎭 **전체 톤**: {role_info.get('mood', 'N/A')}")
                        
                        st.write("**💬 메시지:**")
                        st.write(role_info.get('message', 'N/A'))
                        
                        st.write("**📋 행동 계획:**")
                        for action in role_info.get('action_plan', []):
                            st.write(f"• {action}")
                        
                        st.write("**💪 격려의 말:**")
                        st.write(role_info.get('encouragement', 'N/A'))
                        
                    except json.JSONDecodeError:
                        st.warning("⚠️ AI 응답이 JSON 형식이 아닙니다.")
                        st.code(ai_response, language="text")
                        
            except Exception as e:
                st.error(f"AI 응답 생성 오류: {e}")

    with col2:
        st.subheader("🔮 조건부 프롬프트의 마법")
        st.markdown("""
        **🎭 자동 역할 변신**: AI가 상황을 판단해서 적절한 역할 자동 선택
        
        **🎯 맞춤형 응답**: 학생의 성적에 따라 다른 접근 방식 적용
        
        **🔄 동적 상호작용**: 같은 질문에 대해 다양한 관점에서 답변
        
        **📊 체계적 분석**: 조건에 따른 체계적인 분석과 제안
        """)
        
        st.subheader("💡 활용 아이디어")
        st.markdown("""
        - **학습 상담 시스템**: 성적에 따른 자동 상담 역할 분담
        - **고객 서비스**: 고객 상황에 따른 맞춤형 응답
        - **의료 상담**: 증상에 따른 전문의 역할 수행
        - **법률 상담**: 사건 유형에 따른 변호사 역할
        """)

# 탭 3: 프롬프트 체인
with tab3:
    st.header("🔗 프롬프트 체인 - 단계별 작업 수행")
    st.markdown("복잡한 작업을 **여러 단계로 나누어** AI가 순차적으로 수행하게 만들어봅시다!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 단계별 작업 설계")
        
        # 작업 선택
        task_type = st.selectbox(
            "수행할 작업을 선택하세요:",
            ["학생 성적 종합 분석", "학습 계획 수립", "문제 해결 가이드"]
        )
        
        if task_type == "학생 성적 종합 분석":
            chain_steps = [
                "1단계: 성적 데이터 분석 및 패턴 파악",
                "2단계: 개인별 강점과 약점 도출",
                "3단계: 맞춤형 학습 전략 수립",
                "4단계: 구체적인 행동 계획 제시"
            ]
        elif task_type == "학습 계획 수립":
            chain_steps = [
                "1단계: 현재 학습 상태 진단",
                "2단계: 목표 설정 및 우선순위 결정",
                "3단계: 세부 학습 계획 수립",
                "4단계: 진행 상황 모니터링 방법 제시"
            ]
        else:  # 문제 해결 가이드
            chain_steps = [
                "1단계: 문제 상황 분석",
                "2단계: 원인 파악 및 진단",
                "3단계: 해결 방안 도출",
                "4단계: 예방 및 대응 전략 수립"
            ]
        
        st.write("**🔗 작업 단계:**")
        for step in chain_steps:
            st.write(f"• {step}")
        
        # 프롬프트 체인 실행
        if st.button("🚀 프롬프트 체인 실행"):
            try:
                # 1단계 실행
                st.write("**🔄 1단계 실행 중...**")
                step1_prompt = f"""
{task_type}의 첫 번째 단계를 수행하세요.

**작업 유형**: {task_type}
**1단계**: {chain_steps[0]}

학생 데이터를 기반으로 첫 번째 단계를 완료하고, 다음 단계로 넘어갈 수 있도록 
중간 결과를 정리해주세요.

**응답 형식:**
{{
    "step": "1단계",
    "status": "완료",
    "result": "1단계 결과 요약",
    "next_step_data": "2단계에서 사용할 데이터",
    "insights": ["주요 인사이트들"]
}}
"""
                
                with st.spinner("1단계 실행 중..."):
                    response1 = openai.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "당신은 교육 전문가입니다. 단계별로 체계적으로 작업을 수행하세요."},
                            {"role": "user", "content": step1_prompt}
                        ],
                        temperature=0.3,
                        max_tokens=500
                    )
                    
                    step1_result = response1.choices[0].message.content
                    
                    try:
                        parsed_step1 = json.loads(step1_result)
                        st.success("✅ 1단계 완료!")
                        
                        # 1단계 결과 표시
                        with st.expander("📊 1단계 결과", expanded=True):
                            st.json(parsed_step1)
                        
                        # 2단계 실행
                        st.write("**🔄 2단계 실행 중...**")
                        step2_prompt = f"""
{task_type}의 두 번째 단계를 수행하세요.

**작업 유형**: {task_type}
**2단계**: {chain_steps[1]}

**1단계 결과:**
{json.dumps(parsed_step1, ensure_ascii=False, indent=2)}

1단계 결과를 바탕으로 두 번째 단계를 수행하고, 다음 단계로 넘어갈 수 있도록 
중간 결과를 정리해주세요.

**응답 형식:**
{{
    "step": "2단계",
    "status": "완료",
    "result": "2단계 결과 요약",
    "next_step_data": "3단계에서 사용할 데이터",
    "insights": ["주요 인사이트들"]
}}
"""
                        
                        with st.spinner("2단계 실행 중..."):
                            response2 = openai.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=[
                                    {"role": "system", "content": "당신은 교육 전문가입니다. 1단계 결과를 바탕으로 2단계를 수행하세요."},
                                    {"role": "user", "content": step2_prompt}
                                ],
                                temperature=0.3,
                                max_tokens=500
                            )
                            
                            step2_result = response2.choices[0].message.content
                            
                            try:
                                parsed_step2 = json.loads(step2_result)
                                st.success("✅ 2단계 완료!")
                                
                                # 2단계 결과 표시
                                with st.expander("📊 2단계 결과", expanded=True):
                                    st.json(parsed_step2)
                                
                                # 최종 요약
                                st.info("🎯 **프롬프트 체인 실행 완료!**")
                                st.write("AI가 단계별로 체계적으로 작업을 수행했습니다.")
                                
                            except json.JSONDecodeError:
                                st.warning("2단계 응답이 JSON 형식이 아닙니다.")
                                st.code(step2_result, language="text")
                                
                    except json.JSONDecodeError:
                        st.warning("1단계 응답이 JSON 형식이 아닙니다.")
                        st.code(step1_result, language="text")
                        
            except Exception as e:
                st.error(f"프롬프트 체인 실행 오류: {e}")

    with col2:
        st.subheader("🔗 프롬프트 체인의 장점")
        st.markdown("""
        **🧠 체계적 사고**: 복잡한 문제를 단계별로 분해하여 해결
        
        **📊 단계별 검증**: 각 단계의 결과를 확인하고 다음 단계 진행
        
        **🔄 재사용성**: 성공한 체인을 다른 문제에 적용 가능
        
        **🎯 정확성**: 단계별 검증으로 최종 결과의 품질 향상
        """)
        
        st.subheader("💡 체인 설계 팁")
        st.markdown("""
        - **명확한 단계**: 각 단계의 목표와 출력을 명확히 정의
        
        - **데이터 연결**: 이전 단계의 결과를 다음 단계에서 활용
        
        - **검증 포인트**: 각 단계에서 결과의 품질 확인
        
        - **유연성**: 필요에 따라 단계 추가/수정 가능
        """)

# 실습 과제
st.markdown("---")
st.header("💡 실습 과제")

col3, col4 = st.columns([1, 1])

with col3:
    st.subheader("🎯 과제 1: JSON 응답 마스터")
    st.markdown("""
    **목표**: 다양한 주제로 JSON 응답 요청하기
    
    **실험 방법**:
    1. 다른 학생 데이터로 JSON 분석 요청
    2. 응답 형식을 수정해서 다양한 정보 요청
    3. JSON 파싱 오류 처리 방법 연습
    
    **예시**:
    - 도서 정보 분석
    - 날씨 데이터 요약
    - 쇼핑 리스트 정리
    """)

with col4:
    st.subheader("🎯 과제 2: 조건부 역할 확장")
    st.markdown("""
    **목표**: 더 복잡한 조건부 로직 구현하기
    
    **실험 방법**:
    1. 성적 외에 다른 조건 추가 (출석률, 과제 완성도 등)
    2. 새로운 역할과 응답 형식 설계
    3. 여러 조건을 조합한 복합 로직 구현
    
    **예시**:
    - 성적 + 성격 + 학습 스타일 조합
    - 계절별 학습 조언
    - 나이대별 맞춤 가이드
    """)

# 다음 강의 예고
st.markdown("---")
st.markdown("""
### 📚 다음 강의 예고
**03강: 교육에서의 AI 활용 - 학생 데이터 분석**
- 가상 학생 데이터로 AI 분석 실습
- 성적 패턴 분석 및 개인별 맞춤 조언
- 학습 효과 예측 및 개선 방안 제시
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
