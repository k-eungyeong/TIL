# 2026-05-29
### 배운 내용
##### [ 1교시 ]  
```
# 매우 간단한 에이전트의 구조(노드함수 없음)

tools = [search_tool]   # 도구함수
agent = create_agent(  # Agent(대리인)
    model=llm,
    tools=tools,
    checkpointer=memory, 
    system_prompt="에이전트의 페르소나(persona)"  # person, personality, 성격, 특성
)
result = agent.invoke({
        "messages": [
            {"role": "user", "content": "이용자 프롬프트"}
        ]
    },
    config=config
)

# 도구(Tool)함수, 노드(Node)함수, 일반함수

# 다수개의 노드를 가진 에이전트
# Graph를 구성하는 노드(Node), 엣지(Edge)
# LangGraph : Node(함수), Edge(함수간 연결)
```

##### [ 2교시 ]  
```
# 도구(Tool)함수, 노드(Node)함수, 일반함수

# 다수개의 노드를 가진 에이전트
# Graph를 구성하는 노드(Node), 엣지(Edge)
# LangGraph : Node(함수), Edge(함수간 연결)

builder = StateGraph(State) # 랭체인에서 지원해주는 그래프 (StateGraph) `

builder.add_node("request_approval", request_approval_node)   # ("이름", 함수) = 이 이름으로 이 함수를 실행할 수 있다. 
builder.add_node("execute_task", execute_task_node)

# edge = 함수와 함수 연결 
builder.add_edge(START, "request_approval")
builder.add_edge("request_approval", "execute_task")          
builder.add_edge("execute_task", END)

graph = builder.compile(checkpointer=checkpointer)         # compile 하면 그래프 완성됨
result = graph.invoke((...))

# 노드함수의 규칙 - 파라미터 1개(State), return {} 
def send_email_node(state:MyState) -> dict                 # 밑 함수 내용은 임의로 작성(에이전트의 한 작업 단계)
                                                           # 파라미터에 state 하나만 와야 함
                                                           # 이메일을 보낸다 하면 이메일 전문 에이전트 활용
 # return {'key':'value'} -> 리턴된 dict는 State 오브젝트에 자동 저장(랭체인 프레임워크가 해줌) 

# 노드함수 : 에이전트의 작업 단계 (Step/Stage)
#   사용자 입력 
#   → [검색 노드]       : 검색 전문가 페르소나 지정
#   → [팩트체크 노드]    : 내용 검증 전문가 페르소나 지정
#   → [수정문 생성 노드]  : 내용 생성 전문가 페르소나 지정
#   → 최종 응답 

#  Multi Agents 
```
##### [ 3교시 ]  
```
"""
[기능 요약]
- LangGraph로 Multi-Agent 기반 팩트체크 워크플로우 구성
- Ollama 로컬 모델(Gemma 계열) 사용
- Tavily 검색 도구 사용
- 각 노드 함수 안에서 서로 다른 Persona Agent 실행
  1) 검색 전문가 Agent
  2) 팩트체크 전문가 Agent
  3) 오류 정정 전문가 Agent
"""

import os
from typing import TypedDict, List, Dict, Any

from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()


# =========================
# 1. 환경 설정
# =========================

#os.environ["TAVILY_API_KEY"] = "여기에_TAVILY_API_KEY_입력"

llm = ChatOllama(
    model="gemma4:e4b",   # 실제 Ollama에 설치된 모델명과 일치해야 함
    temperature=0
)

search_tool = TavilySearch(
    max_results=5,
    topic="general"
)


# =========================
# 2. State 정의
# =========================

class FactCheckState(TypedDict):
    user_text: str
    search_result: str
    factcheck_result: str
    corrected_text: str
    final_answer: str


# =========================
# 3. Persona Agent 생성
# =========================

search_agent = create_agent(
    model=llm,
    tools=[search_tool],
    system_prompt="""
당신은 검색 전문가입니다.

역할:
- 사용자가 입력한 문장에서 검증이 필요한 사실 주장들을 파악합니다.
- 각 주장에 대해 신뢰 가능한 웹 자료를 검색합니다.
- 최소 5개 이상의 검색 근거를 확보하려고 노력합니다.
- 검색 결과는 출처, 핵심 내용, 검증 대상 주장과의 관련성을 중심으로 정리합니다.

주의:
- 추측하지 마세요.
- 검색 결과가 부족하면 '근거 부족'이라고 표시하세요.
"""
)

factcheck_agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="""
당신은 매우 엄격한 팩트체크 전문가입니다.

역할:
- 사용자의 원문과 검색 결과를 비교합니다.
- 사실적 오류, 과장, 근거 부족, 날짜 오류, 수치 오류를 찾아냅니다.
- 각 항목마다 다음 형식으로 판단합니다.

출력 형식:
1. 원문 주장:
2. 판단:
   - 사실
   - 부분적으로 사실
   - 사실 오류
   - 근거 부족
3. 문제점:
4. 근거 요약:
5. 정정 방향:

주의:
- 검색 근거에 없는 내용은 단정하지 마세요.
- 애매하면 '근거 부족'으로 분류하세요.
"""
)

rewrite_agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="""
당신은 사실 오류를 정정하는 전문 편집자입니다.

역할:
- 팩트체크 결과를 바탕으로 사용자의 원문을 정확하게 수정합니다.
- 과장된 표현은 중립적으로 바꿉니다.
- 근거가 부족한 내용은 단정 표현을 피합니다.
- 최종 수정문은 자연스럽고 읽기 쉽게 작성합니다.

출력 형식:
[수정된 문장]

[수정 요약]
- 무엇을 고쳤는지 bullet로 정리
"""
)


# =========================
# 4. Node 함수 정의
# =========================

def search_node(state: FactCheckState) -> Dict[str, Any]:
    user_text = state["user_text"]

    result = search_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
다음 텍스트에서 사실 검증이 필요한 주장들을 찾고,
각 주장에 대해 웹 검색을 수행하세요.

검증 대상 텍스트:
{user_text}
"""
            }
        ]
    })

    return {
        "search_result": str(result["messages"][-1].content)
    }


def factcheck_node(state: FactCheckState) -> Dict[str, Any]:
    user_text = state["user_text"]
    search_result = state["search_result"]

    result = factcheck_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
아래 원문과 검색 결과를 비교하여 사실적 오류를 검토하세요.

[원문]
{user_text}

[검색 결과]
{search_result}
"""
            }
        ]
    })

    return {
        "factcheck_result": str(result["messages"][-1].content)
    }


def rewrite_node(state: FactCheckState) -> Dict[str, Any]:
    user_text = state["user_text"]
    factcheck_result = state["factcheck_result"]

    result = rewrite_agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": f"""
아래 팩트체크 결과를 반영하여 원문을 수정하세요.

[원문]
{user_text}

[팩트체크 결과]
{factcheck_result}
"""
            }
        ]
    })

    return {
        "corrected_text": str(result["messages"][-1].content)
    }


def final_node(state: FactCheckState) -> Dict[str, Any]:
    final_answer = f"""
# 팩트체크 결과

## 1. 검색 결과 요약
{state["search_result"]}

---

## 2. 사실 오류 분석
{state["factcheck_result"]}

---

## 3. 오류 정정 문안
{state["corrected_text"]}
"""

    return {
        "final_answer": final_answer
    }


# =========================
# 5. LangGraph 구성
# =========================

graph_builder = StateGraph(FactCheckState)

graph_builder.add_node("search_node", search_node)
graph_builder.add_node("factcheck_node", factcheck_node)
graph_builder.add_node("rewrite_node", rewrite_node)
graph_builder.add_node("final_node", final_node)

graph_builder.add_edge(START, "search_node")
graph_builder.add_edge("search_node", "factcheck_node")
graph_builder.add_edge("factcheck_node", "rewrite_node")
graph_builder.add_edge("rewrite_node", "final_node")
graph_builder.add_edge("final_node", END)

app = graph_builder.compile()


# =========================
# 6. 실행 예시
# =========================

if __name__ == "__main__":
    user_input = """
대한민국의 수도는 부산이며, 2024년 기준 한국의 인구는 1억 명을 넘었다.
또한 서울은 2020년에 처음으로 특별시가 되었다.
"""

    result = app.invoke({
        "user_text": user_input,
        "search_result": "",
        "factcheck_result": "",
        "corrected_text": "",
        "final_answer": ""
    })

    print(result["final_answer"])
```

##### [ 4교시 ]  
* 5/28일자 복습
```
"""
LangGraph interrupt + checkpoint + thread_id 예제
- 위험 작업 전 사용자 승인을 요청하고 실행을 중단
- thread_id 기준으로 상태를 저장
- Command(resume=...)으로 승인 결과를 넣어 실행 재개
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


class State(TypedDict):
    task: str
    approved: bool
    result: str


def request_approval_node(state: State): # 작업 승인 요청 노드, 그래프를 구성하는 하나의 노드 함수

    # 승인을 구하기 위한 이메일 전송작업이 이자리에 올 수 있다

    approval = interrupt({                    # 그래프 중지됨
        "message": "이 작업을 승인하시겠습니까?",
        "task": state["task"],
        "expected_reply": "yes 또는 no"
    })

    return {
        "approved": approval == "yes"
    }


def execute_task_node(state: State):
    if not state["approved"]:
        return {
            "result": "사용자가 작업을 거절했습니다."
        }

    return {
        "result": f"승인되어 작업을 실행했습니다: {state['task']}"
    }


builder = StateGraph(State)

builder.add_node("request_approval", request_approval_node)
builder.add_node("execute_task", execute_task_node)

builder.add_edge(START, "request_approval")
builder.add_edge("request_approval", "execute_task")
builder.add_edge("execute_task", END)


# 상태 저장소 / checkpointer
checkpointer = InMemorySaver()

graph = builder.compile(checkpointer=checkpointer)


# 같은 thread_id를 사용해야 중단된 지점부터 재개 가능
config = {
    "configurable": {
        "thread_id": "approval-thread-001"
    }
}


# 1차 실행: interrupt에서 멈추고 interrupt 메시지 반환
result = graph.invoke(
    {   #승인을 받기 전의 현재 상태를 나타내는 dict, 리턴값에 포함됨, DB에 현재 상태를 저장할 때 유용함
        "task": "고객 DB의 특정 데이터를 수정하는 작업",   
        "approved": False,
        "result": ""
    },
    config=config
)

print("1차 실행 결과:")
print(result)
if "__interrupt__" in result:
    print("\n작업이 중단되었습니다. 승인 요청 메시지를 확인하세요.")

# interrupt 메시지 확인
print("\n승인 요청 내용:")
print(result["__interrupt__"])

# 그래프 외부에서 사용자 승인 시뮬레이션
permit = input("승인은 yes, 거절은 no를 입력하고 Enter를 눌러주세요...")
permit = permit.strip().lower()


# 2차 실행: 사용자가 이메일/콘솔/웹에서 승인했다고 가정
resume_result = graph.invoke(  # 최종 노드에서 저장된 state 의 내용이 리턴됨
    Command(resume=permit),
    config=config
)

print("\n재개 후 결과:")
print(resume_result)
```

### 어려운 점
### 느낀 점
