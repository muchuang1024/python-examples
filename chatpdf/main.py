#!/usr/bin/env python3
# 需要安装一些依赖 pip3 install -r

from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.chains.retrieval_qa.base import RetrievalQA

# 需要设置OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = "sk-xxx"

# 提示用户输入文件名，支持pdf文件和普通文本文件
file_path = input("input pdf path: ")

# 根据文件类型来定义一个loader，不同的loader能够解析不同的文件内容，最终都会解析为一个大文本
loader = file_path.endswith(".pdf") and PyPDFLoader(file_path) or TextLoader(file_path)

# 定义文本分块的规则，这里用了一个很简单的规则，按照默认的分隔符来切割文本，使得每一段不超过1000个字符
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
chunks = loader.load_and_split(splitter)

# 定义文本的embedding，也就是如何把文本转换为向量。默认使用sentence-transformers这个免费的模型，也可以使用OpenAI提供的收费接口
# embeddings = OpenAIEmbeddings()
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# 实现一个本地的文档语义搜索，在存入一堆chunk之后，能够随时检索和问题最相关的一些chunk。Chroma就是一个比较流行的vector store
db = Chroma.from_documents(chunks, embeddings)

# 本地搜索到的chunk会作为context，和问题一起提交给LLM来处理。我们当然要使用ChatGPT模型了，比GPT-3.0又好又便宜
llm = ChatOpenAI(temperature=0)

# chain是LangChain里的概念，其实就相当于定义了一个流程，这里我们提供的参数就是文档语义搜索工具以及LLM
chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())

# 下面就比较简单了，不断读取问题然后执行chain
while True:
    question  = input("\nQ: ")
    if not question:
        break
    print("A:", chain.run(question))