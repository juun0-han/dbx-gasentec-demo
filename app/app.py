import os

import streamlit as st
from databricks.sdk import WorkspaceClient
from databricks_openai import DatabricksOpenAI


st.set_page_config(
    page_title="GasEnTec LNG Supervisor Demo",
    page_icon="⛽",
    layout="wide",
)

SUPERVISOR_ENDPOINT = os.getenv("SUPERVISOR_AGENT_ENDPOINT", "").strip()
GENIE_SPACE_NAME = os.getenv("GENIE_SPACE_NAME", "GasEnTec LNG Operations Genie")
AI_SEARCH_INDEX = os.getenv(
    "AI_SEARCH_INDEX",
    "issu_dip_wksp.gasentec_hands_on.gasentec_lng_glossary_index",
)

st.title("GasEnTec LNG Supervisor Demo")
st.caption("Genie Agent · Knowledge Assistant · AI Search를 연결한 합성 LNG 데모")

with st.sidebar:
    st.subheader("연결 정보")
    st.write(f"**Genie Agent:** {GENIE_SPACE_NAME}")
    st.write(f"**AI Search:** {AI_SEARCH_INDEX}")
    st.write(f"**Supervisor endpoint:** {SUPERVISOR_ENDPOINT or '미설정'}")
    st.divider()
    st.markdown(
        "질문 예시:\n"
        "- 가스 내보낸 양이 많은 터미널은 어디야?\n"
        "- BOG가 뭐야?\n"
        "- BOG rate가 올라가면 무엇을 확인해야 해?"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if not SUPERVISOR_ENDPOINT:
    st.warning(
        "SUPERVISOR_AGENT_ENDPOINT 환경변수가 설정되지 않았습니다. "
        "App 설정에서 Supervisor endpoint 이름을 입력하세요."
    )

question = st.chat_input("LNG 운영에 대해 질문하세요.")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if not SUPERVISOR_ENDPOINT:
            answer = "Supervisor endpoint가 설정되지 않았습니다."
            st.error(answer)
        else:
            try:
                with st.spinner("Supervisor가 적절한 Agent를 선택하고 있습니다..."):
                    workspace_client = WorkspaceClient()
                    client = DatabricksOpenAI(workspace_client=workspace_client)
                    response = client.responses.create(
                        model=SUPERVISOR_ENDPOINT,
                        input=[{"role": "user", "content": question}],
                    )
                    answer = response.output_text or "응답 내용이 없습니다."
                st.markdown(answer)
            except Exception as exc:
                answer = f"Supervisor 호출 중 오류가 발생했습니다.\n\n{exc}"
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

