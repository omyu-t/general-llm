from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.retrievers import TavilySearchAPIRetriever
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()


def find_message():
    return "this is message."


async def chat_openai_stream(question: str):
    prompt = ChatPromptTemplate.from_template(
        '''
        以下の文脈だけを踏まえて質問に回答してください。

        文脈："""{context}"""

        質問：{question}
    '''
    )

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)

    retriever = TavilySearchAPIRetriever(k=3)

    chain = {
        "context": retriever,
        "question": RunnablePassthrough(),
    } | RunnablePassthrough.assign(answer=(prompt | model | StrOutputParser()))

    async for token in chain.astream(input=question):
        if "answer" in token and isinstance(token["answer"], str):
            yield token["answer"]


async def chat_openai(question: str):
    prompt = ChatPromptTemplate.from_template(
        '''
        以下の文脈だけを踏まえて質問に回答してください。

        文脈："""{context}"""

        質問：{question}
    '''
    )

    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    retriever = TavilySearchAPIRetriever(k=3)

    chain = {
        "context": retriever,
        "question": RunnablePassthrough(),
    } | RunnablePassthrough.assign(answer=(prompt | model | StrOutputParser()))

    return await chain.ainvoke(input=question)
