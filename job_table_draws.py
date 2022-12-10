import os

from dotenv import load_dotenv
from terminaltables import SingleTable
from vacancies_hh import get_all_predictions_hh
from vacancies_sjob import get_all_predictions_superjob


def draw_table(all_predictions, title=''):

    table_header = []
    for vacancy_name, vacancy_data in all_predictions.items():
        for data_key, data_value in vacancy_data.items():
            table_header.append(data_key)
        break

    table_rows = [table_header]
    for vacancy_name, vacancy_data in all_predictions.items():
        new_row = []
        for data_key, data_value in vacancy_data.items():
            new_row.append(data_value)

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
