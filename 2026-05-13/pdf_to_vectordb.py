from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# 1. 문서 불러오기 (PDF 예시)
loader = PyPDFLoader("도메인문서_파일.pdf") 
pages = loader.load()

# 2. 문서 잘게 쪼개기 (Chunking)
# AI가 한 번에 읽기 적당한 크기(500~1000자)로 나눕니다.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, 
    chunk_overlap=50
)
splits = text_splitter.split_documents(pages)

# 3. 임베딩 모델 설정 (1단계에서 설치한 모델)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 4. 벡터 DB 생성 및 저장
# 현재 폴더의 './chroma_db' 경로에 데이터를 물리적으로 저장합니다.
vectorstore = Chroma.from_documents(
    documents=splits, 
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print(f"문서가 {len(splits)}개의 조각으로 나누어져 DB에 저장되었습니다.")
