from terminaltables import SingleTable
from vacancies_hh import get_all_predictions_hh
from vacancies_sjob import get_all_predictions_superjob


def draw_table(all_predictions, title=''):
    table_header = []
    for x_item in all_predictions:
        for y_item in all_predictions[x_item]:
            table_header.append(y_item)
        break

    table_data = [table_header]
    for x_item in all_predictions:
        new_row = []
        for y_item in all_predictions[x_item]:
            new_row.append(all_predictions[x_item][y_item])

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
