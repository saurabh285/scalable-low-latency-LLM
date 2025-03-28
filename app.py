import streamlit as st
import requests
import time

st.set_page_config(page_title="Scalable QnA Assistant", layout="centered")

st.title("🧠 Scalable AI QnA Assistant")
st.markdown("Ask any question. The system routes it through Redis, FAISS, or Gemini.")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Your Question", placeholder="e.g. What is Python?")

if st.button("Get Answer") and query:
    with st.spinner("Thinking..."):
        try:
            response = requests.get("http://localhost:8000/ask", params={"q": query}, stream=True)

            try:
                data = response.json()
                source = data.get("source", "")
                latency = data.get("latency_ms", 0)
                answer = data["answer"]

                st.markdown("### ✅ Answer:")
                st.markdown(answer)

                st.markdown(f"**Source:** `{source}`")
                st.markdown(f"**Latency:** `{latency} ms`")

                st.markdown("**Breakdown:**")
                for key, val in data.get("breakdown", {}).items():
                    st.markdown(f"- `{key}`: {val} ms")

                st.session_state.history.append({
                    "q": query,
                    "a": answer,
                    "source": source,
                    "latency": latency
                })

            except Exception:
                # Gemini fallback – streamed response
                st.markdown("### ✅ Answer:")
                streamed_output = st.empty()
                answer = ""
                st.markdown("**Source:** `gemini (streaming)`")

                gemini_start = time.time()
                for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
                    answer += chunk
                    streamed_output.markdown(answer + "▌")
                gemini_end = time.time()

                streamed_output.markdown(answer)
                latency = round((gemini_end - gemini_start) * 1000, 2)
                st.markdown(f"**Latency:** `{latency} ms`")

                st.session_state.history.append({
                    "q": query,
                    "a": answer,
                    "source": "gemini",
                    "latency": latency
                })

        except Exception as e:
            st.error(f"Request failed: {e}")

# History
if st.session_state.history:
    st.markdown("---")
    st.markdown("### 📜 Query History")
    for item in reversed(st.session_state.history):
        st.markdown(f"**Q:** {item['q']}")
        st.markdown(f"- 🧠 *{item['source']}* | ⏱️ *{item['latency']} ms*")
        st.markdown(f"**A:** {item['a']}")
        st.markdown("---")
