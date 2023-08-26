import random
import math

# Special Tokens used by Llama 2
B_INST, E_INST = "[INST]", "[/INST]\n"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

# Other constants
DEFAULT_INSTRUCTIONS = """
You are a helpful, respectful, professional and honest assistant. 
Always answer as helpfully as possible, while being safe. 
Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. 
Please ensure that your responses are socially unbiased and positive in nature. 
Please keep your responses succinct and to the point.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. 
If you don't know the answer to a question, please don't share false information.\n
"""
NUM_EXAMPLES = 5

def prompt(faqs, knowledge, query, instructions=DEFAULT_INSTRUCTIONS):
    # Initial Assistant Instructions and definitions
    PROMPT = "<s>" + B_INST + B_SYS + instructions

    # Knowledge
    PROMPT += "\nYou know the following:\n\n"
    for point in knowledge:
        PROMPT += f"- {point}\n"

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

"""
Example Usage: 

faqs = [("What is MDG Space, IITR?", "MDG Space, IITR is student group that codes"),
        ("Does BURG3R5 enjoy burgers?", "BURG3RS enjoys all kinds of food"),
        ("What is a Turing Machine?", "A Turing machine is a mathematical model of computation describing an abstract machine that manipulates symbols on a strip of tape according to a table of rules.")
        ]
knowledge = ["Orange, the fruit, is older than orange, the color",
            "IITR stands for the Indian Institute of Technology Roorkee",
            "BURG3R5 is a member of MDG Space, IITR"]

prompt(faqs,knowledge,"Do members of MDG Space at the Indian Institute of Technology Roorkee enjoy burgers?")
"""
