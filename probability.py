import numpy as np


def calculate_country_probability(country, questions_so_far, answers_so_far, countries):
    # Prior
    p_country = 1 / len(countries)

    # Likelihood
    p_answers_given_country = 1
    p_answers_given_not_country = 1
    for question, answer in zip(questions_so_far, answers_so_far):
        p_answers_given_country *= max(
            1 - abs(answer - country_answer(country, question)), 0.01)

        p_answer_not_country = np.mean([1 - abs(answer - country_answer(not_country, question))
                                        for not_country in countries
                                        if not_country['name'] != country['name']])
        p_answers_given_not_country *= max(p_answer_not_country, 0.01)

    # Evidence
    p_answers = p_country * p_answers_given_country + (1 - p_country) * p_answers_given_not_country

    # Bayes Theorem
    p_country_given_answers = (p_answers_given_country * p_country) / p_answers

    return p_country_given_answers


def country_answer(country, question):
    if question in country['answers']:
        return country['answers'][question]
    return 0.5


def calculate_probabilities(questions_so_far, answers_so_far, countries):
    probabilities = []
    for country in countries:
        probabilities.append({
            'name': country['name'],
            'probability': calculate_country_probability(country, questions_so_far, answers_so_far, countries)
        })

    return probabilities
