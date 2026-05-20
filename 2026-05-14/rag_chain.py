from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


# 1. 임베딩 모델 설정 (2단계와 동일해야 함)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 2. 저장된 벡터 DB 불러오기 (2단계에서 지정한 경로)
vectorstore = Chroma(
    persist_directory="./chroma_db", 
    embedding_function=embeddings
)

# 3. 검색기(Retriever) 설정
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 4. Gemma 모델 설정 (ollama list에서 확인한 정확한 이름 입력)
llm = ChatOllama(model="gemma4e4b")
#llm = ChatOllama(model="gemma2:9b")  

# 5. 프롬프트 및 체인 구성
template = """당신은 주어진 문맥(context)만을 바탕으로 질문에 답하는 어시스턴트입니다.
#Context: 
{context}       
#Question:
{question}       
#Answer:"""     

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}

    | prompt  
    | llm     
    | StrOutputParser()   
)

# 6. 실행
print("질문하는 중...")

# 체인 실행 : 모든 과정이 순차적으로 자동 실행되어 최종 답변을 반환
print(rag_chain.invoke("문서의 주요 내용을 알려줘"))
