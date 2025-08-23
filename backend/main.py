import os
import asyncio
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from GithubLoader import GithubLoader
import hashlib
from gemini import get_summary, get_embeddings, ask, summarise_commit
from assembly import transcribe_file, ask_meeting
import weaviate
from config import settings
from documentation_generator import generate_documentation_html, generate_file_tree_graph
from questions import QUESTIONS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

client = weaviate.Client(
    url=f"https://{settings.WEAVIATE_ENVIRONMENT}.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key=settings.WEAVIATE_API_KEY),
)
index = client.schema.get(settings.WEAVIATE_INDEX)

app = FastAPI()


class GenerateDocumentationRequest(BaseModel):
    github_url: str


class AskRequest(BaseModel):
    query: str
    github_url: str


def serialise_github_url(url):
    return url.replace("/", "_")


from fastapi import FastAPI, HTTPException, status

# ... (other imports)

@app.post("/generate_documentation")
async def generate_documentation(body: GenerateDocumentationRequest):
    try:
        github_loader = GithubLoader()
        raw_documents = github_loader.load(body.github_url)
    except Exception as e:
        logger.error("Error loading GitHub repository: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to load GitHub repository: {e}"
        )

    file_tree = [i.metadata["source"] for i in raw_documents]
    mermaid_graph = generate_file_tree_graph(file_tree)

    logger.info("mermaid: %s", mermaid_graph)

    try:
        summaries = await asyncio.gather(
            *[get_summary(doc.metadata["source"], doc.page_content) for doc in raw_documents]
        )
        for i, doc in enumerate(raw_documents):
            doc.metadata["summary"] = summaries[i]
    except Exception as e:
        logger.error("Error generating summaries: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate summaries: {e}"
        )

    try:
        embeddings = await asyncio.gather(
            *[get_embeddings(doc.metadata["summary"]) for doc in raw_documents]
        )
        logger.info("Got summary")
        for i, doc in enumerate(raw_documents):
            doc.metadata["embedding"] = embeddings[i]
        logger.info("Got embeddings")
    except Exception as e:
        logger.error("Error generating embeddings: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate embeddings: {e}"
        )

    objects_to_insert = []
    for doc in raw_documents:
        objects_to_insert.append({
            "uuid": hashlib.md5(doc.page_content.encode()).hexdigest(),
            "properties": {
                "source": doc.metadata["source"],
                "code": doc.page_content[:10000],
                "summary": doc.metadata["summary"],
            },
            "vector": doc.metadata["embedding"]
        })

    try:
        index.data.insert_many(
            objects_to_insert,
            namespace=serialise_github_url(body.github_url),
        )
    except Exception as e:
        logger.error("Error inserting data into Weaviate: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to insert data into Weaviate: {e}"
        )

    try:
        answers = await asyncio.gather(
            *[
                ask(question, serialise_github_url(body.github_url))
                for question in QUESTIONS
            ]
        )
        documentation = []
        for i, question in enumerate(QUESTIONS):
            documentation.append({"question": question, "answer": answers[i]})
    except Exception as e:
        logger.error("Error asking questions: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ask questions: {e}"
        )

    project_name = body.github_url.split("/")[-1]
    documentation_html = generate_documentation_html(project_name, documentation, mermaid_graph)

    return {"documentation": documentation_html, "mermaid": mermaid_graph}





@app.post("/ask")
async def query(body: AskRequest):
    try:
        response = await ask(body.query, serialise_github_url(body.github_url))
        return {"message": response}
    except Exception as e:
        logger.error("Error asking question: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ask question: {e}"
        )


class summariseCommitBody(BaseModel):
    commitHash: str
    github_url: str


@app.post("/summarise-commit")
def summariseCommits(body: summariseCommitBody):
    import requests

    try:
        response = requests.get(
            f"{body.github_url}/commit/{body.commitHash}.diff",
            headers={
                "Accept": "application/vnd.github.v3.diff",
                "Authorization": f"token {os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')}",
            },
        )
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        summary = summarise_commit(str(response.content[:10000]))
        logger.info("Summary for commit: %s", summary)
        return {"summary": summary}
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching commit diff from GitHub: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch commit diff from GitHub: {e}"
        )
    except Exception as e:
        logger.error("Error summarising commit: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to summarise commit: {e}"
        )


class transcribeMeetingBody(BaseModel):
    url: str


@app.post("/transcribe-meeting")
async def transcribeMeeting(body: transcribeMeetingBody):
    logger.info("Transcribing: %s", body.url)
    try:
        summaries = await transcribe_file(body.url)
        return {"summaries": summaries}
    except Exception as e:
        logger.error("Error transcribing meeting: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to transcribe meeting: {e}"
        )


class askMeetingBody(BaseModel):
    url: str
    quote: str
    query: str


@app.post("/ask-meeting")
async def askMeeting(body: askMeetingBody):
    try:
        response = await ask_meeting(body.url, body.query, body.quote)
        return {"answer": response}
    except Exception as e:
        logger.error("Error asking meeting question: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ask meeting question: {e}"
        )


# async def main():
#     embeddings = await asyncio.gather(*[getEmbeddings(text) for text in texts])
#     print(len(embeddings))


# asyncio.run(main())
