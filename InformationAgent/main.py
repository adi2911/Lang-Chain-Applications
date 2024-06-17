from langchain.chat_models import ChatOpenAI
from langchain.prompts import (ChatPromptTemplate,HumanMessagePromptTemplate,MessagesPlaceholder)
from langchain.agents import OpenAIFunctionsAgent,AgentExecutor
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool
from handlers.chat_model_start_handler import ChatModelStartHandler

load_dotenv()

handler = ChatModelStartHandler()
chat =ChatOpenAI(callbacks = [handler])

tables = list_tables()

system_message =  '''You are an AI that has access to a SQLite database.\n
                    f"The database has tables of: {tables} \n"
                    Do not make assumption about what tables exist or what columns exist. Instead , use the 'describle_tables' function. '''


chatPrompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content = system_message),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history",return_messages = True)

runningTools = [run_query_tool, describe_tables_tool,write_report_tool]

agent = OpenAIFunctionsAgent(llm=chat, prompt=chatPrompt, tools=runningTools)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True,
    tools = runningTools,
    memory=memory
)


agent_executor("How many users are in the database") #2000 users should be the output

#generating report
agent_executor("Summarise the top 5 most popular products. Write the results to a report file")