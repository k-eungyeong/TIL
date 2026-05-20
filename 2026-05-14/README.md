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

### 어려웠던 점
### 느낀 점
