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
# 이 부분이 추가되어야 vectorstore를 사용할 수 있음.
vectorstore = Chroma(
    persist_directory="./chroma_db",  
    embedding_function=embeddings    
)


# 3. 검색기(Retriever) 설정
# 벡터 DB에 임베딩이 포함되어 있음
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) 


# 4. Gemma 모델 설정 
llm = ChatOllama(model="gemma4e4b") 
#llm = ChatOllama(model="gemma2:2b")


# 5. 문맥 유지를 위한 프롬프트 수정
contextual_prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 주어진 문맥(context)만을 바탕으로 질문에 답하는 어시스턴트입니다."), 
    MessagesPlaceholder(variable_name="chat_history"), 
    ("human", "Context: {context}\n\nQuestion: {question}"),   
])   

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs) 


# 대화 기록을 저장할 리스트 (메모리 역할)
chat_history = [] # 리스트 준비

def ask_question(question):  
    global chat_history      # global : 함수 밖에서 선언된 변수를 함수 안에서 사용할 때 필요한 선언(키워드)
    
    # 수정된 RAG 체인 구성
    rag_chain = (
        { "context": (lambda x: x["question"]) | retriever | format_docs,  
            "question": lambda x: x["question"],                          
            "chat_history": lambda x: x["chat_history"]                     
        }
        | contextual_prompt    
        | llm                   
        | StrOutputParser()     
    )
    
    # 호출
    response = rag_chain.invoke({  
        "question": question,
        "chat_history": chat_history
    })

    
    # 기록 업데이트. 질문과 답변을 대화 기록에 추가하여 다음 질문에서도 문맥으로 활용할 수 있도록 함
    chat_history.append(HumanMessage(content=question))   # 이용자 질문을 대화 기록에 추가
    chat_history.append(AIMessage(content=response))      # 모델의 답변을 대화 기록에 추가
    
    return response    # 최종적으로 모델의 응답을 반환 (이 함수의 출력이 이용자에게 보여지는 답변이 됨)

# 6. 문맥 유지 테스트 시나리오
print("--- 첫 번째 질문 ---")
print(ask_question("감자튀김은 왜 눅눅해질까?"))  

print("\n--- 두 번째 질문 (문맥 유지 테스트) ---")

print(ask_question("감자의 종류가 무엇인가?")) 

print("\n--- 세 번째 질문 (문맥 유지 테스트) ---")

print(ask_question("다시 데우는 방법은?"))
