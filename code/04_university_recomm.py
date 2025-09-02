# 🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨중요 구간: 데이터 전처리 🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()
# 페이지 설정
st.set_page_config(
    page_title="04강: 대학교 추천 시스템 - 방사형 차트 비교",
    page_icon="🎓",
    layout="wide"
)

# 제목
st.title("🎓 04강: 대학교 추천 시스템 - 방사형 차트 비교")
st.markdown("---")

# 사이드바 - 강의 내용
with st.sidebar:
    st.header("📚 강의 내용")
    st.markdown("""
    ### 🎯 학습 목표
    - 방사형 차트(radar chart) 활용법 배우기
    - 데이터 시각화를 통한 비교 분석
    - 현실적인 대학교 합격 가능성 평가
    
    ### 🔑 핵심 개념
    1. **방사형 차트**: 다차원 데이터를 2D로 표현하는 차트
    2. **데이터 정규화**: 서로 다른 스케일의 데이터를 비교 가능하게 만들기
    3. **합격 가능성**: 객관적 데이터를 바탕으로 한 현실적 평가
    """)

# 데이터 로드
@st.cache_data
def load_data():
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel('./code/student_data.xlsx', engine='openpyxl')
        print(f"✅ 엑셀 파일 로드 성공: {len(df)}명의 학생 데이터")
        return df
    except FileNotFoundError:
        print("❌ student_data.xlsx 파일을 찾을 수 없습니다. 샘플 데이터를 사용합니다.")
        # 샘플 데이터 생성
        data = {
            'student_id': ['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008', 'S009', 'S010'],
            'name': ['김민수', '이지은', '박준호', '최수진', '정현우', '한소영', '윤도현', '강미래', '임태호', '송하은'],
            'math_score': [85, 92, 75, 88, 95, 70, 82, 90, 68, 85],
            'korean_score': [92, 95, 68, 85, 78, 88, 75, 92, 72, 88],
            'english_score': [78, 89, 72, 92, 85, 75, 88, 85, 65, 90],
            'science_score': [88, 85, 80, 78, 92, 68, 85, 88, 70, 82],
            'social_score': [90, 87, 65, 82, 75, 85, 78, 90, 68, 85]
        }
        return pd.DataFrame(data)
    except Exception as e:
        print(f"❌ 엑셀 파일 로드 중 오류 발생: {e}")
        # 샘플 데이터 생성
        data = {
            'student_id': ['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008', 'S009', 'S010'],
            'name': ['김민수', '이지은', '박준호', '최수진', '정현우', '한소영', '윤도현', '강미래', '임태호', '송하은'],
            'math_score': [85, 92, 75, 88, 95, 70, 82, 90, 68, 85],
            'korean_score': [92, 95, 68, 85, 78, 88, 75, 92, 72, 88],
            'english_score': [78, 89, 72, 92, 85, 75, 88, 85, 65, 90],
            'science_score': [88, 85, 80, 78, 92, 68, 85, 88, 70, 82],
            'social_score': [90, 87, 65, 82, 75, 85, 78, 90, 68, 85]
        }
        return pd.DataFrame(data)

# 대학교 기준 데이터 (실제 입시 기준을 반영한 가상 데이터)
university_standards = {
    "서울대": {
        "math_score": 100, "korean_score": 100, "english_score": 100, 
        "science_score": 100, "social_score": 100, "total_score": 500,
        "description": "국내 최고 명문대학, 모든 과목에서 최상위권 성적 필요"
    },
    "고려대": {
        "math_score": 95, "korean_score": 92, "english_score": 95, 
        "science_score": 95, "social_score": 95, "total_score": 472,
        "description": "서울 상위권 명문대학, 균형잡힌 성적과 특별활동 중요"
    },
    "연세대": {
        "math_score": 100, "korean_score": 90, "english_score": 100, 
        "science_score": 95, "social_score": 80, "total_score": 465,
        "description": "서울 상위권 명문대학, 영어 성적과 종합적 역량 중시"
    },
    "서강대": {
        "math_score": 85, "korean_score": 88, "english_score": 90, 
        "science_score": 82, "social_score": 82, "total_score": 427,
        "description": "서울 상위권 대학, 실용적 학문과 창의성 중시"
    },
    "한양대": {
        "math_score": 82, "korean_score": 85, "english_score": 88, 
        "science_score": 80, "social_score": 80, "total_score": 415,
        "description": "서울 상위권 대학, 공학과 실무 중심 교육"
    },
    "성균관대": {
        "math_score": 88, "korean_score": 90, "english_score": 88, 
        "science_score": 85, "social_score": 85, "total_score": 436,
        "description": "서울 상위권 명문대학, 전통과 혁신의 조화"
    },
    "중앙대": {
        "math_score": 80, "korean_score": 82, "english_score": 85, 
        "science_score": 78, "social_score": 78, "total_score": 403,
        "description": "서울 상위권 대학, 예술과 미디어 분야 특화"
    },
    "경희대": {
        "math_score": 78, "korean_score": 80, "english_score": 82, 
        "science_score": 75, "social_score": 75, "total_score": 390,
        "description": "서울 상위권 대학, 평화와 인권의 가치 중시"
    },
    "한국외국어대": {
        "math_score": 75, "korean_score": 78, "english_score": 95, 
        "science_score": 72, "social_score": 72, "total_score": 392,
        "description": "언어학 특화 대학, 영어 성적과 외국어 능력 중시"
    },
    "서울시립대": {
        "math_score": 80, "korean_score": 82, "english_score": 80, 
        "science_score": 78, "social_score": 78, "total_score": 398,
        "description": "서울 공립대학, 도시 문제와 공공정책 연구"
    },
    "건국대": {
        "math_score": 75, "korean_score": 78, "english_score": 78, 
        "science_score": 72, "social_score": 72, "total_score": 375,
        "description": "서울 상위권 대학, 실용적 학문과 창의성 중시"
    },
    "동국대": {
        "math_score": 72, "korean_score": 75, "english_score": 75, 
        "science_score": 70, "social_score": 70, "total_score": 362,
        "description": "서울 상위권 대학, 불교 정신과 현대 교육의 조화"
    },
    "홍익대": {
        "math_score": 70, "korean_score": 72, "english_score": 72, 
        "science_score": 68, "social_score": 68, "total_score": 350,
        "description": "서울 상위권 대학, 예술과 디자인 분야 특화"
    }
}

# 데이터 로드
df = load_data()

# 메인 콘텐츠
col1, col2 = st.columns([1, 1])

with col1:
    st.header("👨‍🎓 학생 선택")
    
    # 학생 선택
    selected_student = st.selectbox(
        "분석할 학생을 선택하세요:",
        df['student_id'].tolist(),
        format_func=lambda x: f"{df[df['student_id']==x]['name'].iloc[0]} ({x})"
    )
    
    if selected_student:
        student_data = df[df['student_id'] == selected_student].iloc[0]
        
        st.subheader(f"📊 {student_data['name']} 학생 정보")
        st.markdown(f"**학번**: {student_data['student_id']}")
        st.markdown(f"**수학**: {student_data['math_score']}점")
        st.markdown(f"**국어**: {student_data['korean_score']}점")
        st.markdown(f"**영어**: {student_data['english_score']}점")
        st.markdown(f"**과학**: {student_data['science_score']}점")
        st.markdown(f"**사회**: {student_data['social_score']}점")
        
        # 총점 계산
        total_score = (student_data['math_score'] + student_data['korean_score'] + 
                      student_data['english_score'] + student_data['science_score'] + 
                      student_data['social_score'])
        st.markdown(f"**총점**: {total_score}점")

with col2:
    st.header("🏫 대학교 선택")
    
    # 대학교 선택
    selected_university = st.selectbox(
        "비교할 대학교를 선택하세요:",
        list(university_standards.keys())
    )
    
    if selected_university:
        univ_data = university_standards[selected_university]
        
        st.subheader(f"🎯 {selected_university} 입시 기준")
        st.markdown(f"**수학**: {univ_data['math_score']}점")
        st.markdown(f"**국어**: {univ_data['korean_score']}점")
        st.markdown(f"**영어**: {univ_data['english_score']}점")
        st.markdown(f"**과학**: {univ_data['science_score']}점")
        st.markdown(f"**사회**: {univ_data['social_score']}점")
        st.markdown(f"**총점 기준**: {univ_data['total_score']}점")
        st.markdown(f"**특징**: {univ_data['description']}")

# 방사형 차트 생성
if selected_student and selected_university:
    st.markdown("---")
    st.header("📈 과목별 성적 비교 (방사형 차트)")
    
    student_data = df[df['student_id'] == selected_student].iloc[0]
    univ_data = university_standards[selected_university]
    
    # 과목명과 점수 데이터
    subjects = ['수학', '국어', '영어', '과학', '사회']
    student_scores = [
        student_data['math_score'],
        student_data['korean_score'],
        student_data['english_score'],
        student_data['science_score'],
        student_data['social_score']
    ]
    univ_scores = [
        univ_data['math_score'],
        univ_data['korean_score'],
        univ_data['english_score'],
        univ_data['science_score'],
        univ_data['social_score']
    ]
    
    # 방사형 차트 생성
    fig = go.Figure()
    
    # 학생 점수 (파란색)
    fig.add_trace(go.Scatterpolar(
        r=student_scores,
        theta=subjects,
        fill='toself',
        name=f'{student_data["name"]} 학생',
        line_color='blue',
        fillcolor='rgba(0, 100, 255, 0.3)'
    ))
    
    # 대학교 기준 (빨간색)
    fig.add_trace(go.Scatterpolar(
        r=univ_scores,
        theta=subjects,
        fill='toself',
        name=f'{selected_university} 기준',
        line_color='red',
        fillcolor='rgba(255, 0, 0, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title=f"{student_data['name']} 학생 vs {selected_university} 입시 기준 비교"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 합격 가능성 분석
    st.markdown("---")
    st.header("🎯 합격 가능성 분석")
        
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.subheader("📊 과목별 달성도")
        
        # 과목별 달성도 계산
        math_ratio = (student_data['math_score'] / univ_data['math_score']) * 100
        korean_ratio = (student_data['korean_score'] / univ_data['korean_score']) * 100
        english_ratio = (student_data['english_score'] / univ_data['english_score']) * 100
        science_ratio = (student_data['science_score'] / univ_data['science_score']) * 100
        social_ratio = (student_data['social_score'] / univ_data['social_score']) * 100
        
        # 달성도 표시
        st.metric("수학", f"{math_ratio:.1f}%", f"{student_data['math_score']}/{univ_data['math_score']}")
        st.metric("국어", f"{korean_ratio:.1f}%", f"{student_data['korean_score']}/{univ_data['korean_score']}")
        st.metric("영어", f"{english_ratio:.1f}%", f"{student_data['english_score']}/{univ_data['english_score']}")
        st.metric("과학", f"{science_ratio:.1f}%", f"{student_data['science_score']}/{univ_data['science_score']}")
        st.metric("사회", f"{social_ratio:.1f}%", f"{student_data['social_score']}/{univ_data['social_score']}")
    
    with col4:
        st.subheader("🎯 종합 평가")
        
        # 총점 비교
        student_total = sum(student_scores)
        univ_total = univ_data['total_score']
        total_ratio = (student_total / univ_total) * 100
        
        st.metric("총점 달성도", f"{total_ratio:.1f}%", f"{student_total}/{univ_total}")
        
        # 합격 가능성 등급
        if total_ratio >= 95:
            grade = "🟢 매우 높음"
            description = "합격 가능성이 매우 높습니다. 안정권으로 분류됩니다."
        elif total_ratio >= 85:
            grade = "🟡 높음"
            description = "합격 가능성이 높습니다. 노력하면 충분히 합격할 수 있습니다."
        elif total_ratio >= 75:
            grade = "🟠 보통"
            description = "합격 가능성이 보통입니다. 추가 학습이 필요합니다."
        elif total_ratio >= 65:
            grade = "🔴 낮음"
            description = "합격 가능성이 낮습니다. 대폭적인 성적 향상이 필요합니다."
        else:
            grade = "⚫ 매우 낮음"
            description = "합격 가능성이 매우 낮습니다. 다른 대학교를 고려해보세요."
        
        st.markdown(f"**합격 가능성**: {grade}")
        st.markdown(f"**평가**: {description}")
        
        # 개선 방향 제안
        st.subheader("💡 개선 방향")
        
        # 가장 부족한 과목 찾기
        ratios = [math_ratio, korean_ratio, english_ratio, science_ratio, social_ratio]
        min_subject_idx = ratios.index(min(ratios))
        min_subject = subjects[min_subject_idx]
        min_ratio = min(ratios)
        
        if min_ratio < 80:
            st.warning(f"⚠️ {min_subject} 과목이 가장 부족합니다. ({min_ratio:.1f}%)")
            st.info(f"💪 {min_subject} 과목 집중 학습을 권장합니다.")
        
        if total_ratio < 85:
            st.info("📚 전반적인 성적 향상이 필요합니다. 기초부터 차근차근 학습하세요.")

# 실습 과제
st.markdown("---")
st.header("💡 실습 과제")

col5, col6 = st.columns([1, 1])

with col5:
    st.subheader("🎯 과제 1: 다양한 학생과 대학교 비교")
    st.markdown("""
    **목표**: 방사형 차트를 통해 다양한 패턴 분석하기
    
    **실험 방법**:
    1. 성적이 높은 학생과 낮은 학생 선택
    2. 같은 대학교와 비교해보기
    3. 차트의 모양과 합격 가능성 분석
    
    **분석 포인트**:
    - 어떤 과목이 가장 중요한가?
    - 균형잡힌 성적 vs 특정 과목 우수
    - 총점과 개별 과목의 관계
    """)

with col6:
    st.subheader("🎯 과제 2: 합격 전략 수립")
    st.markdown("""
    **목표**: 개인 맞춤형 입시 전략 수립하기
    
    **전략 수립**:
    1. 현재 부족한 과목 파악
    2. 목표 대학교의 기준점 확인
    3. 효율적인 학습 계획 수립
    
    **고려사항**:
    - 시간 투자 대비 성적 향상 효과
    - 과목별 난이도와 특성
    - 개인의 학습 스타일과 선호도
    """)

# 다음 강의 예고
st.markdown("---")
st.markdown("""
### 📚 다음 강의 예고
**05강: 데이터 분석과 시각화 심화**
- 다양한 차트 타입 활용법
- 인터랙티브 대시보드 만들기
- 데이터 기반 의사결정 시스템 구축
""")

# 참고사항
st.markdown("---")
st.info("""
**📝 참고사항**:
- 이 시스템은 가상의 데이터를 기반으로 합니다
- 실제 입시는 더 복잡한 요소들을 고려합니다
- 방사형 차트는 다차원 데이터 비교에 효과적입니다
- 합격 가능성은 객관적 데이터 기반으로 계산됩니다
""")
