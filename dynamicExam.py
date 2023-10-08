import json 
import datetime as dt

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

# This function checks the answers and returns the number of correct answers
def check_answers(questions, user_answers):
    correct_count = 0
    for idx, q in enumerate(questions):
        correct_choice = q['choices'].index(q['correctAnswer']) + 1
        is_correct = correct_choice == user_answers[idx]
        if is_correct:
            print(f"Question {idx + 1}: Correct!")
            correct_count += 1
        else:
            print(f"Question {idx + 1}: Incorrect. Correct answer: {q['correctAnswer']}")
    return correct_count

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

if __name__ == "__main__":
    
    # This code prompts the user to enter their project ID, loads the questions
    # for the project, displays them to the user, and then checks the user's
    # answers and prints the number of correct answers.

    project_id = input("Enter project ID: ")
    questions = load_questions(project_id, "10_07")
    user_answers = display_questions(questions)
    correct_count = check_answers(questions, user_answers)
    store_performance(project_id, correct_count, len(questions))
    print(f"You got {correct_count}/{len(questions)} questions correct!")