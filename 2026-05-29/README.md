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

### 어려운 점
### 느낀 점
