from config import settings
import weaviate
import assemblyai as aai
import asyncio
import hashlib
from gemini import get_embeddings, ask
from langchain.text_splitter import RecursiveCharacterTextSplitter

client = weaviate.Client(
    url=f"https://{settings.WEAVIATE_ENVIRONMENT}.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key=settings.WEAVIATE_API_KEY),
)
index = client.schema.get(settings.WEAVIATE_INDEX)

aai.settings.api_key = settings.AAI_TOKEN

def serialise_url(url):
    return url.replace("/", "_")

def ms_to_time(ms):
    seconds = ms / 1000
    minutes = seconds / 60
    seconds = seconds % 60
    minutes = minutes % 60
    return "%02d:%02d" % (minutes, seconds)

async def transcribe_file(url):
    config = aai.TranscriptionConfig(auto_chapters=True)
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(url)
    summaries = []
    for chapter in transcript.chapters:
        summaries.append(
            {
                "start": ms_to_time(chapter.start),
                "end": ms_to_time(chapter.end),
                "gist": chapter.gist,
                "headline": chapter.headline,
                "summary": chapter.summary,
            }
        )

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=130)
    docs = splitter.create_documents([transcript.text])

    embeddings = await asyncio.gather(
        *[get_embeddings(doc.page_content) for doc in docs]
    )
    print("getting embeddings for audio")
    for i, doc in enumerate(docs):
        doc.metadata["embeddings"] = embeddings[i]

    index.data.insert_many(
        [
            {
                "uuid": hashlib.md5(doc.page_content.encode()).hexdigest(),
                "properties": {
                    "page_content": doc.page_content,
                },
                "vector": doc.metadata["embeddings"],
            }
            for doc in docs
        ],
        namespace=serialise_url(url),
    )
    print("upserted audio embeddings")
    return summaries


async def ask_meeting(url, query, quote):
    namespace = serialise_url(url)

    query_vector = await get_embeddings(query)
    query_response = index.query.fetch_objects(
        namespace=namespace,
        include_vector=True,
        after=query_vector,
        limit=10,
    )

    context = ""
    for item in query_response.objects:
        context += f"""meeting snippet: {item.properties['page_content']}
"""

    prompt = f"""I am asking a question in regards to this quote in the meeting: {quote}
    here is the question: {query}

    CONTEXT BLOCK
    {context}
    END OF CONTEXT BLOCK
    """
    answer = await ask(prompt, "meeting transcript")
    print("got back answer for", query)

    return answer
