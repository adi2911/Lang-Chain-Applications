from langchain.prompts import MessagesPlaceholder,HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv

from langchain.memory import ConversationSummaryMemory #ConversationBufferMemory, FileChatMessageHistory



chat  = ChatOpenAI()

#memory_key is the additional field we will provide with the list of messages.
#return_messages is telling the LangChain to use it as a completion side model,
# an inteligently wrapup random sttrings in meaningful objects
memory = ConversationSummaryMemory(memory_key="messages",
                                  return_messages=True,
                                llm=chat) # We have to provide llm which it will use for summarization


#ConversationBufferMemory(memory_key="messages",
  #                                return_messages=True,
  #                                 chat_memory=FileChatMessageHistory("messages.json")) # message.json to store it in a file Not very useful


prompt = ChatPromptTemplate(
    input_variables=["content","messages"],
    messages=[
        MessagesPlaceholder(variable_name = "messages"), # Tell to check the input variable messages.
        HumanMessagePromptTemplate.from_template("{content}") # this is human message we got from the terminal
    ]
)


chain = LLMChain(
    llm= chat,
    prompt=prompt,
    memory=memory,
    verbose=True  # For logging  the logs
)




while True:
    content = input(">> ") #input
    result = chain({"content":content})
    print(">> "+result["text"])