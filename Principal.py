from langchain_community.agent_toolkits import GmailToolkit
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

'''Load the environment variables'''
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


'''Create the GmailToolkit object'''
toolkit = GmailToolkit()

'''Get the tools from the toolkit'''
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)

'''Build the resource service'''
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

'''Create tools, instructions, base_prompt, and prompt for the agent'''
tools = toolkit.get_tools()
instructions = """You are an assistant."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)


'''Create llm object with the ChatOpenAI class and the gpt-4o model'''
llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

'''Create the agent using the create_openai_functions_agent function from the langchain library'''
agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)

'''Create the agent executor using the AgentExecutor class from the langchain library'''
agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=False,
)

'''Query the agent using the invoke method of the agent_executor object'''
query = agent_executor.invoke(
    {"input": "What is the date and time of sending the last email sent from namexample?"}
)

'''Save the output to a file called output.txt'''
with open("output.txt", "w") as f:
    r_string = str(query)
    f.write(r_string)