from config import settings
import google.generativeai as genai

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
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)


def get_summary(context, code):
    prompt = f"Summarize the following code in the context of {context}:\n\n{code}"
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


def ask(question, context):
    prompt = f"In the context of {context}, answer the following question: {question}"
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return convo.last.text


def summarise_commit(diff):
    prompt = f"Summarize the following diff:\n\n{diff}"
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    return convo.last.text
