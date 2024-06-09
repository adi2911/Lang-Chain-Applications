from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain



import argparse
from dotenv import load_dotenv

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--task",default="return list of number")
parser.add_argument("--language",default="python")
args = parser.parse_args()


llm = OpenAI() #Takes api key by default from .env folder, it should be specifically name : OPENAI_API_KEY

generate_code_prompt = PromptTemplate(
    template = "Write a very short {language} function that will {task}",
    input_variables =  ["language","task"]
)

generate_code_chain = LLMChain(
    llm=llm,
    prompt=generate_code_prompt,
    output_key="code"
)   

# generated_code = generate_code_chain({
#     "language":args.language,
#     "task":args.task
# })

#result is a dictonary of both input field and output field.
#By default the output comes inside the text field, which can be customised as required 
#We have customised it to : code




test_code_prompt = PromptTemplate(
    template= "Write a test for the following {language} code:\n{code}",
    input_variables= ["language","code"]
)


test_code_chain = LLMChain(
    llm=llm,
    prompt=test_code_prompt,
    output_key="result"
)   

seq_chain = SequentialChain(
    chains = [generate_code_chain,test_code_chain],
    input_variables=["task","language"],
    output_variables=["result","code"]
)

test_and_generated_code = seq_chain({
    "language": args.language,
    "task": args.task
})

print(test_and_generated_code["code"])
print(test_and_generated_code["result"])

