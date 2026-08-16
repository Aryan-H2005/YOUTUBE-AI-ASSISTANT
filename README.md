# YOUTUBE-AI-ASSISTANT 🎥✨

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Jupyter Notebook](https://img.shields.io/badge/Jupyter-Notebook-orange?style=flat-square&logo=jupyter)](https://jupyter.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

The YOUTUBE-AI-ASSISTANT is an intelligent tool designed to enhance your interaction with YouTube video content. Leveraging the power of Large Language Models (LLMs) and vector databases, this project allows you to effortlessly extract, analyze, and query information from any YouTube video. Whether you're a student, researcher, or just curious, this assistant transforms passive viewing into active learning by providing immediate, context-aware answers to your questions based directly on the video's transcript.

## ✨ Features

*   **Retrieve YouTube Video ID**: Automatically extracts the video ID from a given YouTube URL.
*   **Fetch Transcript**: Downloads the full transcript of the YouTube video.
*   **Analyze Video Content**: Processes the video transcript using AI to identify key themes and information.
*   **Store Relevant Information**: Organizes and stores the extracted information in a robust vector database for efficient retrieval.
*   **Interactive Q&A**: Users can ask natural language questions related to the video content.
*   **LLM-Powered Answers**: An integrated LLM analyzes user questions and generates precise answers based on the relevant information retrieved from the vector database.

## 🚀 Tech Stack

*   **Python**: The core programming language for the entire project.
*   **Jupyter Notebook**: For an interactive and exploratory development environment.
*   **Vector Database**: For efficient storage and retrieval of embedded information (e.g., FAISS, ChromaDB, Weaviate - specific implementation may vary).
*   **Large Language Models (LLMs)**: For text analysis, question answering, and summarization (e.g., OpenAI GPT models, Hugging Face models).
*   **Libraries**:
    *   `youtube-transcript-api`: For fetching video transcripts.
    *   `langchain` / `llamaindex`: For LLM orchestration and vector database integration.
    *   `sentence-transformers`: For generating embeddings.

## ⚙️ Installation

To set up the YOUTUBE-AI-ASSISTANT locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Aryan-H2005/YOUTUBE-AI-ASSISTANT.git
    cd YOUTUBE-AI-ASSISTANT
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        venv\Scripts\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(A sample `requirements.txt` might look like this:)*
    ```
    jupyter
    youtube-transcript-api
    langchain
    openai
    tiktoken
    faiss-cpu # or chromadb, pinecone-client, etc.
    sentence-transformers
    python-dotenv
    ```

4.  **Set up API Keys (if using external LLMs):**
    If you are using LLMs like OpenAI's GPT models, you will need an API key. Create a `.env` file in the project root and add your API key:
    ```
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

## 💡 Usage

Once installed, you can start interacting with YouTube videos through the Jupyter Notebook.

1.  **Launch Jupyter Notebook:**
    ```bash
    jupyter notebook
    ```
    This will open a browser window with the Jupyter interface.

2.  **Open the main notebook:**
    Navigate to and open the primary notebook file (e.g., `youtube_assistant.ipynb`).

3.  **Run the cells:**
    Follow the step-by-step instructions within the notebook. Typically, the workflow will be:

    *   **Provide a YouTube URL:**
        ```python
        youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Replace with your desired video URL
        ```

    *   **Process the video (retrieve transcript, analyze, store):**
        Run the relevant cells that handle transcript fetching, text chunking, embedding generation, and storing into the vector database.

    *   **Ask your questions:**
        Once the video content is processed, you can query it:
        ```python
        question = "What are the key takeaways from this video?"
        answer = assistant.ask_question(question) # Assuming 'assistant' is your configured LLM chain
        print(answer)

        question_2 = "Can you summarize the introduction?"
        answer_2 = assistant.ask_question(question_2)
        print(answer_2)
        ```
    The LLM will then provide answers based on the video's content.

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
