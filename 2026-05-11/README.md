# 2026-05-11
## 목표 : LM Studio, Ollama 개념 이해
### 배운 내용
1. RAG
   - 검색증강시스템(Retrieval Augmented Generation)
   - 거대언어모델(LLM)이 답변을 생성하기 전, 외부 신뢰할 수 있는 DB나 문서에서 관련 정보를 검색(Retrieval)하여 그 내용을 바탕으로 답변을 보강(Augmented)하여 문장을 새로 생성(Generation)하는 기술
   - RAG를 사용하는 경로
      1) 이용자 : 언어모델을 사용하고자 함(대화신청 = 프롬포트를 사용해 데이터 전달) → 텍스트 입력(질문, 쿼리) → LLM으로 텍스트가 들어가서 응답 추출
      2) 개발자 : 이용자가 텍스트 입력 → 텍스트가 벡터 변환 거침(Embedding) → LLM → 응답
      3) 자세하게 : 이용자 입력 텍스트 → Embedding Model → 벡터 → 벡터 DB에서 의미검색 → 다수 개의 검색결과 리턴 → Embedding Model → 텍스트 → LLM(청크를 가지고 문장 완성) → 완성된 문장 → 이용자에게 출력 

   * LLM이란? Large Language Model ex. ChatGPT
   * LangChain 모듈 : 언어모델을 체인처럼 엮어서 서비스하는 것 (Python 모듈)
   * LM 테스트 : 현재 시스템 사양에 맞춰 응답 시간이나 한글 지원 여부를 확인 → 저사양 시스템에서도 실행 가능

2. Embedding(끼워넣기)
   - 텍스트를 벡터로 변환하는 작업
   - 텍스트 의미상 비슷한 문장은 벡터 중간에서 인접하도록 변환
   - Pre-Trained Embedding Model(이미 학습된 AI모델) ex. nomic-embed-text
  
3. LM Studio 
   - 여러가지 LM을 로컬 시스템에서 테스트하는 용도
   - 언어모델을 검색하고 다운로드 및 테스트
   - 허깅페이스에서 언어모델을 자동으로 다운로드 해줌 → 중간 SW 역할을 해주는 공간
  
4. Ollama
   - LM Studio에서 더 큰 개념, 터미널 기반 작동
   - 로컬 시스템에서 웹서버를 통해 언어모델을 실행할 수 있는 환경(기업용 유리)
  
5. Vector DB
   - Embedding을 이용해 벡터(숫자)가 생성되면 DB에 저장
   - 검색할 때 벡터의 유사도를 사용하는 시스템(텍스트 의미(벡터)가 유사한지 검색)
  
6. 문서의 벡터화
   - 전문영역에 특화된 문서
   - 텍스트 → Embedding Model → 벡터 → 벡터DB에 저장

### 어려웠던 점
### 느낀 점 
