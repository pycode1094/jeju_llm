from gpt_functions import get_current_time, tools, get_yf_stock_info, get_yf_stock_history, get_yf_stock_recommendations
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st
from collections import defaultdict

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def tool_list_to_tool_obj(tool_calls_chunk):
    """tool_calls_chunk를 올바른 형태로 변환하는 함수"""
    if not tool_calls_chunk:
        return {"tool_calls": []}
    
    # tool_calls를 인덱스별로 그룹화
    tool_calls_dict = defaultdict(lambda: {
        "id": None, 
        "function": {"arguments": "", "name": None}, 
        "type": "function"
    })

    for tool_call in tool_calls_chunk:
        index = tool_call.index
        
        # id 설정
        if tool_call.id is not None:
            tool_calls_dict[index]["id"] = tool_call.id

        # 함수 이름 설정
        if tool_call.function.name is not None:
            tool_calls_dict[index]["function"]["name"] = tool_call.function.name

        # 인수 누적 (여러 청크에서 나온 인수를 합침)
        if tool_call.function.arguments is not None:
            tool_calls_dict[index]["function"]["arguments"] += tool_call.function.arguments

    # 딕셔너리를 리스트로 변환
    tool_calls_list = list(tool_calls_dict.values())
    
    return {"tool_calls": tool_calls_list}

def get_ai_response(messages, tools=None, stream=True):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        stream=stream,
        messages=messages,
        tools=tools,
    )

    if stream: 
        for chunk in response:
            yield chunk
    else:
        return response

st.title("🔺 주식 투자 상담사") 

# 초기 메시지 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "너는 사용자를 도와주는 주식 투자 상담사야."}
    ]

# 대화 기록 출력
for msg in st.session_state.messages:
    if msg["role"] in ["assistant", "user"]:
        st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    # AI 응답 받기
    ai_response = get_ai_response(st.session_state.messages, tools=tools)
    
    content = ''
    tool_calls_chunk = []
    
    # 스트리밍 응답 처리
    with st.chat_message("assistant").empty():
        for chunk in ai_response:
            # content 처리
            if chunk.choices[0].delta.content:
                content_chunk = chunk.choices[0].delta.content
                print(content_chunk, end="")
                content += content_chunk
                st.markdown(content)
            
            # tool_calls 처리
            if chunk.choices[0].delta.tool_calls:
                tool_calls_chunk.extend(chunk.choices[0].delta.tool_calls)

    # tool_calls 처리
    if tool_calls_chunk:
        tool_obj = tool_list_to_tool_obj(tool_calls_chunk)
        tool_calls = tool_obj["tool_calls"]
        
        print(f"\n🔧 실행할 도구들: {len(tool_calls)}개")
        for i, tool_call in enumerate(tool_calls):
            print(f"  {i+1}. {tool_call['function']['name']}: {tool_call['function']['arguments']}")
        
        # 각 도구 실행
        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            tool_call_id = tool_call["id"]
            
            try:
                arguments = json.loads(tool_call["function"]["arguments"])
                
                if tool_name == "get_current_time":
                    func_result = get_current_time(timezone=arguments['timezone'])
                elif tool_name == "get_yf_stock_info":
                    func_result = get_yf_stock_info(ticker=arguments['ticker'])
                elif tool_name == "get_yf_stock_history":
                    func_result = get_yf_stock_history(
                        ticker=arguments['ticker'], 
                        period=arguments['period']
                    )
                elif tool_name == "get_yf_stock_recommendations":
                    func_result = get_yf_stock_recommendations(
                        ticker=arguments['ticker']
                    )
                else:
                    func_result = f"알 수 없는 도구: {tool_name}"
                
                # 함수 실행 결과를 대화 기록에 추가
                st.session_state.messages.append({
                    "role": "function",
                    "tool_call_id": tool_call_id,
                    "name": tool_name,
                    "content": func_result,
                })
                
                print(f"✅ {tool_name} 실행 완료")
                
            except Exception as e:
                print(f"❌ {tool_name} 실행 오류: {e}")
                func_result = f"도구 실행 중 오류 발생: {e}"
                
                st.session_state.messages.append({
                    "role": "function",
                    "tool_call_id": tool_call_id,
                    "name": tool_name,
                    "content": func_result,
                })

        # 도구 실행 후 AI에게 다시 응답 요청
        st.session_state.messages.append({
            "role": "system", 
            "content": "이제 주어진 결과를 바탕으로 답변할 차례다."
        })
        
        ai_response = get_ai_response(st.session_state.messages, tools=tools)
        content = ""
        
        with st.chat_message("assistant").empty():
            for chunk in ai_response:
                if chunk.choices[0].delta.content:
                    content_chunk = chunk.choices[0].delta.content
                    print(content_chunk, end='')
                    content += content_chunk
                    st.markdown(content)

    # 최종 응답을 대화 기록에 추가
    st.session_state.messages.append({
        "role": "assistant",
        "content": content
    })

    print(f"\n✅ AI 응답 완료: {len(content)}자")