import json 
import datetime as dt
import streamlit as st

def load_questions(project_id, time_id):
    """Load questions from a JSON file for a given project and time ID."""
    path = f"output/{project_id}/mongoDB_{time_id}.json"
    with open(path, 'r') as f:
        data = json.load(f)
    return data['questions']

def display_questions(questions):
    """Display questions in the console and capture user responses."""
    user_answers = []
    for idx, q in enumerate(questions):
        print(f"{idx + 1}. {q['questionText']}")
        for cidx, choice in enumerate(q['choices']):
            print(f"   {cidx + 1}. {choice}")
        answer = input("Your answer (number): ")
        user_answers.append(int(answer))
    return user_answers

def check_answers(questions, user_answers):
    """Check user's answers and return the count of correct answers and feedbacks."""
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

def store_performance(project_id, correct_count, total_questions):
    """Store the user's performance data as a JSON file."""
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
    """Run the Streamlit app to allow users to answer questions and view their performance."""
    st.title("Exam Questions")
    uploaded_file = st.file_uploader("Choose a JSON file", type="json")

    if uploaded_file:
        data = json.load(uploaded_file)
        questions = data['questions']
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
                    st.write(f"**Explanation:** {explanation}\n\n---")  # Horizontal line in Streamlit for separation
                
                st.write(f"You got **{correct_count}/{len(questions)}** questions correct!")

if __name__ == "__main__":
    run_streamlit()
