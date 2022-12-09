import requests


def send_request(url, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response


def predict_rub_salary(vacancy):

    salary_all = []
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
        response = send_request('https://api.hh.ru/vacancies', param).json()
        quantity = response['found']
        total_pages = int(quantity/per_page)

        for single_vacancy in response['items']:

            if single_vacancy['salary'] is None:
                continue

            if single_vacancy['salary']['currency'] != 'RUR':
                continue

            if single_vacancy['salary']['from'] is None:
                salary_all.append(single_vacancy['salary']['to'] * 0.8)

            if single_vacancy['salary']['to'] is None:
                salary_all.append(single_vacancy['salary']['from'] * 1.2)

            if single_vacancy['salary']['to'] and single_vacancy['salary']['from']:
                salary_all.append(
                    (single_vacancy['salary']['to'] + single_vacancy['salary']['from'])/2
                    )
        if page == total_pages or page == 19:
            more = False
        page += 1
        True
    return [salary_all, quantity]


def get_all_predictions_hh(all_jobs):
    vacancies = {}
    for language in all_jobs:
        [all_salaries, vacancies_quantity] = predict_rub_salary(language)

        vacancy_solver = sum(all_salaries)/len(all_salaries)
        vacancy_average_salary = 1000 * round(vacancy_solver/1000)
        vacancies_processed = len(all_salaries)
        vacancy_data = {
            language: {
                'Наименование': language,
                'Средняя оплата': vacancy_average_salary,
                'Всего вакансий': vacancies_quantity,
                'Кол-во обработанных': vacancies_processed
                }
            }
        vacancies.update(vacancy_data)

    return vacancies
