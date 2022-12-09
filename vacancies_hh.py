import requests


def send_request(url, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response


def get_vacancy_quantity(vacancy, area=113, professional_role=96):
    param = {
        'text': vacancy,
        'area': area,
        'professional_role': professional_role,
        'per_page': 100,
        'clusters': True,
        'describe_arguments': True
        }
    response = send_request('https://api.hh.ru/vacancies', param).json()
    return (response['found'])


def predict_rub_salary(vacancy, quantity):

    if quantity > 2000:
        quantity = 2000

    salary_all = []
    town = 113  # Moscow
    speciality = 96  # Программист, разработчик
    pages = int(quantity/100)
    for page in range(pages):
        param = {
            'text': vacancy,
            'area': town,
            'professional_role': speciality,
            'page': page,
            'per_page': 100,
            'describe_arguments': True,
            'clusters': True
            }
        response = send_request('https://api.hh.ru/vacancies', param).json()
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
    return salary_all


def get_all_predictions_hh(all_jobs):
    vacancies = {}
    for language in all_jobs:
        vacancies_quantity = get_vacancy_quantity(language)
        vacancy_all_salaries = predict_rub_salary(language, vacancies_quantity)

        vacancy_solver = sum(vacancy_all_salaries)/len(vacancy_all_salaries)
        vacancy_average_salary = 1000 * round(vacancy_solver/1000)
        vacancies_processed = len(vacancy_all_salaries)
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
