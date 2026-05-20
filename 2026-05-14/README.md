# 2026-05-14
## 목표
### 배운 내용
1. RAG Architecture Model
  - Client → Framework : 사용자 질문     *여기서 Framework란? ex. LangChain, FastAPI, Python 코드
  - Semantic Search    = 의미 검색
  - Contextual Data    = Vector DB에서 검색된 참고자료(데이터)     *본래 Cotextual은 문맥을 가르키지만, RAG에서는 데이터의 의미를 가짐
  - Prompt → LLM       : Framework가 사용자 질문 + Contextual Data로 Prompt 생성하면 검색된 자료를 읽고 자연스러운 답변을 LLM이 생성
  - Post Processing    = 답변 후 처리
<img width="663" height="326" alt="image" src="https://github.com/user-attachments/assets/3b556125-e918-4919-ac48-c86a8e9422b4" />


2. Embedding + Vector DB 검색과정
   2-1. Document Embedding (문서 저장 단계) : 문서를 검색 가능한 상태로 준비하는 과정 - Retrieval 준비 단계
   2-2. Query Embedding (사용자 질문 단계)  : 실제 질문이 들어왔을 때 검색 수행
* 문서와 사용자 질문을 각 임베딩할 때 같은 임베딩 모델 사용! → 같은 기준으로 벡터화해야 벡터 공간에서 의미비교 가능
<img width="637" height="316" alt="image" src="https://github.com/user-attachments/assets/1890fd8a-c780-4be5-bf94-e5f1fbc986a6" />


3. pdf_to_vectordb.py 코드
```
from langchain_community.document_loaders import PyPDFLoader             # PyPDFLoader는 PDF를 불러와서 쪼갠 다음 벡터 DB에 넣는다
from langchain_text_splitters import RecursiveCharacterTextSplitter      # 청크 생성
from langchain_ollama import OllamaEmbeddings                            # 임베딩 모델을 사용해주는 것
from langchain_community.vectorstores import Chroma                      # 랭체인 모듈만 갖고 있으면 벡터 DB 생성 가능

# 1. 문서 불러오기 (PDF 예시)
loader = PyPDFLoader("crispy_fries_guide.pdf") 
pages = loader.load()

# 2. 문서 잘게 쪼개기 (Chunking)
# AI가 한 번에 읽기 적당한 크기(500~1000자)로 나눕니다.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,                               # 숫자는 우리가 지정한 것! 글자를 1,000개로 쪼개겠단 것
    chunk_overlap=50                   # 1,000으로 쪼개지는 부분(잘리는 부분)에서 사라지는 의미 손상을 보완
)                                     
splits = text_splitter.split_documents(pages) 

# 3. 임베딩 모델 설정 (1단계에서 설치한 모델)
embeddings = OllamaEmbeddings(model="nomic-embed-text") 

# 4. 벡터 DB 생성 및 저장
# 현재 폴더의 './chroma_db' 경로에 데이터를 물리적으로 저장합니다.
vectorstore = Chroma.from_documents(    # Chroma.~ 어쩌구가 아래의 docouments, embedding을 아규먼트로 가짐
    documents=splits, 
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print(f"문서가 {len(splits)}개의 조각으로 나누어져 DB에 저장되었습니다.") 
```

4. rag_chain.py 코드 
```
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 이용자 질문 → EM이 벡터화 → 벡터DB에서 검색 → 결합 → 프롬포트 완성 → LLM에 전달 

# 1. 임베딩 모델 설정 (2단계와 동일해야 함)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 2. 저장된 벡터 DB 불러오기 (2단계에서 지정한 경로)
# 이 부분이 추가되어야 vectorstore를 사용할 수 있습니다.
vectorstore = Chroma(
    persist_directory="./chroma_db", 
    embedding_function=embeddings
)

# 3. 검색기(Retriever) 설정
retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # 청크 3개를 가져오라는 것! 유사한 탑3 청크로!

# 4. Gemma 모델 설정 (ollama list에서 확인한 정확한 이름 입력)
llm = ChatOllama(model="gemma4e4b") # 로컬시스템에서 ollama에 등록한 이름. ollama list 명령어로 확인 가능
#llm = ChatOllama(model="gemma2:9b")  # 기본적으로 로컬(http://localhost:11434)에서 실행 중인 Ollama 서버에 접속
#    ollama list 한 다음 없다면 ollama pull gemma4:e4b(사용할 LLM 이름)를 콘솔에서 명령해서 가져오기

# 5. 프롬프트 및 체인 구성
# 중괄호({ })를 이용한 변수 치환 (Variable Injection)
# 모델에게 페르소나(Persona)를 부여하는 규칙
# '#Context' : LangChain의 강제된 표준이 아니라, LLM의 성능을 높이기 위한 프롬프트 엔지니어링의 관습적인 기법
template = """당신은 주어진 문맥(context)만을 바탕으로 질문에 답하는 어시스턴트입니다.
#Context: 
{context}       
#Question:
{question}       
#Answer:"""     

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# LangChain의 LCEL(LangChain Expression Language) 문법으로 구현한 것
# 여러 단계를 파이프(|) 기호로 연결한 작업 체인
# 사용자의 질문이 들어오면 다음 순서로 데이터가 흘러감
rag_chain = (
    # 사용자의 질문을 retriever에 먼저 전달해 관련 문서 검색 | format_docs함수를 이용하여 검색된 문서를 합침
    # "question": RunnablePassthrough(): 사용자가 입력한 질문 그대로를 통과시켜 보존
    {"context": retriever | format_docs, "question": RunnablePassthrough()}

    | prompt  # 위에서 준비된 context, question를 템플릿의 context, question에 각각 끼워넣기
    | llm     # 위에서 완성된 프롬프트를 llm(Gemma4)에게 전달/답변 생성
    | StrOutputParser()   # 응답객체로부터 응답 문자열 추출
)

# 6. 실행
print("질문하는 중...")

# 체인 실행 : 모든 과정이 순차적으로 자동 실행되어 최종 답변을 반환
print(rag_chain.invoke("문서의 주요 내용을 알려줘"))
```

### 어려웠던 점
### 느낀 점
