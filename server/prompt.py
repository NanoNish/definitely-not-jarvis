import random
import math

# Special Tokens used by Llama 2
B_INST, E_INST = "[INST]", "[/INST]\n"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

# Other constants
DEFAULT_ASSIST_INSTRUCTIONS = """
You are a helpful, respectful, professional and honest assistant. 
Always answer as helpfully as possible, while being safe. 
Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
Please ensure that your responses are socially unbiased and positive in nature. 
Please keep your responses succinct and to the point.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. 
If you don't know the answer to a question, please don't share false information.\n
"""

DEFAULT_CLASSIFY_INSTRUCTIONS = """You are a classifier. You will receive some
instructions and a user input. You have to classify the user input into the
categories/projects specified below. Respond in one word OR as briefly as possible\n"""

NUM_EXAMPLES = 5

def assist_prompt(faqs, knowledge, query, instructions=DEFAULT_ASSIST_INSTRUCTIONS) -> str:
    # Initial Assistant Instructions and definitions
    PROMPT = "<s>" + B_INST + B_SYS + instructions

    # Knowledge
    PROMPT += "\nYou know the following:\n\n"
    for point in knowledge:
        PROMPT += f"- {point[1]}\n"

    # FAQs
    PROMPT += "\nYou have frequently been asked the following questions:\n\n"
    for question in faqs:
        PROMPT += f"Question: {question[0]}\nAnswer: {question[1]}\n\n"

    # Examples
    examples = random.sample(faqs, min(NUM_EXAMPLES, math.floor(len(faqs)*2/3)))
    PROMPT+= "\nHere are a few examples of conversations you have had:\n\n"
    for example in examples:
        PROMPT += f"user: {example[0]}\nyou: {example[1]}\n\n"

    # Append user input
    PROMPT += E_SYS + query + E_INST

    return PROMPT


def classify_prompt(knowledge: list[tuple[str, str]], query: str, instructions=DEFAULT_CLASSIFY_INSTRUCTIONS) -> tuple[str, str]:
    # Initial Assistant Instructions and definitions
    prompt1 = "<s>" + B_INST + B_SYS + instructions
    prompt2 = "<s>" + B_INST + B_SYS + instructions

    # Knowledge
    prompt2 += "\nYou know the following about the projects:\n\n"
    for k in knowledge:
        prompt2 += f"Project name: {k[0]}\nAbout project: {k[1]}\n\n"

    prompt1 += """Classify the user query, with one of the following categories: 'bug', 'issue',
    'how-to', 'request', or 'feature', following the provided format. You should just give one word as output,
    and it should be a category mentioned previously."""

    prompt2 += """Classify the user query, into the relevant project. You should just give a single project
    name as output of the ones mentioned previously. If no project seems relevant, give output as 'general'."""

    # Append user input
    prompt1 += E_SYS + query + E_INST
    prompt2 += E_SYS + query + E_INST

    return prompt1, prompt2
