import openai 
from promptTemplates import summarizerSystemPrompt, questionGeneratorSystemPrompt, questionCritiquerSystemPrompt, convertToMongoDBSystemPrompt
from config import OPENAI_API_KEY
import os
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
import re
import datetime
import argparse


# Set up configurations 
openai.api_key= OPENAI_API_KEY

# This function extracts all the text from the files in the data directory
def extract_all_text_in_data_directory(directory="data/"):
    all_text = []

    # List all the files in the directory
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # Check if the file is a PDF
        if file_name.endswith('.pdf'):
            try:
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PdfReader(pdf_file)
                    for page in pdf_reader.pages:
                        all_text.append(page.extract_text())
                    print(f"Successfully processed {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

        # Check if the file is a text file
        elif file_name.endswith('.txt'):
            try:
                with open(file_path, 'r', encoding='utf-8') as text_file:
                    all_text.append(text_file.read())
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    return ''.join(all_text)

# This function generates a summary from a given text
def generateSummary(system_prompt, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"This is the input below:\n{context}"},
        ]
    )
    return response['choices'][0]['message']['content']

# This function generates questions from a given text
def generateQuestions(system_prompt, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Make questions on the following content:\n{context}"},
        ]
    )
    return response['choices'][0]['message']['content']

# This function critiques questions from a given text
def critiqueQuestions(system_prompt, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Critique the set of questions generated:\n{context}"},
        ]
    )
    return response['choices'][0]['message']['content']

# This function finalizes questions from a given text
def finalizedQuestions(system_prompt, context, critiques):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"This is the content you're making questions on: \n{context}\n These are the critiques you've recieved: \n{critiques}. Your revised questions are:"},
        ]
    )
    return response['choices'][0]['message']['content']

# This function converts questions to MongoDB format
def convertToMongoDB(system_prompt, context):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Convert the questions to MongoDB format:\n{context}"},
        ]
    )
    return response['choices'][0]['message']['content']

def text_to_pdf(text, pdf_filename="questions.pdf"):
    # Split the text into individual questions
    questions = re.split(r'\d+\.', text)[1:]  # Split by numbers followed by a dot
    
    # Create a new PDF document
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    
    # Define styles for the PDF
    styles = getSampleStyleSheet()
    
    # Create an empty list to hold the PDF content
    content = []
    
    for question in questions:
        lines = question.strip().split('\n')
        for line in lines:
            content.append(Paragraph(line.strip(), styles['Normal']))
            content.append(Spacer(1, 12))  # Add a space after each line for clarity
        content.append(PageBreak())
    
    # Build the PDF document with the content
    doc.build(content)

def create_new_folder():
    output_dir = "output"
    num_folders = len(os.listdir(output_dir))
    new_folder_name = str(num_folders)
    new_folder_path = os.path.join(output_dir, new_folder_name)
    os.mkdir(new_folder_path)
    return new_folder_path

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_directory", help="path to data directory")
    args = parser.parse_args()

    # Read and store the text from the input file
    inputText = extract_all_text_in_data_directory(args.data_directory if args.data_directory else "data/")

    # Generate the summary and questions
    summary = generateSummary(summarizerSystemPrompt, inputText)
    print("SUMMARY\n" + summary + "\n")

    questions = generateQuestions(questionGeneratorSystemPrompt, summary)
    print("QUESTIONS\n" + questions + "\n")

    critiques = critiqueQuestions(questionCritiquerSystemPrompt, questions)
    print("CRITIQUES\n" + critiques + "\n")

    finalized = finalizedQuestions(questionGeneratorSystemPrompt, summary, critiques)
    print("FINALIZED\n" + finalized + "\n")

    mongoDB = convertToMongoDB(convertToMongoDBSystemPrompt, finalized)
    print("MONGODB\n" + mongoDB + "\n")

    # Automatically create a new folder in "output" based on number
    new_folder_path = create_new_folder()
    mm_day = datetime.datetime.now().strftime("%m_%d")

    # Save the questions to a PDF file
    text_to_pdf(finalized, f"{new_folder_path}/questions_{mm_day}.pdf")

    # Write the summary of the file path to an output file
    outputFile = open(f"{new_folder_path}/summary_{mm_day}.txt", "w")
    outputFile.write(summary)
    outputFile.close()

    # Write the questions of the file path to an output file
    outputFile = open(f"{new_folder_path}/questions_{mm_day}.txt", "w")
    outputFile.write(finalized)
    outputFile.close()

    # Write the MongoDB of the file path to an output file BSON
    outputFile = open(f"{new_folder_path}/mongoDB_{mm_day}.bson", "w")
    outputFile.write(mongoDB)
    outputFile.close()


