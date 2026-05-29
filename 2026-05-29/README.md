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


### 어려운 점
### 느낀 점
