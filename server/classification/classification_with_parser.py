
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
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List

USER_ID = "openai"
APP_ID = "chat-completion"
MODEL_ID = "GPT-4"

# MODEL_VERSION_ID = "e52af5d6bc22445aa7a6761f327f7129"
# Initialize a Clarifai LLM
clarifai_llm = Clarifai(
    pat=CLARIFAI_PAT, user_id=USER_ID, app_id=APP_ID, model_id=MODEL_ID,
)
# You can provide a specific model version as the model_version_id arg.
# MODEL_VERSION_ID = "MODEL_VERSION_ID"

# Defining The Output Parser Setup

# Define your desired data structure.
class Classifier(BaseModel):
    classification: str = Field(description="""The classification of the user query. This will be a string value with one of the     
following possibilities: 'bug', 'issue', 'how-to','request', or 'feature'.""")
    Answer: str = Field(description="""The answer to the user query. This will be a string value that is a brief and concise summary
of the user query and its classification.""")
    
    # You can add custom validation logic easily with Pydantic.
    @validator('classification')
    def classification_ends_with_hashtag(cls, field):
        if field!="issue" and field!="bug" and field!="request" and field!="how-to" and field!="feature":
            raise ValueError("Bad classification!")
        return field


# Set up a parser + inject instructions into the prompt template.
parser = PydanticOutputParser(pydantic_object=Classifier)

prompt = PromptTemplate(
    template="""Classify the user query, with one of the     
following possibilities: 'bug', 'issue', 'how-to','request', or 'feature', following the provided format.
    \n{format_instructions}\n{query}\n""",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)


# And a query intended to prompt a language model to populate the data structure.

classification_query = "How can I contact the manager?"
_input = prompt.format_prompt(query=classification_query)


output = clarifai_llm(_input.to_string())
# print("INPUT:\n",_input.to_string())
# print("OUTPUT:\n",output)
out = parser.parse(output)

print("PARSED OUTPUT\n",out)
