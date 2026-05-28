import smtplib
import imaplib
import email
from email.header import decode_header
from email.mime.text import MIMEText
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent

# ══════════════════════════════════════════════
#  공통 설정 데이터
# ══════════════════════════════════════════════
GMAIL_ADDRESS = "kimeungyeong33@gmail.com"
GMAIL_APP_PW  = "dqzljtrhfjnaeqvu"

# ══════════════════════════════════════════════
#  유틸리티 함수
# ══════════════════════════════════════════════
def decode_str(value):
    if not value:
        return ""
    decoded_parts = decode_header(value)
    result = ""
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            result += part.decode(charset or "utf-8", errors="ignore")
        else:
            result += part
    return result

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition  = str(part.get("Content-Disposition", ""))
            if content_type == "text/plain" and "attachment" not in disposition:
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                body = payload.decode(charset, errors="ignore")
                break
    else:
        payload = msg.get_payload(decode=True)
        charset = msg.get_content_charset() or "utf-8"
        body = payload.decode(charset, errors="ignore")
    return body.strip()

# ══════════════════════════════════════════════
#  1. 에이전트용 메일 수신 툴 정의
# ══════════════════════════════════════════════
@tool
def fetch_latest_emails_tool(limit: int = 5) -> str:
    """Gmail 수신함(INBOX)에서 최근 이메일을 가져옵니다. 
    가져올 메일 개수(limit)를 지정할 수 있으며, 기본값은 5개입니다."""
    try:
        # IMAP 서버 연결 및 로그인
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_ADDRESS, GMAIL_APP_PW)
        mail.select("inbox")

        # 모든 메일 ID 검색
        status, data = mail.search(None, "ALL")
        if status != "OK":
            return "❌ 메일 목록을 가져오는 데 실패했습니다."

        mail_ids = data[0].split()
        if not mail_ids:
            return "📥 수신함이 비어 있습니다."

        # 최근 메일 ID부터 역순 정렬 후 지정한 개수만큼 슬라이싱
        latest_ids = mail_ids[::-1][:limit]
        
        result_summary = []
        
        for index, m_id in enumerate(latest_ids, start=1):
            status, msg_data = mail.fetch(m_id, "(RFC822)")
            if status != "OK":
                continue
                
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # 발신자, 제목, 본문 추출
            sender = decode_str(msg.get("From"))
            subject = decode_str(msg.get("Subject"))
            body = get_email_body(msg)
            
            # 한눈에 보기 편하게 포맷팅
            email_info = (
                f"[{index}] ──────────────────────────────\n"
                f"📩 보낸 사람: {sender}\n"
                f"📌 제    목: {subject}\n"
                f"📝 본    문:\n{body[:300]}..."  # 긴 본문은 요약을 위해 300자까지만 전송
            )
            result_summary.append(email_info)

        mail.logout()
        return "\n\n".join(result_summary)

    except Exception as e:
        return f"❌ 메일 조회 중 오류 발생: {str(e)}"

# ══════════════════════════════════════════════
#  2. LangGraph + Ollama 에이전트 조립
# ══════════════════════════════════════════════
llm = ChatOllama(model="gemma4:e4b", temperature=0)

# 도구 리스트에 조회용 툴 장착
tools = [fetch_latest_emails_tool]

# 에이전트 빌드 (안자 경고가 발생하지 않는 표준 함수)
agent = create_agent(llm, tools)

# ══════════════════════════════════════════════
#  3. 에이전트 실행 및 테스트
# ══════════════════════════════════════════════
if __name__ == "__main__":
    # 에이전트의 정체성 (전송/조회 업무 분담 지침)
    system_instruction = (
        "당신은 유능한 이메일 관리 비서입니다. "
        "사용자가 메일을 확인해 달라고 하거나 최근 메일을 보여달라고 요청하면 "
        "반드시 'fetch_latest_emails_tool'을 호출하여 결과를 정리해 알려주세요."
    )
    
    # 💡 에이전트 호출 테스트 문구
    user_query = "최근 받은 메일 5개만 확인해서 보여줘."
    
    print(f"🤖 에이전트 요청 입력: {user_query}\n")
    print("⏳ 에이전트가 수신함을 조회하는 중...")

    # 프롬프트 결합 및 실행
    response = agent.invoke({
        "messages": [
            SystemMessage(content=system_instruction),
            HumanMessage(content=user_query)
        ]
    })

    # 최종 출력
    final_reply = response["messages"][-1].content
    print("\n══════════════════════════════════════════════")
    print("🤖 에이전트 최종 분석 답변:")
    print(final_reply)
    print("══════════════════════════════════════════════")
