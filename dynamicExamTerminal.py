import json 
import datetime as dt
import streamlit as st

# This function loads the generated question
def load_questions(project_id, time_id):
    path = f"output/{project_id}/mongoDB_{time_id}.json"
    with open(path, 'r') as f:
        data = json.load(f)
    return data['questions']

# This function displays the questions to the user 
def display_questions(questions):
    user_answers = []
    for idx, q in enumerate(questions):
        print(f"{idx + 1}. {q['questionText']}")
        for cidx, choice in enumerate(q['choices']):
            print(f"   {cidx + 1}. {choice}")
        answer = input("Your answer (number): ")
        user_answers.append(int(answer))
    return user_answers

def check_answers(questions, user_answers):
    correct_count = 0
    feedbacks = []
    for idx, q in enumerate(questions):
        correct_choice = q['choices'].index(q['correctAnswer']) + 1
        is_correct = correct_choice == user_answers[idx]
        if is_correct:
            feedbacks.append((f"Question {idx + 1}: **Correct!**", q['explanation']))
            correct_count += 1
        else:
            feedbacks.append((f"Question {idx + 1}: **Incorrect.** Correct answer: {q['correctAnswer']}", q['explanation']))
    return correct_count, feedbacks

# This function stores the performance of the user
def store_performance(project_id, correct_count, total_questions):
    now = dt.datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    path = f'./output/{project_id}/performance_{current_time}.json'
    performance = {
        'correct': correct_count,
        'total': total_questions,
        'percentage': (correct_count / total_questions) * 100
    }
    with open(path, 'w') as f:
        json.dump(performance, f)

def run_streamlit():
    st.title("Exam Questions")
    
    # Select a project ID
    project_id = st.text_input("Enter project ID:", "")
    
    # Load questions if a project ID is entered
    if project_id:
        questions = load_questions(project_id, "10_07")
        
        # Display questions using Streamlit widgets
        user_answers = [None] * len(questions)  # Initialize with None

        for idx, q in enumerate(questions):
            st.subheader(f"{idx + 1}. {q['questionText']}")
            answer = st.radio(f"Choices for Question {idx + 1}", options=q['choices'], index=None, key=idx)
            
            # Only update user_answers if a valid answer is provided
            if answer is not None:
                user_answers[idx] = q['choices'].index(answer) + 1

        # Button to submit answers
        if st.button("Submit Answers"):
            if None in user_answers:
                st.warning("Please answer all the questions before submitting!")
            else:
                correct_count, feedbacks = check_answers(questions, user_answers)
                
                for idx, (feedback, explanation) in enumerate(feedbacks):
                    st.markdown(feedback)
                    st.write(f"**Explanation:** {explanation}\n\n---")  # The '---' will create a horizontal line in Streamlit for separation
                
                st.write(f"You got **{correct_count}/{len(questions)}** questions correct!")
                store_performance(project_id, correct_count, len(questions))




if __name__ == "__main__":

    run_streamlit()
    
    # This code prompts the user to enter their project ID, loads the questions
    # for the project, displays them to the user, and then checks the user's
    # answers and prints the number of correct answers.

    # project_id = input("Enter project ID: ")
    # questions = load_questions(project_id, "10_07")
    # user_answers = display_questions(questions)
    # correct_count = check_answers(questions, user_answers)
    # store_performance(project_id, correct_count, len(questions))
    # print(f"You got {correct_count}/{len(questions)} questions correct!")