import requests

from common_func import calculate_avarage_salary


def get_superJob_page(token, vacancy, page=0):

    category = 48  # Разработка, программирование
    town = 4  # Moscow

    host = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': token}
    params = {
        'keyword': vacancy,
        'catalogues': category,
        't': town,
        'count': 100,
        'page': page
        }

    response = requests.get(host, headers=headers, params=params)
    response.raise_for_status()
    decoded_response = response.json()

    all_vacancies = decoded_response['objects']
    more = decoded_response['more']
    total = decoded_response['total']

    return (all_vacancies, more, total)


def predict_rub_salary_for_superJob(all_vacancies):

    payments = []
    processing_filter = 100

    for single_vacancy in all_vacancies:
        currency = single_vacancy['currency']  # rub
        payment_from = single_vacancy['payment_from']
        payment_to = single_vacancy['payment_to']

        if currency != 'rub':
            continue

        payment = calculate_avarage_salary(payment_from, payment_to)

        if payment > processing_filter:
            payments.append(payment)

    return payments


def get_all_predictions_superjob(token, all_jobs):
    all_predictions = {}
    for lang in all_jobs:
        page = 0
        total = 0
        avarage_salary = '- данных нет -'
        more = True
        all_vacancies = []

        while more:
            page_vacancies, more, page_total = get_superJob_page(token, lang, page)
            all_vacancies.extend(page_vacancies)
            total += page_total

        payments = predict_rub_salary_for_superJob(all_vacancies)

        if payments:
            avarage_salary = int(sum(payments)/len(payments))

        all_predictions[lang] = {
            'Наименование': lang,
            'Средняя оплата': avarage_salary,
            'Всего вакансий': total,
            'Кол-во обработанных': len(payments)
            }

    return all_predictions
