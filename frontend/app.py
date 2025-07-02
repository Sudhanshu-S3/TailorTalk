import streamlit as st
import requests
import os
from datetime import date, timedelta

BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")

FRONTEND_FACING_BACKEND_URL = os.environ.get("FRONTEND_FACING_BACKEND_URL", BACKEND_URL)
CHAT_URL = f"{BACKEND_URL}/chat"
SLOTS_URL = f"{BACKEND_URL}/slots"

st.set_page_config(page_title="Calendo")

with st.sidebar:
    st.title("Calendo")
    st.caption("Your friendly appointment booking assistant.")
    st.markdown("---")

    st.subheader("Available Slots")
    try:
        response = requests.get(SLOTS_URL)
        response.raise_for_status()
        slots = response.json()

        today_str = date.today().strftime("%B %d")
        tomorrow_str = (date.today() + timedelta(days=1)).strftime("%B %d")

        st.write(f"**Today ({today_str})**")
        if slots.get("today"):
            for slot in slots["today"]:
                st.write(f"- {slot}")
        else:
            st.write("No slots available.")

        st.write(f"**Tomorrow ({tomorrow_str})**")
        if slots.get("tomorrow"):
            for slot in slots["tomorrow"]:
                st.write(f"- {slot}")
        else:
            st.write("No slots available.")

    except requests.exceptions.RequestException:
        st.warning("Could not fetch available slots. The backend might be offline.")
    except Exception:
        st.warning("Could not display available slots.")


    st.markdown("---")
    if st.button("Clear Chat History"):
        st.session_state.messages = [{"role": "assistant", "content": "How can I help you today?"}]
        st.rerun()
    st.markdown("---")
    st.markdown("This chatbot helps you book appointments with a tailor. You can ask about available slots, book a new appointment, or check your existing appointments.")
    st.markdown("Powered by Streamlit and FastAPI.")

st.title(" Calendo Appointment Bot ")
st.caption("I can help you book an appointment. Try asking 'Are there any slots available tomorrow?'")


st.markdown("### Example Prompts")
st.info("""
- "Are there any 1-hour slots available tomorrow?"
- "Book me an appointment for tomorrow or 2025-07-06 at 3pm for a suit fitting."
- "What appointments do I have?"
""")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # Send request to the backend
        response = requests.post(CHAT_URL, json={"message": prompt})
        response.raise_for_status() 
        
        reply = response.json()["reply"]
        
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
