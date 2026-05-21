# 2026-05-13
## 목표 : Ollama를 사용해 Local System에서 LLM(Gemma4) 사용해보기
### 배운 내용
1. LM Studio : GUI(Graphic User Interpace)를 사용해 Local System에서 LLM을
   다운로드 및 시작, 사용, 종료 등 관리
    - 개인이 LLM을 다운하여 Local System에서 사용할 때 권장
    - 여기서 Studio란? 눈에 보이는 화면(GUI)을 갖춘 작업공간 = 시각적인 작업장
    - 메모리 차지 ↑
2. Ollama : Local System에서 LLM을 다운로드하고 시작, 사용, 종료 등 관리
    - Python 프로젝트에서 Ollama에 접속하여 LLM을 사용할 수 있으므로 기업용 Chatbot을 구축할 때 권장
    - 내부에서 http 서버를 내장
    - CMD/Python에서도 사용 가능
    - 서버처럼 작동하여 프로그램 코드에서 접근하기 최적화
    - 커맨드 라인에서 돌아가는 툴
  
[ Ollama에 Gemma4 등록하기 ]
 → Ollama가 Gemma4를 실행해 프롬포트를 나르고 보여주는 중간 역할 수행
 1. Gemma4를 저장해둔 공간(ex. LM Studio에서 사용했다면, 파일 경로 복사)
 2. 경로 중 마지막 모델 명을 Ollama Settings에서 설정한 루트 안으로 넣어줘야 함!
 3. Ollama\models 안에 Modelfile 파일 생성(텍스트 파일이 아닌 시스템 설정하는 설계도이기 때문에 확장자X)
 4. Modelfile의 내용 넣기 : FROM "./(모델명)"        *이때 파일명은 모두 소문자여야 함
 5. CMD) ollama 내 models 파일 폴더로 경로 이동
 6. "ollama create (모델명)" 명령어 실행 → 최초 1회만
 7. 콘솔에 gathering model components ..., writing manifest, success가 뜨면 등록 성공한 것
 8. CMD) "ollama run (모델명)" 명령 → 사용자 질문 요청 → 알맞은 답변 뜨면 성공 → 종료시 "/bye"



### 어려웠던 것
### 느낀 점
