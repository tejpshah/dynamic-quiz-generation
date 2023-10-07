import openai 
from promptTemplates import summarizerSystemPrompt
from config import OPENAI_API_KEY

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY 

# Read and store the text from the input file
inputFile = open("data/sample.txt", "r")
inputText = inputFile.read()
inputFile.close()

def generateSummary(system_prompt, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"This is the input below:\n{context}"},
        ]
    )
    return response['choices'][0]['message']['content']

print(generateSummary(summarizerSystemPrompt, inputText))

