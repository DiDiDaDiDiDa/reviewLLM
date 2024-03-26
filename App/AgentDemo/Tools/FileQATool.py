 
from typing import List

from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.word_document import UnstructuredWordDocumentLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.llms.openai import OpenAI
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_file_extension(filename: str) -> str:
    return filename.split(".")[-1]


class FileLoadFactory:
    @staticmethod
    def get_loader(fileName: str):
        ext = get_file_extension(fileName)
        if ext == "pdf":
            return PyPDFLoader(fileName)
        elif ext == "docx" or ext == "doc":
            return UnstructuredWordDocumentLoader(fileName)
        else:
            raise NotImplementedError(f"File extension {ext} not supported.")


def load_docs(filename: str) -> List[Document]:
    file_loader = FileLoadFactory.get_loader(filename)
    pages = file_loader.load_and_split()
    return pages


def ask_docment(
        filename: str,
        query: str,
) -> str:
    """根据一个PDF文档的内容，回答一个问题"""

    raw_docs = load_docs(filename)
    if len(raw_docs) == 0:
        return "抱歉，文档内容为空"
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    documents = text_splitter.split_documents(raw_docs)
    if documents is None or len(documents) == 0:
        return "无法读取文档内容"
    db = Chroma.from_documents(documents, OpenAIEmbeddings(model="text-embedding-ada-002"))
    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(
            temperature=0,
            model_kwargs={
                "seed": 42
            },
        ),  # 语言模型
        chain_type="stuff",  # prompt的组织方式，后面细讲
        retriever=db.as_retriever()  # 检索器
    )
    response = qa_chain.run(query + "(请用中文回答)")
    return response


if __name__ == "__main__":
    filename = "../data/2023年10月份销售计划.docx"
    query = "销售额达标的标准是多少？"
    response = ask_docment(filename, query)
    print(response)
