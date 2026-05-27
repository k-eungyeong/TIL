# 2026-05-27
## 목표 : N교시별 작성
### 배운 내용
[ 1교시 ] AI-Agent의 도구(Tools)의 예
```
@tool
def send_email_tool(to)email: str, subject: str, body:str) -> str. # 함수의 헤드
	"""
	[doctring 역할]
	Gmail SMTP를 통해 이메일을 전송합니다.
	to_email: 수신자 주소, subject: 제목, body: 본문
	→ LLM에게 '이 툴이 무엇인지' 알림
	
	# 메일을 보내는 기능 구현 
	# try execpt...                                    # 에러 유무를 LLM이 알아야 해서
	# 메일 보내기 성공/실패 메시지를 문자열로 리턴         # 이 툴의 작업결과를 LLM에게 넣어줘(?)
	 
	 
	 Human_in-th
	
# AI-Agent의 역햘을 아래처럼 분명하게 지정
system_prompt - ""
[system_prompt의 역할]
사용자가 메일 전송을 요청하는 경우 반드시 send_email_tool을 호출
수신자/제목/본문 중 하나라도 빠지면 툴 호출 전 사용자에게 먼저 확인
→ LLM에게 "언제, 어떻게 툴을 써야 하는지" 지시 
	"""

http:/www.tavily.com/?utm_source=chatgpt.com 들어가서 AI-Agent 전용 검색 엔진 API
회원가입/API키 발급 -> 발급 후 한 번밖에 안 보여지니 메모해두기! 
```
아나콘다 프롬포트 > “pip install -U langgraph langchain langchain-ollama langchain-tavily python-dotenv”

[ 2교시 ]
- 환경변수(Environment Variables) : 운영체제가 사용하는 시스템 변수 
   - 개발자 코드에 포함하면 보안상 위험에 노출될 수도 있는 비번, API키 등을 코드에서 숨긴다
   - python-dotenv 모듈은 “.env” 안에 입력된 데이터를 운영체제의 환경변수에 저장해주는 기능
- API키는 환경변수에 등록하고, 개발자의 코드에서 필요시에는 OS의 환경변수에서 참조
```
import os
os.environ["TAVILY_API_KEY"] = "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"  # 발급받은 Tavily API Key
                                                          # 이런 역할을 dot + env가 해주는데 우리는 현재 수동으로 하고있음
                                                          # 이러면 다 보여! 보안상 안 돼! dotenv 파일을 써서 완저니 감춰

"""
import os
os.environ["TAVILY_API_KEY"] = "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"  # 발급받은 Tavily API Key
                                                          # 이런 역할을 dot + env가 해주는데 우리는 현재 수동으로 하고있음
                                                          # 이러면 다 보여! 보안상 안 돼! dotenv 파일을 써서 완저니 감춰

"""
LangGraph 기반 ReAct AI-Agent 예제
- Agent의 4가지 요소(Memory, Profile, Planning, Tools)를 모두 활용한 ReAct 에이전트 구현
- Ollama 로컬 모델 사용
- Gemma4:e4b 모델 (텍스트 생성, 검색 키워드 추출, 검색 결과 요약, 응답 생성, 도구 사용 판단, 반복 요구 등 다양한 역할 수행)
- ReAct 프레임워크로 검색과 응답을 반복하는 에이전트 구현 (system_prompt에 ReAct 행동 지침(반복여부) 포함). LLM이 반복 결정 -> LangGraph가 반복 실행 -> LLM이 종료 결정 -> 최종 답변 생성
- Tavily 웹 검색 Tool 사용
- LangChain create_agent는 내부적으로 LangGraph runtime을 사용
"""

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch

load_dotenv()  

# 1) Ollama LLM 설정
llm = ChatOllama(
    model="gemma4:e4b",
    temperature=0,       # 0: 완전 결정론적 응답(완전 사실만 받고싶다면), 0.7: 적당한 창의성, 1.0: 매우 창의적 응답
)

# 2) Tavily 검색 Tool 설정
# max_results는 검색 결과 개수. TavilySearch는 max_results, topic, search_depth 등을 지원.
search_tool = TavilySearch(  # TavilySearch는 랭체인에서 지원해줘서 쉽게 만들 수 있음(?)
    max_results=3,           # 사이트 3개에서 검색! 객관성을 띄워야 하니까 
    search_depth="basic",  # "basic"은 간단한 검색, "deep"은 더 많은 결과와 상세한 정보, "advanced"는 최대한 많은 결과와 상세한 정보 제공
)

tools = [search_tool]

# 3) ReAct Agent 생성
from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()  # LangGraph가 이전 대화 history를 자동으로 이어서 기억(이용자 메시지 + 에이전트 메시지 모두 저장) -> create_agent의 checkpointer로 전달하면 됨. 이후 대화에서 thread_id가 같으면 자동으로 이어서 기억

agent = create_agent(
    model=llm,
    tools=tools,
    checkpointer=memory,   # 에이전트의 상태를 저장하는 체크포인터
    system_prompt="""
당신은 정확한 정보를 제공하는 한국어 AI-Agent입니다.

목표:
사용자의 질문에 대해 최신성, 정확성, 근거가 충분한 답변을 제공하세요.

도구 사용 기준:
1. 최신 정보, 변경 가능성이 있는 정보, 불확실한 정보는 Tavily 검색 도구를 사용하세요.
2. 검색 결과가 부족하거나 서로 충돌하면 추가 검색을 수행하세요.
3. 답변에 필요한 핵심 근거가 확보될 때까지 검색과 분석을 반복하세요.
4. 충분한 근거가 확보되면 최종 답변을 작성하세요.
5. 근거가 부족하면 추측하지 말고 “확인된 정보가 부족하다”고 말하세요.
"""
)

# 4) 실행
config = {
    "configurable": {
        "thread_id": "user-001"    # 사용자별로 고유한 thread_id를 사용하여 대화 상태를 관리할 수 있음
    }
}

if __name__ == "__main__":
    """  스트리밍 방식이 아닌 호출: 
    question = "2026년 현재 LangGraph에서 ReAct Agent를 만드는 권장 방식은 무엇인가요?"

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    },
    config=config
)

    print(result["messages"][-1].content)
    """

    # 스트리밍 방식으로 실행하기 : 각 단계별로 출력 가능
    question = "오늘 기준 LangGraph와 LangChain Agent의 차이를 검색해서 설명해줘."
    for step in agent.stream(
        {
            "messages": [
                {"role": "user", "content": question}
            ]
        },
        config=config,
        stream_mode="values",  # "values"는 각 단계별로 출력, "final"은 최종 결과만 출력, "all"은 모든 단계의 메시지를 포함한 최종 결과 출력, "update"는 각 단계별로 업데이트된 메시지만 출력
    ):
        step["messages"][-1].pretty_print()
```
* 이용자가 찾고자 하는 내용 “AI-Agent라는 것이 무엇인지 그 개념을 설명하고 구성요소에는 무엇이 포함되는지 알려줘”
→ 젬마4에 해당 지식이 없다면 웹 검색 필요 → 키워드를 뽑아냄 ex. AI-Agent, 구성요소 → 키워드를 뽑아내는 건 LLM 담당 → Tavily 
→ 검색 텍스트 → LLM → 정리(완성된 문서로 리턴)


### 어려웠던 점
### 느낀 점
