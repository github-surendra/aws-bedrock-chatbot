import boto3
import streamlit as st
import os
import uuid

## s3_client
s3_client = boto3.client("s3", region_name="us-east-1")
BUCKET_NAME = os.getenv("BUCKET_NAME")

## Bedrock
from langchain_aws import BedrockEmbeddings
from langchain_aws import ChatBedrock

## Prompt and Chain - ✅ No more RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

## Text Splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

## Pdf Loader
from langchain_community.document_loaders import PyPDFLoader

## FAISS
from langchain_community.vectorstores import FAISS

## Bedrock client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
)

## Embeddings
bedrock_embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v1",
    client=bedrock_client
)

folder_path = "/tmp/"

def get_unique_id():
    return str(uuid.uuid4())

## Load index from S3
def load_index():
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.faiss", Filename=f"{folder_path}my_faiss.faiss")
    s3_client.download_file(Bucket=BUCKET_NAME, Key="my_faiss.pkl", Filename=f"{folder_path}my_faiss.pkl")

## LLM
def get_llm():
    llm = ChatBedrock(
        model_id="openai.gpt-oss-safeguard-20b",
        client=bedrock_client,
        model_kwargs={"max_tokens": 512}
    )
    return llm

## ✅ get_response using LCEL instead of RetrievalQA
def get_response(llm, vectorstore, question):
    prompt_template = """
    Human: Please use the given context to provide concise answer to the question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    <context>
    {context}
    </context>

    Question: {question}

    Assistant:"""

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    ## ✅ LCEL chain — replaces RetrievalQA completely
    qa_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | PROMPT
        | llm
        | StrOutputParser()
    )

    return qa_chain.invoke(question)

## main
def main():
    st.header("This is Client Site for Chat with PDF demo using Bedrock, RAG etc")

    load_index()

    dir_list = os.listdir(folder_path)
    st.write(f"Files and Directories in {folder_path}")
    st.write(dir_list)

    ## Load FAISS index
    faiss_index = FAISS.load_local(
        index_name="my_faiss",
        folder_path=folder_path,
        embeddings=bedrock_embeddings,
        allow_dangerous_deserialization=True
    )

    st.write("INDEX IS READY")
    question = st.text_input("Please ask your question")
    if st.button("Ask Question"):
        with st.spinner("Querying..."):
            llm = get_llm()
            st.write(get_response(llm, faiss_index, question))
            st.success("Done")

if __name__ == "__main__":
    main()