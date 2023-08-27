
# Install required dependencies
# ! pip install clarifai
# ! pip install -upgrade langchain
# ! pip install --upgrade typing-extensions


# Please login and get your API key from  https://clarifai.com/settings/security
from getpass import getpass
# CLARIFAI_PAT = getpass()
CLARIFAI_PAT = "..." # User's Personal Access Tokens of Clarifai

# Import the required modules
from langchain.llms.clarifai import Clarifai
from langchain import PromptTemplate, LLMChain

USER_ID = "meta"
APP_ID = "Llama-2"
MODEL_ID = "llama2-13b-chat"
# You can provide a specific model version as the model_version_id arg.
# MODEL_VERSION_ID = "MODEL_VERSION_ID"

# Initialize a Clarifai LLM
clarifai_llm = Clarifai(
    pat=CLARIFAI_PAT, user_id=USER_ID, app_id=APP_ID, model_id=MODEL_ID
)

# --------------------------------------------------------------
# Create a PromptTemplate and LLMChain
# --------------------------------------------------------------

template = """
Classify the Provided Query as 'issue', 'request', 'bugs', 'feature', 'how-to issues':
Example: 
Query: This Github repo has degraded packages.
Answer:issue.
Example: 
Query: How can I access the clarifai model from my workflow?
Answer:how-to-issues.
Example: 
Query: The model keeps on throwing this error on this particular prompt.
Answer:bugs.
Example:
Query: How to get pass this server auth?
Answer:how-to-issues.

Query: {question}
Answer:"""


prompt = PromptTemplate(template=template, input_variables=["question"])
# Create LLM chain
llm_chain = LLMChain(prompt=prompt, llm=clarifai_llm)

""" The User Prompt"""
question = "How can I contact the manager?"

res = llm_chain.run(question)

print(res)


