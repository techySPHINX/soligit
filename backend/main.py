import os
import asyncio
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






@app.post("/generate_documentation")
async def generate_documentation(body: GenerateDocumentationRequest):
    github_loader = GithubLoader()
    raw_documents = github_loader.load(body.github_url)
    file_tree = [i.metadata["source"] for i in raw_documents]
    mermaid_graph = generate_file_tree_graph(file_tree)

    print("mermaid", mermaid_graph)
    summaries = await asyncio.gather(
        *[get_summary(doc.metadata["source"], doc.page_content) for doc in raw_documents]
    )
    # print(summaries)
    for i, doc in enumerate(raw_documents):
        doc.metadata["summary"] = summaries[i]

    embeddings = await asyncio.gather(
        *[get_embeddings(doc.metadata["summary"]) for doc in raw_documents]
    )
    print("got summary")
    for i, doc in enumerate(raw_documents):
        doc.metadata["embedding"] = embeddings[i]
    print("got embeddings")

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

    index.data.insert_many(
        objects_to_insert,
        namespace=serialise_github_url(body.github_url),
    )
    answers = await asyncio.gather(
        *[
            ask(question, serialise_github_url(body.github_url))
            for question in QUESTIONS
        ]
    )
    documentation = []
    for i, question in enumerate(QUESTIONS):
        documentation.append({"question": question, "answer": answers[i]})

    project_name = body.github_url.split("/")[-1]
    documentation_html = generate_documentation_html(project_name, documentation, mermaid_graph)

    return {"documentation": documentation_html, "mermaid": mermaid_graph}


@app.post("/ask")
async def query(body: AskRequest):
    response = await ask(body.query, serialise_github_url(body.github_url))
    return {"message": response}


class summariseCommitBody(BaseModel):
    commitHash: str
    github_url: str


@app.post("/summarise-commit")
def summariseCommits(body: summariseCommitBody):
    import requests

    response = requests.get(
        f"{body.github_url}/commit/{body.commitHash}.diff",
        headers={
            "Accept": "application/vnd.github.v3.diff",
            "Authorization": f"token {os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')}",
        },
    )
    summary = summarise_commit(str(response.content[:10000]))
    print("summary for commit", summary)
    return {"summary": summary}


class transcribeMeetingBody(BaseModel):
    url: str


@app.post("/transcribe-meeting")
async def transcribeMeeting(body: transcribeMeetingBody):
    print("transcribing", body.url)
    summaries = await transcribe_file(body.url)
    return {"summaries": summaries}


class askMeetingBody(BaseModel):
    url: str
    quote: str
    query: str


@app.post("/ask-meeting")
async def askMeeting(body: askMeetingBody):
    response = await ask_meeting(body.url, body.query, body.quote)
    return {"answer": response}


# async def main():
#     embeddings = await asyncio.gather(*[getEmbeddings(text) for text in texts])
#     print(len(embeddings))


# asyncio.run(main())