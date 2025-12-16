import streamlit as st
from google import genai
from google.genai import types
import os

# --- 0. CLIENT INITIALIZATION ---
# NOTE: The client is initialized outside the main execution flow to persist the API Key, 
# but we will RECREATE the chat session inside the prompt loop on every turn.
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    CLIENT = genai.Client(api_key=API_KEY) # The persistent client (for API Key use)
except:
    st.error("FATAL ERROR: Gemini API Key not found. Please set the 'GEMINI_API_KEY' secret.")
    st.stop()
    
model = "gemini-2.5-flash"

# --- 1. CORE LOGIC FUNCTION ---
# We make a single function to get a response for one turn only
def get_single_response(client, model_name, system_prompt, user_prompt):
    """Creates a new chat session, sends ONE message, and returns the response."""
    
    # 1. Create CONFIGURATION for the chat session
    config = types.GenerateContentConfig(
        system_instruction=system_prompt
    )
    
    # 2. Re-create the entire chat object (new connection guaranteed)
    chat_session = client.chats.create(
        model=model_name, 
        config=config,
    )
    
    # 3. Send the message and return the response
    return chat_session.send_message(user_prompt)

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

# --- 3. STREAMLIT UI SETUP (Remains the same) ---

st.set_page_config(page_title="Hire Zack, He's got your Back!", layout="centered")
st.title("🤖 Meet My AI Advocate: ZackRocks ChatBot")
st.markdown(f"***A personalized bot to explain why you should hire Zack for the Senior Trust Operations Analyst role.***")

# Initialize chat history (visible messages)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! I am ZackRocks ChatBot. I've been exclusively trained to provide compelling reasons why **Zack** is the perfect candidate. How can I impress you today?"}
    ]

# --- 4. DISPLAY CHAT HISTORY and HANDLE USER INPUT ---

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask me why I love Zack so much!"):
    # Append user message to history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Gemini API using the new, single-turn client approach
    with st.chat_message("assistant"):
        with st.spinner("Let me think about that, Zack loves puppies btw"):
            
            response = None
            try:
                # *** CRITICAL FIX: The entire chat session is rebuilt here ***
                response = get_single_response(CLIENT, model, SYSTEM_PROMPT, prompt)
                
            except Exception as e:
                # Catch all remaining errors, including the File Descriptor issue
                st.error(f"FATAL ERROR: The connection failed. Please try again. Details: {e}")
                st.stop()
            
            if response:
                # Display the streamed response
                st.markdown(response.text)
                
                # Add the model's response to the chat history
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
st.sidebar.markdown(f"**Tip for the Hiring Manager:** Ask me about **Strategic customer support**, **Audit Management**, or **Process Optimization** to see Zack's best work!")
