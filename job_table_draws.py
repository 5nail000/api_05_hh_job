from terminaltables import SingleTable
from vacancies_hh import get_all_predictions_hh
from vacancies_sjob import get_all_predictions_superjob


def draw_table(all_predictions, title=''):
    table_header = []
    for vacancy in all_predictions:
        for vacancy_data in all_predictions[vacancy]:
            table_header.append(vacancy_data)
        break

    table_data = [table_header]
    for vacancy in all_predictions:
        new_row = []
        for vacancy_data in all_predictions[vacancy]:
            new_row.append(all_predictions[vacancy][vacancy_data])

        table_data.append(new_row)

    table = SingleTable(table_data, title)
    print()
    print(table.table)


if __name__ == '__main__':

    languages_10top = [
        'JavaScript', 'Java', 'Python', 'Ruby', 'PHP',
        'C++', 'CSS', 'C#', 'C', 'Go'
        ]

    all_predictions = get_all_predictions_superjob(languages_10top)
    draw_table(all_predictions, ' SuperJob.ru (Moscow) ')

    all_predictions = get_all_predictions_hh(languages_10top)
    draw_table(all_predictions, ' HeadHunter.ru (Moscow) ')
