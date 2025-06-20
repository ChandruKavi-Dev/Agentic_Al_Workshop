import os
import requests
from bs4 import BeautifulSoup
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from app.models.schemas import HospitalCulture

def get_text_from_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    except Exception:
        return ""

def extract_hospital_culture(url: str, docs_text: str) -> dict:
    """Uses RAG with Gemini to extract hospital cultural traits."""
    parser = JsonOutputParser(pydantic_object=HospitalCulture)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

    # Use Google's own embedding model for a consistent stack
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY"))
    
    all_text = docs_text + " " + get_text_from_url(url)
    if not all_text.strip():
        return {"core_values": ["Not Found"], "work_environment": "Not Found", "mission_focus": "Not Found"}

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
    splits = text_splitter.split_text(all_text)

    vectorstore = Chroma.from_texts(texts=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever()
    
    system_prompt = (
        "You are an expert analyst of healthcare organizational culture. "
        "Use the provided context to extract the hospital's core values, work environment, and mission focus. "
        "Your output must be a valid JSON object that conforms to the provided schema."
        "\n\n"
        "CONTEXT: {context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Based on the context, extract the hospital's cultural traits. {format_instructions}"),
    ])
    
    Youtube_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, Youtube_chain)

    response = rag_chain.invoke({
        "input": "Extract hospital cultural traits from the provided context.",
        "format_instructions": parser.get_format_instructions()
    })
    
    return parser.parse(response["answer"])