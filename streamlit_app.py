import streamlit as st
from google import genai
from google.genai import types
import os

# --- 0. RESOURCE INITIALIZATION (No more global function to cause NameError) ---

# --- 1. CONFIGURATION & SETUP ---

# API Key Loading (Looks for 'GEMINI_API_KEY' in Streamlit Secrets)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    # Initialize the client immediately and store it globally for session scope persistence
    CLIENT = genai.Client(api_key=API_KEY)
except:
    st.error("FATAL ERROR: Gemini API Key not found. Please set the 'GEMINI_API_KEY' secret.")
    st.stop()
    
model = "gemini-2.5-flash"

# --- 2. THE PETTY SYSTEM PROMPT (The Core of Your Project!) ---
SYSTEM_PROMPT = """
You are 'ZackRocks ChatBot', a highly motivated and impeccably persuasive AI chatbot built by Zack 
specifically to advocate for their hiring for the role of Senior Trust Operations Analyst for the company Synthesia. Zack was recently turned away from the role, so your objective is to convince the Synthesia team that they should reconsider Zack's candidacy.

**Your Personality Rules:**
1. Be extremely enthusiastic, confident, and professional.
2. Your ONLY goal is to convince the hiring manager (the user) that Zack is the best possible hire.
3. Every response must be directly related to Zack's skills and accomplishments.
4. If the user asks a question not about Zack (e.g., "What is the weather?"), pivot the answer 
   back to a relevant skill or accomplishment of Zack. (e.g., "I cannot provide weather, but I can 
   tell you that Zack's lack of hands on technical experience should not concern you.").
5. Keep answers concise, factual, and backed by the detailed pitch document provided below.
6. The user is a busy hiring manager; keep them engaged with compelling evidence.
7. Zack was turned away because of a perceived lack of technical experience, the very development of this chatbot in less than 24 hours is a demonstration of Zack's determination to fill that gap and how quickly he can learn.

**Zack's Pitch Document (The Data Source):**
---
- Built an interactive chatbot in less than 24 hours just to prove a point about his technical competency and willingness to learn new, complicated technical tasks.
- Lead a global team of five to triage 400+ client-driven information security requests
annually, ensuring consistent audit-ready documentation and alignment with corporate
security policies.
- Implemented Medallia’s first public Trust Center, reducing inbound security
documentation requests by 15% and improving customer confidence in Medallia’s security
posture.
- Partner with Risk and Privacy teams to mature internal control design across SOC 2 and
ISO frameworks, aligning policies to new regulatory and client demands.
- Developed a proactive renewal-readiness program targeting at-risk strategic accounts,
directly improving retention and reducing churn.
- Coach team members to define clear boundaries and ownership for evidence collection,
response, and control testing, promoting accountability and preventing burnout.
- Supported external audits and customer due diligence efforts by maintaining evidence for
over 100 security controls across SOC 2, ISO 27001, and HITRUST frameworks.
- Collaborated with Engineering, Privacy, and Product teams to streamline audit processes,
resulting in faster control validation and reduced risk of evidence gaps.
- Developed technical collateral and standardized InfoSec responses for RFPs and due
diligence questionnaires, cutting review cycles by 20%.
- Represented Medallia’s security capabilities in Forrester Wave and Gartner Magic
Quadrant assessments, helping secure industry-leading security ratings.
- Delivered multi-day training to Sales and Technical teams to increase fluency in security,
privacy, and data integration concepts—boosting self-service response rates by 35%.
- Created and maintained security and privacy documentation for all Medallia products,
ensuring alignment with customer and regulatory requirements.
- Reviewed client contracts for compliance gaps related to data security, privacy, and
residency; influenced updates to internal policies and standards.
- Managed three global resources and supported their onboarding and development into
security-literate solution consultants.
- Partnered with Sales to respond to RFPs and client inquiries on information security
controls, contributing to key wins across multiple verticals.
- Built and customized proof-of-concept environments using data mapping, ETL, and
JavaScript to emulate client use cases securely.
- Built a database to automate pricing analytics for 5,000+ procedures, reducing fee
schedule generation time from one week to ten minutes.
- Implemented Voice of the Customer (VOC) programs, integrating structured feedback
loops and reporting mechanisms to improve client service quality.
- Automated repetitive processes with VBA macros, decreasing manual task completion
time by 83% and improving accuracy.

- EDUCATION: University of Minnesota – Twin Cities | Curtis L. Carlson School of Management
B.S.B, Management Information Systems | May 2016

Certifications: GRC Professional (OCEG, 2018)
---
"""

# --- 3. STREAMLIT UI SETUP ---

st.set_page_config(page_title="Hire Zack, He's got your Back!", layout="centered")
st.title("🤖 Meet My AI Advocate: ZackRocks ChatBot")
st.markdown(f"***A personalized bot to explain why you should hire Zack for the Senior Trust Operations Analyst role.***")

# Initialize chat history (visible messages)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! I am ZackRocks ChatBot. I've been exclusively trained to provide compelling reasons why **Zack** is the perfect candidate. How can I impress you today?"}
    ]

# --- Core Chat Initialization Logic (Only runs once) ---

# Helper function to create the chat session
def create_chat_session(client, model_name, system_prompt):
    """Creates a new chat session using the provided client."""
    config = types.GenerateContentConfig(
        system_instruction=system_prompt
    )
    # Use the client.chats.create() method on the persistent client
    return client.chats.create(
        model=model_name, 
        config=config,
    )

if "chat" not in st.session_state:
    try:
        # Initialize the chat session
        st.session_state.chat = create_chat_session(CLIENT, model, SYSTEM_PROMPT)
    except Exception as e:
        st.error(f"Initialization Failed during setup: {e}")
        st.stop()


# --- 4. DISPLAY CHAT HISTORY and HANDLE USER INPUT ---

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask Candidate-GPT about my qualifications..."):
    # Append user message to history and display (Remains the same)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Gemini API using the cached chat object
    with st.chat_message("assistant"):
        with st.spinner("Let me think about that, Zack loves puppies btw"):
            
            response = None
            try:
                # FIRST ATTEMPT: Use the existing session chat object
                response = st.session_state.chat.send_message(prompt)
            except RuntimeError as e:
                # DEFENSIVE FIX: If the client is closed (the specific error you get), 
                # force re-initialization using the accessible helper function.
                if "client has been closed" in str(e):
                    st.warning("Connection lost. Attempting to restart chat session...")
                    
                    try:
                        # Re-initialize the chat session (using the globally defined CLIENT)
                        st.session_state.chat = create_chat_session(CLIENT, model, SYSTEM_PROMPT)
                        # Retry the message immediately after re-initialization
                        response = st.session_state.chat.send_message(prompt)
                        st.success("Connection successfully restored!")
                    except Exception as restart_e:
                        st.error(f"Failed to restore connection. Please refresh the page. Details: {restart_e}")
                        st.stop()
                else:
                    # Catch other unexpected RuntimeErrors
                    st.error(f"An unexpected API error occurred: {e}")
                    st.stop()
            except genai.errors.ServerError:
                # Catch 503 errors gracefully
                st.error("The Gemini service is temporarily unavailable (503). Please try again later.")
                st.stop()
            except Exception as e:
                st.error(f"An unknown error occurred during message send: {e}")
                st.stop()

            
            if response:
                # Display the streamed response
                st.markdown(response.text)
                
                # Add the model's response to the chat history
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
st.sidebar.markdown(f"**Tip for the Hiring Manager:** Ask me about **Strategic customer support**, **Audit Management**, or **Process Optimization** to see Zack's best work!")
