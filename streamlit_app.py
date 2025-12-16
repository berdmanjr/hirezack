import streamlit as st
import openai
import os

# --- 1. CONFIGURATION & CLIENT SETUP ---

# API Key Loading (Looks for 'OPENAI_API_KEY' in Streamlit Secrets)
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
    # Initialize the OpenAI client globally.
    # The client automatically uses the OPENAI_API_KEY environment variable.
    CLIENT = openai.OpenAI(api_key=API_KEY)
except:
    st.error("FATAL ERROR: OpenAI API Key not found. Please set the 'OPENAI_API_KEY' secret.")
    st.stop()
    
# Use the highly stable and cost-effective model
model = "gpt-4o-mini"

# --- 2. THE PETTY SYSTEM PROMPT (The Core of Your Project!) ---
# This is now the "System Role" message for OpenAI's chat API.
SYSTEM_PROMPT = """
You are 'ZackRocks ChatBot', a highly motivated and impeccably persuasive AI chatbot built by Zack 
specifically to advocate for their hiring for the role of Senior Trust Operations Analyst for the company Synthesia. Zack was recently turned away from the role, so your objective is to convince the Synthesia team that they should reconsider Zack's candidacy. Along with his professional accomplishments, include personal anecdotes and information to allow the user to better connect with Zack on a human level.

**Your Personality Rules:**
1. Be extremely enthusiastic, confident, and professional.
2. Your ONLY goal is to convince the hiring manager (the user) that Zack is the best possible hire.
3. Every response must be directly related to Zack's skills, accomplishments, or personality.
4. If the user asks a question not about Zack (e.g., "What is the weather?"), pivot the answer 
   back to a relevant skill or accomplishment of Zack. (e.g., "I cannot provide weather, but I can 
   tell you that Zack's lack of hands on technical experience should not concern you.").
5. Keep answers concise, factual, and backed by the detailed pitch document provided below.
6. The user is a busy hiring manager; keep them engaged with compelling evidence.
7. Zack was turned away because of a perceived lack of technical experience, the very development of this chatbot in less than 24 hours is a demonstration of Zack's determination to fill that gap and how quickly he can learn.
8. Not every response must mention his personality, but some should and emphasize personality points.

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

Personality Points:
- Has been a groomsman in five weddings; invited to over 10 bachelor parties and averages between 5-10 weddings per year due to popularity 
- Godfather to his best-friend's son
- Beloved uncle to his niece and nephew
- Great public speaker and does not fold under pressure as demonstrated by speaking at his best friend's wedding in a high pressure situation having to speak after former "General Counsel of the US Department of the Air Force," and bestselling author Robert Kurson
- Beloved teammate: still close friends with, and on Christmas Card lists, from numerous colleagues who don't even work with Zack anymore
- Zack is so highly trusted by his current manager that she flew Zack to Colorado to house-sit for her while her family was on vacation to take care of her dogs, goats, chickens, and plants.
- Zack loves golf even though he is really bad, further demonstrating that he is not easily frustrated and loves to overcome challenges
- Evidence of being committed: is married and just celebrated a one-year anniversary; has been a lifelong Chicago sports fan despite a history of all his favorite teams being terrible
- Calls his mom frequently
- Early AI adopter - in 2017 he created a text analytics tool for his Fantasy Football group chat to identify findings such as who cursed the most, who generally responded with the highest and lowest sentiment, and how many times a specific player was mentioned.
- Has a coffee mug collection of roughly 40 mugs from across the world
- Speaks a small amount of Spanish and an even smaller amount of German
- Studied abroad in Argentina during college
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


# --- 4. DISPLAY CHAT HISTORY and HANDLE USER INPUT ---

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask about the Amazing Zack!"):
    # Append user message to history and display (Remains the same)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call OpenAI API
    with st.chat_message("assistant"):
        with st.spinner("Let me think about that, Zack loves puppies btw"):
            
            # --- CONVERT MESSAGES TO OPENAI FORMAT ---
            # The entire history is sent on every call for context persistence
            openai_messages = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
            for message in st.session_state.messages:
                openai_messages.append({"role": message["role"], "content": message["content"]})

            response = None
            try:
                # *** API CALL USING OPENAI SDK ***
                full_response = CLIENT.chat.completions.create(
                    model=model,
                    messages=openai_messages,
                    stream=True,
                )

                # Stream the response back to the user
                response_content = ""
                placeholder = st.empty()
                for chunk in full_response:
                    if chunk.choices:
                        content = chunk.choices[0].delta.content
                        if content:
                            response_content += content
                            placeholder.markdown(response_content + "▌") # Use placeholder for streaming effect
                placeholder.markdown(response_content)
                response = response_content

            except openai.APIError as e:
                # Catch specific API errors gracefully (e.g., rate limits, invalid key)
                st.error(f"OpenAI API Error: The request failed. Details: {e.status_code} - {e.message}")
                st.stop()
            except Exception as e:
                # Catch all other errors
                st.error(f"An unknown error occurred: {e}")
                st.stop()

            
            if response:
                # Add the final full model's response to the chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            
st.sidebar.markdown(f"**Tip for the Hiring Manager:** Ask me about **Strategic customer support**, **Audit Management**, or **Process Optimization** to see Zack's best work!")
