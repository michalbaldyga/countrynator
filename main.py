from Tree import *
from utils import *
from probability import *


def main():
    categories = create_categories()
    countries_answers, countries = load_data()

    questions_dict = {}
    countries_questions = list(range(len(countries)))
    question_numbers = list(range(len(countries_questions)))
    for i in question_numbers:
        questions_dict[i] = countries_questions[i]

    t = Tree()
    questions_number = len(countries[0]) - 1

    questions_so_far = []
    answers_so_far = []
    deleted_questions = 0

    while True:

        my_tree = t.build_tree(countries)
        if isinstance(my_tree, Leaf):
            confirm_answer(result, answers_so_far, questions_so_far, questions_number, countries_answers, True,
                           countries)
            break

        question = my_tree.question
        key = str(question.column)
        answer_value = -1

        print(question)
        while answer_value < 0:
            answer = input()
            answer_value = match_answer(answer)

        countries_answers_question = find_value(questions_dict, int(key))
        questions_so_far.append(str(countries_answers_question))
        answers_so_far.append(float(answer_value))

        countries_probabilities = calculate_probabilities(questions_so_far, answers_so_far, countries_answers)
        result = sorted(countries_probabilities, key=lambda p: p['probability'], reverse=True)
        print("probabilities", result)

        if answer == 'yes':
            category = find_category(categories, int(key))
            countries_questions = update_questions(countries_questions, categories[category])
            deleted_questions += delete_category(countries, category, categories, t.headers)
            update_questions_in_categories(categories)
            if len(questions_so_far) > 2:
                delete_countries(countries_probabilities, countries_answers)

        elif answer == 'no' or answer == 'maybe' or answer == 'probably no' or answer == 'probably yes':
            countries_questions = update_questions(countries_questions, [int(key)])
            delete_question(countries, int(key), categories)
            delete_header(t.headers, int(key))
            update_questions_in_categories(categories)
            if len(questions_so_far) > 2:
                delete_countries(countries_probabilities, countries_answers)

        for i in question_numbers:
            questions_dict[i] = countries_questions[i]

        if check_prob(result) or len(questions_so_far) == 15:
            if confirm_answer(result, answers_so_far, questions_so_far, questions_number, countries_answers,
                              False, countries):
                break

        countries_probabilities = calculate_probabilities(questions_so_far, answers_so_far, countries_answers)
        result = sorted(countries_probabilities, key=lambda p: p['probability'], reverse=True)


if __name__ == "__main__":
    while True:
        main()
        print('Czy chcesz zaczac nowa gre?')

        while True:
            new_game = input()
            if new_game == "yes" or new_game == "no":
                break
        if new_game == 'no':
            break
