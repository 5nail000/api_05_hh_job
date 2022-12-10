import os

from dotenv import load_dotenv
from terminaltables import SingleTable

from vacancies_hh import get_all_predictions_hh
from vacancies_sjob import get_all_predictions_superjob


def draw_table(all_predictions, title=''):

    table_header = []
    for vacancy_name, vacancy_params in all_predictions.items():
        for param_key, param_value in vacancy_params.items():
            table_header.append(param_key)
        break

    table_rows = [table_header]
    for vacancy_name, vacancy_params in all_predictions.items():
        new_row = []
        for param_key, param_value in vacancy_params.items():
            new_row.append(param_value)

        table_rows.append(new_row)

    return SingleTable(table_rows, title).table


if __name__ == '__main__':

    load_dotenv()
    token_sjob = os.getenv('SUPERJOB_SECRET_KEY')

    languages_10top = [
        'JavaScript', 'Java', 'Python', 'Ruby', 'PHP',
        'C++', 'CSS', 'C#', 'C', 'Go'
        ]

    all_predictions = get_all_predictions_superjob(token_sjob, languages_10top)
    print(draw_table(all_predictions, ' SuperJob.ru (Moscow) '))

    all_predictions = get_all_predictions_hh(languages_10top)
    print(draw_table(all_predictions, ' HeadHunter.ru (Moscow) '))
