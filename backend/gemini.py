from config import settings
import google.generativeai as genai
from main import client, settings

genai.configure(api_key=settings.GEMINI_API_KEY)

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings,
)


def get_summary(context, code):
    prompt = f"""
Please provide a concise and informative summary of the following code from the file '{context}'.
Your summary should be understandable to a developer who is new to the project.

Your summary should include:
- A high-level overview of the code's purpose and functionality.
- A description of the key functions, classes, and their roles.
- Any important dependencies or external libraries used in the code.

Here is the code:
{code}
"""
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return convo.last.text


def get_embeddings(text):
    result = genai.embed_content(
        model="models/embedding-001",
        content=text,
        task_type="SEMANTIC_SIMILARITY",
    )
    return result["embedding"]


def retrieve_documents(question, context):
    response = client.query.hybrid(
        query=question,
        alpha=0.7,  # Give more weight to vector search
        namespace=context,
        properties=["source", "code", "summary"],
        limit=10
    )
    return response['data']['Get'][settings.WEAVIATE_INDEX]

def generate_answer(question, context, documents):
    prompt = f"""
You are a helpful AI assistant that answers questions about a GitHub repository.
You will be given a question and a set of documents retrieved from the repository.
Your task is to answer the question based on the provided documents.

Here is the question:
{question}

Here are the relevant documents:
{documents}

Please provide a comprehensive answer to the question based on the documents.
You should cite the sources of your answer by referencing the file paths of the documents.
If the documents don't contain enough information to answer the question, please state that you couldn't find an answer in the provided documents.
"""
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return convo.last.text

def ask(question, context):
    documents = retrieve_documents(question, context)
    answer = generate_answer(question, context, documents)
    return answer


def summarise_commit(diff):
    prompt = f"Summarize the following diff:\n\n{diff}"
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return convo.last.text
