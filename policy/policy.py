import json
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool
from langchain_community.embeddings import OllamaEmbeddings


def load_documents_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        documents = [(item['question'], item['answer']) for item in data]
    langchain_docs = []
    for d in documents:
        question, answer = d
        langchain_docs.append(Document(page_content=answer, metadata={"source": question}))

    return langchain_docs


class VectorStoreRetriever:
    def __init__(self, docs: list):
        self._docs = docs

    @classmethod
    def from_file(cls, path):
        docs = load_documents_from_json(path)
        return cls(docs)

    def query(self, query: str, k: int = 5) -> list[Document]:
        vectorstore = Chroma.from_documents(
            self._docs,
            embedding=OllamaEmbeddings(),
        )

        return RunnableLambda(vectorstore.similarity_search).bind(k=k).invoke(query)


@tool
def lookup_policy(retriever: VectorStoreRetriever, query: str) -> str:
    docs = retriever.query(query, k=2)
    return "\n\n".join([doc["page_content"] for doc in docs])
