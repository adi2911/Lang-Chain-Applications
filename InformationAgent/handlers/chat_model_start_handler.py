from pyboxen import boxen
from langchain.callbacks.base import BaseCallbackHandler


def boxen_print(*args, **kwargs):
    print(boxen(*args,**kwargs))

class ChatModelStartHandler(BaseCallbackHandler):
    def on_chat_model_start(self, serialized,messages,**kwargs):
        print("\n\n\n\n =============Sending Messages==================\n\n\n\n")

        #assuming only one list of messages present
        for message in message[0]:
            if message.type == "system":
                boxen_print(message.content,title=message.type,color="yellow")
            
            elif message.type == "human":
                boxen_print(message.content,title=message.type,color="green")
            
            elif message.type == "ai" and "fuction_call" in message.additional_kwargs:
                call = message.additional_kwargs["function_call"]
                boxen_print(f"Running tool {call['name']} with args {call['arguments']}" ,
                            title=message.type,color="cyan")

            elif message.type == "ai":
                boxen_print(message.content,title=message.type,color="blue")

            elif message.type == "function":
                boxen_print(message.content,title=message.type,color="purple")

            else:
                boxen_print(message.content, title=message.type)
            
            

