import streamlit as st
import openai
from dotenv import load_dotenv
import os
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 페이지 설정
st.set_page_config(
    page_title="03강: 교육에서의 AI 활용 - 학생 데이터 분석",
    page_icon="📊",
    layout="wide"
)

# 제목
st.title("📊 03강: 교육에서의 AI 활용 - 학생 데이터 분석")
st.markdown("---")

# 사이드바 - 강의 내용
with st.sidebar:
    st.header("📚 강의 내용")
    st.markdown("""
    ### 🎯 학습 목표
    - CSV 데이터 업로드 및 처리
    - AI를 활용한 학생 데이터 분석
    - 데이터 시각화 및 인사이트 도출
    
    ### 🔑 핵심 개념
    1. **데이터 기반 교육**: 학생 정보를 체계적으로 분석
    2. **AI 분석 결과 해석**: AI가 제공한 인사이트 활용
    3. **개인별 맞춤 교육**: 데이터를 바탕으로 한 개인화 전략
    """)

# 데이터 로드 함수
def load_student_data():
    """학생 데이터 로드 (엑셀 파일 업로드 또는 기존 파일)"""
    try:
        # 엑셀 파일이 있으면 로드
        if os.path.exists("student_data.xlsx"):
            df = pd.read_excel("student_data.xlsx", engine='openpyxl')
            st.success("✅ student_data.xlsx 파일을 성공적으로 로드했습니다!")
            return df
    except Exception as e:
        st.warning(f"⚠️ 엑셀 파일 로드 중 오류가 발생했습니다: {e}")
        return None

# 탭 구성
tab1, tab2, tab3, tab4 = st.tabs(["📁 데이터 업로드", "📈 데이터 시각화", "🤖 AI 개인 분석", "🎯 AI 교육 전략"])

# 탭 1: 데이터 업로드
with tab1:
    st.header("📁 학생 데이터 업로드")
    st.markdown("CSV 파일을 업로드하여 학생 데이터를 분석해보세요!")
    
    # 파일 업로드
    uploaded_file = st.file_uploader(
        "학생 데이터 엑셀 파일을 선택하세요",
        type=['xlsx', 'xls'],
        help="학생 정보가 포함된 엑셀 파일을 업로드하세요. 컬럼은 자유롭게 구성할 수 있습니다."
    )
    
    if uploaded_file is not None:
        try:
            # 엑셀 파일 읽기
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.success(f"✅ 파일 업로드 성공! {len(df)}명의 학생 데이터를 로드했습니다.")
            
            # 데이터 미리보기
            st.subheader("📋 데이터 미리보기")
            st.dataframe(df.head())
            
            # 데이터 정보
            st.subheader("📊 데이터 정보")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**총 학생 수**: {len(df)}명")
                st.write(f"**데이터 컬럼 수**: {len(df.columns)}개")
                
            with col2:
                st.write(f"**데이터 타입**:")
                for col in df.columns:
                    st.write(f"• {col}: {df.dtypes[col]}")
            
            # 파일 저장
            df.to_excel("student_data.xlsx", index=False, engine='openpyxl')
            st.success("💾 데이터가 student_data.xlsx로 저장되었습니다!")
            
            # 전역 변수로 설정
            st.session_state['student_df'] = df
            
        except Exception as e:
            st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
            st.info("CSV 파일 형식을 확인해주세요.")
    
    # 기존 파일 로드
    else:
        existing_df = load_student_data()
        if existing_df is not None:
            st.session_state['student_df'] = existing_df
        else:
            st.warning("⚠️ 데이터를 업로드하거나 기존 파일을 준비해주세요.")
            st.info("""
            **데이터 형식 예시:**
            - student_id, name, gender, age, grade
            - math_score, korean_score, english_score
            - attendance_rate, homework_rate, study_time
            - favorite_subject, learning_style, personality
            
            **파일 형식**: .xlsx 또는 .xls 엑셀 파일
            """)

# 데이터 확인
if 'student_df' in st.session_state:
    student_df = st.session_state['student_df']
    
    # 탭 2: 데이터 시각화
    with tab2:
        st.header("📈 학생 데이터 시각화")
        st.markdown("학생 데이터를 다양한 차트로 분석해봅시다!")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📊 성적 분포 분석")
            
            # 차트 타입 선택
            chart_type = st.selectbox(
                "차트 타입을 선택하세요:",
                ["막대 차트", "박스 플롯", "히스토그램", "산점도"]
            )
            
            # 성적 컬럼 찾기
            score_cols = [col for col in student_df.columns if 'score' in col.lower()]
            
            if score_cols:
                if chart_type == "막대 차트":
                    # 과목별 평균 성적
                    subject_names = [col.replace('_score', '').replace('_', ' ').title() for col in score_cols]
                    avg_scores = [student_df[col].mean() for col in score_cols]
                    
                    fig = px.bar(
                        x=subject_names, 
                        y=avg_scores,
                        title="과목별 평균 성적",
                        labels={'x': '과목', 'y': '평균 점수'},
                        color=avg_scores,
                        color_continuous_scale='RdYlGn'
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                elif chart_type == "박스 플롯":
                    # 과목별 성적 분포
                    fig = go.Figure()
                    
                    for i, col in enumerate(score_cols):
                        subject_name = col.replace('_score', '').replace('_', ' ').title()
                        fig.add_trace(go.Box(
                            y=student_df[col],
                            name=subject_name,
                            boxpoints='outliers'
                        ))
                    
                    fig.update_layout(
                        title="과목별 성적 분포",
                        yaxis_title="점수",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                elif chart_type == "히스토그램":
                    # 전체 성적 분포
                    all_scores = []
                    for col in score_cols:
                        all_scores.extend(student_df[col].tolist())
                    
                    fig = px.histogram(
                        x=all_scores,
                        title="전체 성적 분포",
                        labels={'x': '점수', 'y': '학생 수'},
                        nbins=20
                    )
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                    
                elif chart_type == "산점도":
                    # 첫 번째와 두 번째 성적 컬럼으로 산점도
                    if len(score_cols) >= 2:
                        col1_name = score_cols[0].replace('_score', '').replace('_', ' ').title()
                        col2_name = score_cols[1].replace('_score', '').replace('_', ' ').title()
                        
                        fig = px.scatter(
                            student_df,
                            x=score_cols[0],
                            y=score_cols[1],
                            title=f"{col1_name} vs {col2_name} 성적 상관관계",
                            labels={score_cols[0]: f'{col1_name} 점수', score_cols[1]: f'{col2_name} 점수'},
                            hover_data=['name'] if 'name' in student_df.columns else None
                        )
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("산점도를 그리려면 최소 2개의 성적 컬럼이 필요합니다.")
            else:
                st.info("성적 관련 컬럼을 찾을 수 없습니다. 'score'가 포함된 컬럼명을 사용해주세요.")
        
        with col2:
            st.subheader("📋 데이터 요약")
            
            # 기본 통계
            st.write("**📊 기본 통계**")
            st.write(f"• 총 학생 수: {len(student_df)}명")
            st.write(f"• 데이터 컬럼 수: {len(student_df.columns)}개")
            
            # 성적 통계
            if score_cols:
                st.write("**📈 성적 통계**")
                for col in score_cols:
                    subject_name = col.replace('_score', '').replace('_', ' ').title()
                    avg_score = student_df[col].mean()
                    max_score = student_df[col].max()
                    min_score = student_df[col].min()
                    
                    st.write(f"• {subject_name}: 평균 {avg_score:.1f}점 (최고 {max_score}점, 최저 {min_score}점)")
            
            # 출석률 통계
            attendance_cols = [col for col in student_df.columns if 'attendance' in col.lower()]
            if attendance_cols:
                for col in attendance_cols:
                    avg_attendance = student_df[col].mean()
                    st.write(f"**📅 {col}**: 평균 {avg_attendance:.1f}%")
            
            # 학습 시간 통계
            time_cols = [col for col in student_df.columns if 'time' in col.lower() or 'hour' in col.lower()]
            if time_cols:
                for col in time_cols:
                    avg_time = student_df[col].mean()
                    st.write(f"**⏰ {col}**: 평균 {avg_time:.1f}시간")
    
    # 탭 3: AI 개인 분석
    with tab3:
        st.header("🤖 AI 개인 분석")
        st.markdown("AI가 개별 학생을 분석하고 맞춤형 조언을 제공합니다!")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎯 학생 선택")
            
            # 학생 선택
            if 'name' in student_df.columns:
                student_names = student_df['name'].tolist()
            else:
                student_names = [f"학생 {i+1}" for i in range(len(student_df))]
            
            selected_student = st.selectbox(
                "분석할 학생을 선택하세요:",
                student_names
            )
            
            if selected_student:
                # 선택된 학생 데이터
                if 'name' in student_df.columns:
                    student_data = student_df[student_df['name'] == selected_student].iloc[0]
                else:
                    student_data = student_df.iloc[student_names.index(selected_student)]
                
                # 학생 정보 표시
                st.write(f"**📚 {selected_student} 학생 정보**")
                
                # 기본 정보
                info_cols = ['age', 'grade', 'gender']
                for col in info_cols:
                    if col in student_data:
                        st.write(f"• {col}: {student_data[col]}")
                
                # 성적 정보
                if score_cols:
                    st.write("**📊 과목별 성적**")
                    for col in score_cols:
                        if col in student_data:
                            score = student_data[col]
                            if score >= 90:
                                color = "🟢"
                            elif score >= 80:
                                color = "🟡"
                            elif score >= 70:
                                color = "🟠"
                            else:
                                color = "🔴"
                            subject_name = col.replace('_score', '').replace('_', ' ').title()
                            st.write(f"{color} {subject_name}: {score}점")
                
                # 추가 정보
                additional_cols = [col for col in student_df.columns if col not in info_cols + score_cols]
                for col in additional_cols:
                    if col in student_data:
                        st.write(f"• {col}: {student_data[col]}")
        
        with col2:
            st.subheader("🤖 AI 분석 요청")
            
            # 분석 유형 선택
            analysis_type = st.selectbox(
                "분석 유형을 선택하세요:",
                ["전체 성적 분석", "학습 스타일 분석", "개선 방안 제시", "맞춤형 학습 계획"]
            )
            
            if st.button("🚀 AI 분석 시작"):
                try:
                    with st.spinner("AI가 분석 중..."):
                        # 분석 유형에 따른 프롬프트 생성
                        if analysis_type == "전체 성적 분석":
                            prompt = f"""
다음 학생의 전체적인 성적을 분석해주세요.

**학생 정보:**
{json.dumps(student_data.to_dict(), ensure_ascii=False, indent=2)}

**분석 요청:**
1. 전체적인 성적 수준 평가
2. 강점과 약점 과목 분석
3. 성적 패턴 및 특징

**응답 형식:**
{{
    "overall_assessment": "전체적인 성적 수준 (상/중/하)",
    "strengths": ["강점 과목들"],
    "weaknesses": ["약점 과목들"],
    "patterns": ["성적 패턴 및 특징"],
    "summary": "전체적인 평가 요약"
}}

반드시 JSON 형식으로만 응답하세요.
"""
                        elif analysis_type == "학습 스타일 분석":
                            prompt = f"""
다음 학생의 학습 스타일과 성격을 분석해주세요.

**학생 정보:**
{json.dumps(student_data.to_dict(), ensure_ascii=False, indent=2)}

**분석 요청:**
1. 학습 스타일과 성격의 연관성
2. 현재 학습 방법의 적합성
3. 학습 효율성 향상 방안

**응답 형식:**
{{
    "learning_style_analysis": "학습 스타일 분석 결과",
    "personality_insights": "성격과 학습의 연관성",
    "current_methods": "현재 학습 방법 평가",
    "improvement_suggestions": ["학습 효율성 향상 방안"]
}}

반드시 JSON 형식으로만 응답하세요.
"""
                        elif analysis_type == "개선 방안 제시":
                            prompt = f"""
다음 학생의 성적 개선을 위한 구체적인 방안을 제시해주세요.

**학생 정보:**
{json.dumps(student_data.to_dict(), ensure_ascii=False, indent=2)}

**분석 요청:**
1. 약점 과목별 구체적 개선 방안
2. 학습 시간 활용 최적화
3. 동기부여 및 관리 방안

**응답 형식:**
{{
    "subject_improvements": {{"과목명": "개선 방안"}},
    "time_optimization": "학습 시간 활용 방안",
    "motivation_strategies": ["동기부여 전략"],
    "monitoring_plan": "진행 상황 모니터링 방법"
}}

반드시 JSON 형식으로만 응답하세요.
"""
                        else:  # 맞춤형 학습 계획
                            prompt = f"""
다음 학생을 위한 맞춤형 학습 계획을 수립해주세요.

**학생 정보:**
{json.dumps(student_data.to_dict(), ensure_ascii=False, indent=2)}

**분석 요청:**
1. 개인별 맞춤 학습 전략
2. 주간/월간 학습 계획
3. 목표 설정 및 달성 방안

**응답 형식:**
{{
    "personalized_strategy": "개인별 맞춤 전략",
    "weekly_plan": "주간 학습 계획",
    "monthly_goals": "월간 목표 설정",
    "achievement_methods": ["목표 달성 방안"]
}}

반드시 JSON 형식으로만 응답하세요.
"""
                        
                        # AI 분석 요청
                        response = openai.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "당신은 교육 전문가입니다. 학생 데이터를 분석하여 구체적이고 실용적인 조언을 제공하세요. 반드시 JSON 형식으로만 응답하세요."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.3,
                            max_tokens=800
                        )
                        
                        ai_response = response.choices[0].message.content
                        
                        # JSON 파싱 시도
                        try:
                            parsed_response = json.loads(ai_response)
                            st.success("✅ AI 분석이 완료되었습니다!")
                            
                            # 분석 결과 표시
                            st.subheader("📊 AI 분석 결과")
                            st.json(parsed_response)
                            
                            # 주요 결과 하이라이트
                            st.markdown("---")
                            st.subheader("🎯 주요 결과")
                            
                            for key, value in parsed_response.items():
                                if isinstance(value, list):
                                    st.write(f"**{key}:**")
                                    for item in value:
                                        st.write(f"• {item}")
                                elif isinstance(value, dict):
                                    st.write(f"**{key}:**")
                                    for sub_key, sub_value in value.items():
                                        st.write(f"  - {sub_key}: {sub_value}")
                                else:
                                    st.write(f"**{key}:** {value}")
                            
                        except json.JSONDecodeError:
                            st.warning("⚠️ AI 응답이 JSON 형식이 아닙니다.")
                            st.info("AI 응답을 JSON 형식으로 변환해보겠습니다...")
                            
                            # AI 응답을 JSON으로 변환 시도
                            try:
                                # 간단한 텍스트 정리
                                cleaned_response = ai_response.strip()
                                if cleaned_response.startswith('```json'):
                                    cleaned_response = cleaned_response[7:]
                                if cleaned_response.endswith('```'):
                                    cleaned_response = cleaned_response[:-3]
                                
                                # 다시 파싱 시도
                                parsed_response = json.loads(cleaned_response.strip())
                                st.success("✅ JSON 형식으로 변환되었습니다!")
                                
                                st.subheader("📊 AI 분석 결과")
                                st.json(parsed_response)
                                
                            except:
                                st.error("JSON 변환에 실패했습니다.")
                                st.subheader("📝 원본 AI 응답")
                                st.code(ai_response, language="text")
                                
                except Exception as e:
                    st.error(f"AI 분석 중 오류가 발생했습니다: {e}")
    
    # 탭 4: AI 교육 전략
    with tab4:
        st.header("🎯 AI 교육 전략")
        st.markdown("AI가 전체 학급을 분석하여 교육 전략을 제시합니다!")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📊 학급 전체 분석")
            
            # 분석 유형 선택
            class_analysis_type = st.selectbox(
                "학급 분석 유형을 선택하세요:",
                ["성적 분포 분석", "학습 스타일 분포", "개선 우선순위", "교육 전략 수립"]
            )
            
            if st.button("🎯 학급 분석 시작"):
                try:
                    with st.spinner("AI가 학급을 분석 중..."):
                        # 학급 데이터 요약
                        class_summary = {
                            "total_students": len(student_df),
                            "score_columns": score_cols,
                            "average_scores": {},
                            "columns": list(student_df.columns)
                        }
                        
                        # 과목별 평균 성적 계산
                        for col in score_cols:
                            class_summary["average_scores"][col] = student_df[col].mean()
                        
                        # 출석률과 학습시간 추가
                        attendance_cols = [col for col in student_df.columns if 'attendance' in col.lower()]
                        time_cols = [col for col in student_df.columns if 'time' in col.lower() or 'hour' in col.lower()]
                        
                        if attendance_cols:
                            class_summary["attendance_rate"] = student_df[attendance_cols[0]].mean()
                        if time_cols:
                            class_summary["study_time"] = student_df[time_cols[0]].mean()
                        
                        # 분석 유형에 따른 프롬프트 생성
                        if class_analysis_type == "성적 분포 분석":
                            prompt = f"""
다음 학급의 성적 분포를 분석하고 교육적 인사이트를 도출해주세요.

**학급 정보:**
{json.dumps(class_summary, ensure_ascii=False, indent=2)}

**분석 요청:**
1. 과목별 성적 분포 특징
2. 성적 격차 및 균형성 분석
3. 학급 전체의 강점과 약점

**응답 형식:**
{{
    "subject_analysis": {{"과목명": "분석 결과"}},
    "performance_gaps": "성적 격차 분석",
    "class_strengths": ["학급 전체 강점"],
    "class_weaknesses": ["학급 전체 약점"],
    "educational_insights": ["교육적 인사이트"]
}}

반드시 JSON 형식으로만 응답하세요.
"""
                        elif class_analysis_type == "학습 스타일 분포":
                            prompt = f"""
다음 학급의 학습 스타일 분포를 분석해주세요.

**학급 정보:**
{json.dumps(class_summary, ensure_ascii=False, indent=2)}

**분석 요청:**
1. 학습 스타일별 분포 현황
2. 성격과 학습 스타일의 연관성
3. 다양한 학습 스타일을 고려한 교육 방안

**응답 형식:**
{{
    "learning_style_distribution": "학습 스타일 분포 현황",
    "personality_correlations": "성격과 학습 스타일 연관성",
    "diverse_teaching_methods": ["다양한 학습 스타일을 위한 교육 방안"],
    "individual_attention": "개별 학생 맞춤 접근법"
}}

반드시 JSON 형식으로만 응답하세요.
"""
                        elif class_analysis_type == "개선 우선순위":
                            prompt = f"""
다음 학급의 개선 우선순위를 설정해주세요.
반드시 한국어로 대답하세요.

**학급 정보:**
{json.dumps(class_summary, ensure_ascii=False, indent=2)}

**분석 요청:**
1. 과목별 개선 우선순위
2. 학생 그룹별 맞춤 전략
3. 단기/장기 개선 목표

**응답 형식:**
{{
    "subject_priorities": ["과목별 개선 우선순위"],
    "student_group_strategies": "학생 그룹별 전략",
    "short_term_goals": ["단기 개선 목표"],
    "long_term_goals": ["장기 개선 목표"],
    "implementation_plan": "구현 계획"
}}

반드시 JSON 형식으로만 응답하세요.
"""
                        else:  # 교육 전략 수립
                            prompt = f"""
다음 학급을 위한 종합적인 교육 전략을 수립해주세요.

**학급 정보:**
{json.dumps(class_summary, ensure_ascii=False, indent=2)}

**분석 요청:**
1. 학급 전체 교육 방향
2. 과목별 교수법 개선
3. 학생 참여 및 동기부여 전략

**응답 형식:**
{{
    "overall_education_direction": "학급 전체 교육 방향",
    "subject_teaching_improvements": "과목별 교수법 개선",
    "student_engagement_strategies": ["학생 참여 전략"],
    "motivation_enhancement": "동기부여 향상 방안",
    "monitoring_and_evaluation": "모니터링 및 평가 방법"
}}

반드시 JSON 형식으로만 응답하세요.
"""
                        
                        # AI 분석 요청
                        response = openai.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "당신은 교육 전문가입니다. 학급 전체를 분석하여 체계적이고 실용적인 교육 전략을 제시하세요. 반드시 JSON 형식으로만 응답하세요."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.3,
                            max_tokens=1000
                        )
                        
                        ai_response = response.choices[0].message.content
                        
                        # JSON 파싱 시도
                        try:
                            parsed_response = json.loads(ai_response)
                            st.success("✅ 학급 분석이 완료되었습니다!")
                            
                            # 분석 결과 표시
                            st.subheader("📊 학급 분석 결과")
                            st.json(parsed_response)
                            
                            # 주요 결과 하이라이트
                            st.markdown("---")
                            st.subheader("🎯 주요 전략")
                            
                            for key, value in parsed_response.items():
                                if isinstance(value, list):
                                    st.write(f"**{key}:**")
                                    for item in value:
                                        st.write(f"• {item}")
                                elif isinstance(value, dict):
                                    st.write(f"**{key}:**")
                                    for sub_key, sub_value in value.items():
                                        st.write(f"  - {sub_key}: {sub_value}")
                                else:
                                    st.write(f"**{key}:** {value}")
                            
                        except json.JSONDecodeError:
                            st.warning("⚠️ AI 응답이 JSON 형식이 아닙니다.")
                            st.info("AI 응답을 JSON 형식으로 변환해보겠습니다...")
                            
                            # AI 응답을 JSON으로 변환 시도
                            try:
                                # 간단한 텍스트 정리
                                cleaned_response = ai_response.strip()
                                if cleaned_response.startswith('```json'):
                                    cleaned_response = cleaned_response[7:]
                                if cleaned_response.endswith('```'):
                                    cleaned_response = cleaned_response[:-3]
                                
                                # 다시 파싱 시도
                                parsed_response = json.loads(cleaned_response.strip())
                                st.success("✅ JSON 형식으로 변환되었습니다!")
                                
                                st.subheader("📊 학급 분석 결과")
                                st.json(parsed_response)
                                
                            except:
                                st.error("JSON 변환에 실패했습니다.")
                                st.subheader("📝 원본 AI 응답")
                                st.code(ai_response, language="text")
                                
                except Exception as e:
                    st.error(f"학급 분석 중 오류가 발생했습니다: {e}")
        
        with col2:
            st.subheader("💡 교육 전략 활용법")
            st.markdown("""
            **📊 데이터 기반 의사결정**
            - AI 분석 결과를 바탕으로 교육 방향 설정
            - 개별 학생과 전체 학급의 균형 고려
            
            **🎯 맞춤형 접근법**
            - 학습 스타일별 차별화된 교수법 적용
            - 성적 수준에 따른 단계별 학습 지원
            
            **🔄 지속적 모니터링**
            - 정기적인 데이터 수집 및 분석
            - 교육 전략의 효과 측정 및 개선
            """)
            
            st.subheader("🔧 실습 과제")
            st.markdown("""
            **🎯 과제 1: 데이터 시각화 마스터**
            - 다양한 차트 타입으로 데이터 분석
            - 시각화 결과의 교육적 의미 해석
            
            **🎯 과제 2: AI 분석 결과 활용**
            - AI 제안을 바탕으로 구체적 교육 계획 수립
            - 개별 학생과 전체 학급의 균형점 찾기
            
            **🎯 과제 3: 교육 전략 설계**
            - AI 분석 결과를 바탕으로 한 종합 교육 전략 수립
            - 실행 가능한 구체적 행동 계획 작성
            """)

# 실습 과제
st.markdown("---")
st.header("💡 실습 과제")

col3, col4 = st.columns([1, 1])

with col3:
    st.subheader("🎯 과제 1: 데이터 탐색 마스터")
    st.markdown("""
    **목표**: 다양한 차트로 학생 데이터 분석하기
    
    **실험 방법**:
    1. 여러 차트 타입으로 같은 데이터 시각화
    2. 각 차트가 보여주는 정보의 차이점 파악
    3. 교육적 관점에서 차트 결과 해석하기
    
    **예시**:
    - 막대 차트 vs 박스 플롯으로 성적 분포 비교
    - 산점도로 과목 간 상관관계 분석
    - 히스토그램으로 전체 성적 분포 파악
    """)

with col4:
    st.subheader("🎯 과제 2: AI 분석 활용하기")
    st.markdown("""
    **목표**: AI 분석 결과를 교육에 적용하기
    
    **실험 방법**:
    1. 다양한 분석 유형으로 같은 학생 분석
    2. AI 제안을 바탕으로 구체적 교육 계획 수립
    3. 개별 학생과 전체 학급의 균형점 찾기
    
    **예시**:
    - 개인별 맞춤 학습 계획 수립
    - 학급 전체 교육 전략 설계
    - 성적 개선을 위한 구체적 행동 계획
    """)

# 다음 강의 예고
st.markdown("---")
st.markdown("""
### 📚 다음 강의 예고
**04강: AI 교육 콘텐츠 생성기**
- AI를 활용한 맞춤형 학습 자료 생성
- 개인별 난이도 조절 및 문제 출제
- 교육 콘텐츠의 자동화 및 개인화
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
