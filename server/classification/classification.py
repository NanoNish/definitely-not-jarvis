
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
MODEL_ID = "llama2-70b-chat"
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
Classify the Provided Query as 'issue', 'request', 'bug', 'feature', 'how-to issue':
Example: 
Query: This Github repo has degraded packages.
Answer:issue
Example: 
Query: How can I access the clarifai model from my workflow?
Answer:how-to-issue
Example: 
Query: The model keeps on throwing this error on this particular prompt.
Answer:bug
Example:
Query: How to get pass this server auth?
Answer:how-to-issue

Query: {question}
Answer:"""


prompt = PromptTemplate(template=template, input_variables=["question"])
# Create LLM chain
llm_chain = LLMChain(prompt=prompt, llm=clarifai_llm)

""" The User Prompt"""
question = "render overflow error"

string_list = llm_chain.run(question).split("\n")
res = string_list[0]
print(res)
