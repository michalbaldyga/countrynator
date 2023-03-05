import csv


def is_numeric(value):
    """Test if a value is numeric."""
    return isinstance(value, int) or isinstance(value, float)


def country_names(rows):
    """Makes the list of the countries names from the data."""
    country_name = []  # an empty list for the countries names
    for row in rows:
        # in our dataset format, the name of the country is always the last column
        country_name.append(row[-1])
    return country_name


def load_headers():
    headers = []
    list_of_column_names = []
    rows_to_skip = 2
    with open('baza.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            list_of_column_names.append(row)
            rows_to_skip -= 1
            if rows_to_skip == 0:
                break

    for i in range(len(list_of_column_names[0]) - 1):
        headers.append(list_of_column_names[0][i] + " == " + list_of_column_names[1][i])

    return headers


def create_categories():
    """Loading column names from .csv file."""
    categories = {}
    categories_tmp = {}
    list_of_column_names = []
    with open('baza.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            list_of_column_names.append(row)
            break

    col = 0
    list_of_column_names[0].pop()
    for column in list_of_column_names[0]:
        categories_tmp[column] = col
        categories[column] = []
        col += 1

    starting_value = 0
    for category, value in categories_tmp.items():
        for i in range(starting_value, value + 1):
            categories[category].append(i)
        starting_value = value + 1

    return categories


def create_possible_questions():
    """Creating questions based on column names."""
    headers = load_headers()
    questions = {}
    key = 0
    for header in headers:
        questions[str(key)] = "Czy " + header + "?"
        key += 1
    return questions


def load_data():
    """Loading data from .csv file."""
    data = []
    rows_to_skip = 2
    with open('baza.csv') as file_obj:
        reader_obj = csv.reader(file_obj)
        for row in reader_obj:
            if rows_to_skip > 0:
                rows_to_skip -= 1
                continue
            data.append(row)

    """Transforming our dataset."""
    countries = []
    for i in range(len(data)):
        features_no = len(data[i]) - 1
        country = {'name': data[i][features_no]}
        answers = {}
        key = 0
        for j in range(features_no):
            answers[str(key)] = float(data[i][j])
            key += 1
        country['answers'] = answers
        countries.append(country)

    return countries, data


def find_category(categories, col_num):
    """Searching for a category based on a column number."""
    for category, columns in categories.items():
        for column in columns:
            if column == col_num:
                return category


def delete_question_from_category(categories, q):
    for category, questions in categories.items():
        for question in questions:
            if question == q:
                categories[category].remove(question)


def update_questions_in_categories(categories):
    curr_col = 0
    for category, questions in categories.items():
        for i in range(len(questions)):
            categories[category][i] = curr_col
            curr_col += 1


def delete_category(countries, category, categories, headers):
    deleted_questions = 0
    starting_col = categories[category][0]
    for _ in range(len(categories[category])):
        delete_question(countries, starting_col, categories)
        delete_header(headers, starting_col)
        deleted_questions += 1
    categories.pop(category)
    return deleted_questions


def delete_question(countries, col_num, categories):
    for i in range(len(countries)):
        countries[i].pop(col_num)
    delete_question_from_category(categories, col_num)


def delete_header(headers, col):
    headers.pop(col)


def update_questions(questions, categories):
    new_questions = []
    curr_value = 0
    for i in questions:
        if i == -1:
            new_questions.append(-1)
            continue
        elif i < categories[0]:
            new_questions.append(i)
            curr_value += 1
        elif i in categories:
            new_questions.append(-1)
        else:
            new_questions.append(curr_value)
            curr_value += 1
    return new_questions


def find_value(dictionary, k):
    for key, value in dictionary.items():
        if k == value:
            return key


def check_prob(probabilities):
    highest_prob = probabilities[0]['probability']
    sec_highest_prob = 1.0

    if len(probabilities) > 1:
        sec_highest_prob = probabilities[1]['probability']
    if highest_prob >= 0.6 or highest_prob - sec_highest_prob >= 0.4:
        return 1
    else:
        return 0


def match_answer(answer):
    match answer:
        case 'yes':
            return 1
        case 'probably yes':
            return 0.75
        case 'maybe':
            return 0.5
        case 'probably no':
            return 0.25
        case 'no':
            return 0
        case _:
            return -1


def delete_countries(probabilities, countries):
    min_value = 0.0001

    for probability in probabilities:
        if probability['probability'] < min_value:
            delete_country_from_list(countries, probability['name'])


def delete_country_from_list(countries, name):
    for country in countries:
        if country['name'] == name:
            countries.remove(country)
            break


def confirm_answer(result, answers_so_far, questions_so_far, questions_number, countries, no_questions,
                   countries_in_db):
    i = 0
    while True:
        print('Czy myslales o tym kraju?')
        print(result[i]['name'])  # country that has best probabilities
        max_probability = result[0]['probability']

        while True:
            confirmation = input()
            if confirmation == 'yes' or confirmation == 'no':
                break

        if confirmation == 'yes':
            update_country(countries, answers_so_far, questions_so_far, result[i]['name'])
            return True
        else:
            delete_country_from_list(countries, result[i]['name'])
            if len(countries) == 0:
                add_new_country(answers_so_far, questions_so_far, questions_number, countries_in_db)
                return True

        i += 1
        if len(result) > 1:
            if max_probability - result[1]['probability'] > 0.1:
                if no_questions:
                    add_new_country(answers_so_far, questions_so_far, questions_number, countries_in_db)
                    return True
                else:
                    return False

        if i == 2 and not no_questions:
            return False


def add_new_country(user_answers, questions, questions_number, countries):
    print('Podaj nazwe kraju, ktory wybrales')
    country_name = input()

    if not is_country_in_base(country_name, countries):
        country_answers = [0.5 for _ in range(questions_number)]
        iter_max = len(user_answers)

        for i in range(iter_max):
            question_no = int(questions[i])
            country_answers[question_no] = user_answers[i]

        with open("baza.csv", "a") as file:
            for answer in country_answers:
                file.write(str(answer) + ",")
            file.write(country_name)
            file.write("\n")


def is_country_in_base(name, country_list):
    for country in country_list:
        if country[0] == name:
            return True

    return False


def update_country(countries_answers, user_answers, questions, country_name):
    for country in countries_answers:
        if country['name'] == country_name:
            country_answers = country['answers']
            break

    new_country_probability = []
    for country in countries_answers:
        if country['name'] == country_name:
            answers = country['answers']
            for key, value in answers.items():
                new_country_probability.append(value)

    i = 0
    for answer in user_answers:
        new_country_probability[int(questions[i])] = new_answer_value(country_answers[questions[i]], answer)
        i += 1

    text = ""
    with open('baza.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\n')

        for line in csv_reader:
            if country_name in line[0]:
                replacement = create_replacement(new_country_probability, country_name)
                text += replacement
            else:
                text += line[0]
            text += "\n"

    with open('baza.csv', 'w') as csv_file_writer:
        csv_file_writer.write(text)


def new_answer_value(last_value, new_value):
    if last_value == 0 or last_value == 1:
        return last_value
    else:
        return new_value


def create_replacement(probabilities, name):
    replacement = ""
    for probability in probabilities:
        replacement += str(probability)
        replacement += ","

    replacement += name
    return replacement
