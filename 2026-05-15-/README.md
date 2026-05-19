# 2026-05-15
## 목표 : RAG 시스템에서 문맥 유지하는 방법 (대화를 기억하는 RAG)
### 배운 내용
1. 문맥유지 (Context Retention)
   - Question : 이용자가 입력한 질문 텍스트
   - Context : 이용자의 질문을 벡터 DB에서 검색한 결과(Retriever 결과)
   - History : Question, Context를 기억하기 위해 필요(이전 대화의 기록)
     → 대화를 기억하는 것은 LLM의 일 X
2. 코드 최적화
   - Anaconda jupyter notebook 사용하기!
    : 셀 단위로 실행해서 이용자가 n을 요청하면 n을 돌리기 위해 필요한 작업들을 미리 셀로 돌려둘 수 있음, 즉 미리 메모리에 로드 가능 = 속도 향상
4. rag_contextualize.py 코드
   - 전체 흐름
    * 사용자 질문 → 이전 대화(chat_history) 불러오기 → Retriever 검색 → Context 생성 → Prompt에 history 포함 → LLM 답변 생성 → 대화기록 저장
   - 새로 등장한 것
    * HumanMessage, AIMessage : 대화를 사람메시지, AI메시지를 구분해서 저장
    * MessagesPlaceholder : Prompt 안에 chat_history 대화가 들어갈 자리 표시자
    * global : 함수 밖에 선언된 변수를 함수 안에서 참고하고자 할 때
    * lambda : 익명함수(짧게 쓰는 함수), 코드 내에서 → invoke 입력 딕셔너리에서 question 값만 꺼내 retriever에게 넘기기 위한 익명 함수
       해석 ex. lambda x : x["question"] => 함수 만들기, 입력값 : 반환값 
***************************************************   코드 해석 *************************************************
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import MessagesPlaceholder

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda


    # 1. 임베딩 모델 설정 (2단계와 동일해야 함)
embeddings = OllamaEmbeddings(model="nomic-embed-text")  

    # 2. 저장된 벡터 DB 불러오기 (2단계에서 지정한 경로)
                  이 부분이 추가되어야 vectorstore를 사용할 수 있음.
vectorstore = Chroma(
    persist_directory="./chroma_db",  
    embedding_function=embeddings         # 저장(벡터화)/검색(문자열화) 시 동일한 임베딩 모델을 사용해야 함
)

    # 3. 검색기(Retriever) 설정
                  벡터 DB에 임베딩이 포함되어 있음
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # 여기서 vertorstore이 vertor db임(위에서 선언함)
                                                             # 여기서 k는 하이퍼 파라미터 

    # 4. Gemma 모델 설정 (ollama list에서 확인한 정확한 이름 입력)
llm = ChatOllama(model="gemma4e4b") # 로컬시스템에서 ollama에 등록한 이름. ollama list 명령어로 확인 가능
#llm = ChatOllama(model="gemma2:2b")


    # 5. 문맥 유지를 위한 프롬프트 수정
contextual_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 주어진 문맥(context)만을 바탕으로 질문에 답하는 어시스턴트입니다."), # system은 컴퓨터(언어모델)을 의미/ 역할 배정하는 공간(롤 역할)
    
    MessagesPlaceholder(variable name="chat history"), # 대화기록이 들어갈 자리. 입력 딕셔너리에서 'chat_history' 키의 값이 여기에 들어감
    
    ("human", "Context: {context}\n\nQuestion: {question}"),   # question: 이용자 입력, context:retriever로 검색된 문서 내용
]) 

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs) # docs에 청크 3개(위에서 정함)이 들어감


            
chat_history = [] # 리스트 준비 > 대화 기록을 저장할 리스트_ 메모리 역할

def ask_question(question):  # question 문자열만 입력받도록 수정
    global chat_history      # global : 함수 밖에서 선언된 변수를 함수 안에서 사용할 때 필요한 선언(키워드)
                             #   = 지역 변수 X. global 하지 않으면 사용할 때마다 새로 만들어짐(대화누적 안 됨)
    
    # 수정된 RAG 체인 구성
    rag_chain = (
        {
            # 입력 딕셔너리에서 'question' 키의 값만 추출
            "context": (lambda x: x["question"]) | retriever | format_docs,  
                     # retriever는 question을 받아서 관련 문서를 검색, format_docs는 문서 내용을 하나의 문자열로 변환
                     # lambad란? 익명함수. 여기서 x는 함수의 파라미터 → 익명함수라 바로 파라미터가 나옴 
                     #          : 다음 x["question"]이 함수의 바디 부분. 즉, x 자리에 이용자의 질문이 들어옴
                     #          : 다음 retirever 은 벡터 DB에서 의미가 가장 유사한 청크 3개를 추출하고,
                     #          : 다음 format_docs 은 추출한 3개의 청크를 하나의 문자열로 만드는 것 
            "question": lambda x: x["question"],                             # 사용자 질문 그 자체
            "chat_history": lambda x: x["chat_history"]                      # 이전까지의 대화기록 그 자체
        }
        
        | contextual_prompt     # 프롬프트 완성 및 context, question, chat_history를 LLM에 전달
        | llm                   # LLM에서 답변 생성
        | StrOutputParser()     # 답변을 문자열로 파싱 (현재 체인이 실행되면 최종 출력은 LLM의 응답이 문자열로 반환됨)
    )
    
    # 호출 
    response = rag_chain.invoke({  # 입력 딕셔너리로 question과 chat_history 전달
        "question": question,
        "chat_history": chat_history
    })
    
    
    # 기록 업데이트. 질문과 답변을 대화 기록에 추가하여 다음 질문에서도 문맥으로 활용
    chat_history.append(HumanMessage(content=question))   # 이용자 질문을 대화 기록에 추가
    chat_history.append(AIMessage(content=response))      # 모델의 답변을 대화 기록에 추가
    
    return response    # 최종적으로 모델의 응답을 반환 (이 함수의 출력이 이용자에게 보여지는 답변이 됨)

     # 6. 문맥 유지 테스트 시나리오
print("--- 첫 번째 질문 ---")
print(ask_question("감자튀김은 왜 눅눅해질까?")) # 함수 호출할 때 키보드 값 받아와서 " " 안에 넣어주면 됨 

print("\n--- 두 번째 질문 (문맥 유지 테스트) ---")

print(ask_question("감자의 종류가 무엇인가?")) 

print("\n--- 세 번째 질문 (문맥 유지 테스트) ---")

print(ask_question("다시 데우는 방법은?"))
***************************************************************************************************************

### 어려웠던 점
- 데이터가 어디서 생성되고 어디서 흐르는가?
  : invoke 입력값 vs Prompt 최종 입력값
- lambda 역할
  : 코드 내에서의 단순 축약 담당 vs 데이터 가공 담당
- MessagesPlaceholder 의미
  : 처음엔 실제 역할과 다른 저장 공간 그 자체로 이해

  
### 느낀 점
LangChain을 처음 들었을 땐, 단순하게 "완성도 높은 문장을 위해 LLM을 중심으로 기능을 연결한다." 라고만 생각했었다.
하지만 전체적인 코드를 보면 가장 기본이 되는 틀이며 복잡한 구조를 띄고있다고 생각한다.
