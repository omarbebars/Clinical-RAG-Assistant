import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq  # <-- 1. Import Groq
import os
from dotenv import load_dotenv
load_dotenv()




# Configuration
COLLECTION_NAME = "medical_cases"
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
# 3. Use a Groq model name
LLM_MODEL = 'llama-3.1-8b-instant'
DB_PATH = "./cases_db"


@st.cache_resource
def load_components():
    """
    Load all the heavy components ONCE and cache them.
    """
    print("Loading models and DB (this runs once)...")
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)

    # Embedding model (still local)
    model = SentenceTransformer(EMBEDDING_MODEL)

    # 4. Initialize the Groq LLM client
    try:
        llm = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        # Test the connection
        llm.chat.completions.create(model=LLM_MODEL, messages=[{"role": "user", "content": "test"}], max_tokens=10)
    except Exception as e:
        st.error(f"Error connecting to Groq: {e}")
        st.error("Please make sure your API key is correct and pasted in line 11.")
        return None, None, None

    print("Components loaded successfully.")
    return collection, model, llm


collection, model, llm = load_components()

# --- Streamlit Interface (Mostly the same) ---
st.set_page_config(layout="wide")
st.title("🩺 Medical RAG Assistant (w/ Groq)")
st.write(f"Running on Groq with: **{LLM_MODEL}**")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about the case studies..."):
    if not all([collection, model, llm]):
        st.error("Components are not loaded. Cannot process request. Check API key and refresh.")
    else:
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # --- RAG Logic ---
        with st.spinner("Finding relevant cases..."):
            query_embedding = model.encode(prompt).tolist()
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=5
            )
            retrieved_context = "\n\n---\n\n".join(results['documents'][0])

        prompt_template = f"""
        You are a medical case study assistant.
        Answer the user's question based *only* on the following context.
        If the answer is not found, say "I do not have that information in the provided case studies."
        --- CONTEXT ---
        {retrieved_context}
        --- END OF CONTEXT ---
        USER'S QUESTION: {prompt}
        """

        # 5. Generate and Stream Response (NOW USING GROQ)
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            try:
                # 6. This is the new Groq API call
                response_stream = llm.chat.completions.create(
                    model=LLM_MODEL,
                    messages=[{'role': 'user', 'content': prompt_template}],
                    stream=True
                )

                for chunk in response_stream:
                    token = chunk.choices[0].delta.content
                    if token:
                        full_response += token
                        response_placeholder.markdown(full_response + "▌")
                response_placeholder.markdown(full_response)

            except Exception as e:
                st.error(f"An error occurred: {e}")

        st.session_state.messages.append({"role": "assistant", "content": full_response})

