# 2026-05-13
## 목표 : RAG 챗봇을 만들기 위한 핵심 3요소(시스템)
### 배운 내용
1. RAG 시스템 구성 순서 
  - Domain Documents : PDF 파일 준비
  - Embedding Model : 한글/영문이 가능한 Pre-Trained 임베딩 모델 ex. nomic-embed-text
  - Vector DB : Chroma DB
  - LangChain 모듈을 이용하여 위 항목들 실행 및 DB 구축
  - LLM(Gemma4)
    * 여기서 LangChain은 전체 흐름을 관리하는 관리자 st! Vector DB에서 실행되는 것이 아님
  [ Vector DB 하는 일 ]
   - 벡터 저장, 의미 검색(벡터 공간에서 크기/방향으로 식별 = 유사한 벡터를 N개 찾아서 리턴)
    * 사용자가 질문했을 때 RAG 검색이 수행되는 흐름 : 사용자 질문 입력 → 질문을 임베딩 벡터로 변환 → Vector DB에서 유사벡터 검색 → 관련 원문 텍스트 가져오기 → LLM 전달 → 답변 생성

2. 문맥유지(Context Retention)
  - 현재 대화 그 전의 대화를 기억하고 응답에 활용하기 위해 필요
  - 최근 대화만 기억하기 + 기존 대화 요약하기 = 결합 혼용
  - 상용화하기 위해서는 앞선 대화를 DB에 저장

3. 웹사이트에서 RAG 시스템 연동
  - FastAPI는 Session을 지원하지 않는 무상태(Stateless) 방식
  - Session 사용을 위해 외부 모듈 사용 → 사용하면 이용자의 상태를 서버 측에서 유지 가능, 이용자별 대화를 별도로 메모리에 저장하고 문맥 유지시 활용가능

4. LangChain 모듈을 사용해 PDF 문서를 Vector DB에 저장(실습)
  - 도메인 문서 PDF 파일 준비
  - Embedding 모델을 사용하여 벡터화하는 내용 포함되어 있음
  - Anaconda Prompt 실행 → "conda env list" → torch_env 유무 확인 → "conda activate torch_env" 
    → "pip install langchain langchain-community langchain-ollama langchain-chroma pypdf" → "cd (저장공간)" → 바뀌면 "code." 해서 VS code 실행
  - VS code 열리면 pdf_to_vectordb.py 저장     * 저장된 곳에 사용할 PDF도 저장


[ 언어 ]  
Session  사용자별 임시 기억공간 (문맥 유지방식)  
Redis    초고속 메모리 저장소

### 어려웠던 것
### 느낀 점
