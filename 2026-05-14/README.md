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
    
### 어려웠던 점
### 느낀 점
