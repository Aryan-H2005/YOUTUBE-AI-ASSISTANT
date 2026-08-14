import os
import streamlit as st

from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import FAISS

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from langchain_core.prompts import PromptTemplate


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="YouTube AI Assistant",
    page_icon="🎥",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🎥 YouTube AI Assistant")
st.write(
    "Ask questions about a YouTube video using its transcript."
)


# =========================================================
# API KEY
# =========================================================




# =========================================================
# FUNCTIONS
# =========================================================

def extract_video_id(url):

    parsed_url = urlparse(url)

    # youtube.com/watch?v=...
    if parsed_url.hostname in [
        "www.youtube.com",
        "youtube.com"
    ]:

        return parse_qs(
            parsed_url.query
        ).get("v", [None])[0]

    # youtu.be/...
    if parsed_url.hostname == "youtu.be":

        return parsed_url.path.lstrip("/")

    return None


def get_transcript(video_id):

    try:

        api = YouTubeTranscriptApi()

        transcript_data = api.fetch(
            video_id,
            languages=["en"]
        )

        transcript_list = (
            transcript_data.to_raw_data()
        )

        transcript = " ".join(
            chunk["text"]
            for chunk in transcript_list
        )

        return transcript

    except TranscriptsDisabled:

        return None

    except Exception as e:

        st.error(f"Transcript error: {e}")

        return None


def create_vectorstore(transcript):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.create_documents(
        [transcript]
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectorstore


def ask_question(question, vectorstore):

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = PromptTemplate(
        template="""
You are an intelligent YouTube video assistant.

Answer the user's question using ONLY
the information provided in the transcript context.

Rules:

1. Do not invent information.
2. Do not use outside knowledge.
3. If the answer is not available in the
   transcript, say:

"I couldn't find the answer in the video."

4. Give a clear and concise answer.

Transcript Context:
{context}

User Question:
{question}

Answer:
""",

        input_variables=[
            "context",
            "question"
        ]
    )

    final_prompt = prompt.format(
        context=context,
        question=question
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    response = llm.invoke(
        final_prompt
    )

    return response.content


# =========================================================
# SESSION STATE
# =========================================================

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "video_id" not in st.session_state:
    st.session_state.video_id = None


# =========================================================
# YOUTUBE URL
# =========================================================

st.subheader("1️⃣ Enter YouTube Video")

youtube_url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)


# =========================================================
# PROCESS VIDEO
# =========================================================

if st.button("🚀 Process Video"):


    if not youtube_url:

        st.warning(
            "Please enter a YouTube URL."
        )

    else:

        video_id = extract_video_id(
            youtube_url
        )

        if not video_id:

            st.error(
                "Invalid YouTube URL."
            )

        else:

            with st.spinner(
                "Fetching video transcript..."
            ):

                transcript = get_transcript(
                    video_id
                )

            if transcript is None:

                st.error(
                    "Could not retrieve the transcript."
                )

            else:

                with st.spinner(
                    "Creating vector database..."
                ):

                    vectorstore = create_vectorstore(
                        transcript
                    )

                st.session_state.vectorstore = (
                    vectorstore
                )

                st.session_state.video_id = (
                    video_id
                )

                st.success(
                    "Video processed successfully! 🎉"
                )

                st.video(
                    f"https://www.youtube.com/watch?v={video_id}"
                )


# =========================================================
# QUESTION ANSWERING
# =========================================================

if st.session_state.vectorstore:

    st.divider()

    st.subheader("2️⃣ Ask Questions")

    question = st.text_input(
        "Ask something about the video",
        placeholder="What is the main topic of the video?"
    )

    if st.button("💬 Ask"):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Thinking..."
            ):

                answer = ask_question(
                    question,
                    st.session_state.vectorstore
                )

            st.subheader("🤖 Answer")

            st.write(answer)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "YouTube AI Assistant • RAG + FAISS + Gemini"
)
