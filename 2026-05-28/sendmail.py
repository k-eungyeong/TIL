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


def request_approval_node(state: State):
    approval = interrupt({
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


# 1차 실행: interrupt에서 멈춤
result = graph.invoke(
    {
        "task": "고객 DB의 특정 데이터를 수정하는 작업",
        "approved": False,
        "result": ""
    },
    config=config
)

print("1차 실행 결과:")
print(result)

# interrupt 메시지 확인
print("\n승인 요청 내용:")
print(result["__interrupt__"])

permit = input("승인은 yes, 거절은 no를 입력하고 Enter를 눌러주세요...")
permit = permit.strip().lower()


# 2차 실행: 사용자가 이메일/콘솔/웹에서 승인했다고 가정
resume_result = graph.invoke(
    Command(resume=permit),
    config=config
)

print("\n재개 후 결과:")
print(resume_result)
