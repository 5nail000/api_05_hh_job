import requests

from common_func import calculate_avarage_salary


def predict_rub_salary(vacancy):

    all_salaries = []
    town = 113  # Moscow
    speciality = 96  # Программист, разработчик
    per_page = 100
    page = 0
    more = True

    while more:
        param = {
                'text': vacancy,
                'area': town,
                'professional_role': speciality,
                'page': page,
                'per_page': per_page,
                'describe_arguments': True,
                'clusters': True
                }

        response = requests.get('https://api.hh.ru/vacancies', params=param)
        response.raise_for_status()
        decoded_response = response.json()

        quantity = decoded_response['found']
        total_pages = int(quantity/per_page)

        for single_vacancy in decoded_response['items']:

            if not single_vacancy['salary']:
                continue

            if single_vacancy['salary']['currency'] != 'RUR':
                continue

            avarage_salary = calculate_avarage_salary(
                                            single_vacancy['salary']['from'],
                                            single_vacancy['salary']['to']
                                            )
            all_salaries.append(avarage_salary)

        if page == total_pages or page == 19:
            more = False
        page += 1

    return (all_salaries, quantity)


def get_all_predictions_hh(all_jobs):
    vacancies = {}
    for language in all_jobs:
        all_salaries, vacancies_quantity = predict_rub_salary(language)

        vacancy_solver = 0
        if all_salaries:
            vacancy_solver = sum(all_salaries)/len(all_salaries)
        vacancy_average_salary = 1000 * round(vacancy_solver/1000)
        vacancies_processed = len(all_salaries)

        vacancies[language] = {
            'Наименование': language,
            'Средняя оплата': vacancy_average_salary,
            'Всего вакансий': vacancies_quantity,
            'Кол-во обработанных': vacancies_processed
            }

    return vacancies
