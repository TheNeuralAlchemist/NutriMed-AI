"""One chat box used by both MediLens and NutriLens (Phases 4 and 7)."""
import streamlit as st
import ai


def chat_ui(name, context, topic):
    key = f"chat_{name}"
    history = st.session_state.setdefault(key, [])

    for m in history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    question = st.chat_input(f"Ask about your {topic}...", key=f"input_{name}")
    if question:
        with st.chat_message("user"):
            st.markdown(question)
        previous = "\n".join(
            f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}"
            for m in history[-8:]
        )
        prompt = (
            ai.SAFETY
            + f"The user is asking about their {topic}. Answer ONLY using the "
              "information below plus general knowledge. If the answer is not "
              "there, say so.\n\n--- INFORMATION ---\n"
            + context[:12000]
            + "\n--- CHAT SO FAR ---\n" + previous
            + f"\n--- NEW QUESTION ---\n{question}\n\nKeep the answer short and simple."
        )
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, err = ai.ask(prompt)
            if err:
                st.error(err)
            else:
                st.markdown(answer)
                history.append({"role": "user", "content": question})
                history.append({"role": "assistant", "content": answer})

    if history and st.button("Clear chat", key=f"clear_{name}"):
        st.session_state[key] = []
        st.rerun()
