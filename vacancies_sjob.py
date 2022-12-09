import os
import requests

from dotenv import load_dotenv


load_dotenv()
token = os.getenv('SUPERJOB_SECRET_KEY')


def get_superJob_page(vacancy, page=0):

    global token

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
    response = response.json()

    all_vacancies = response['objects']
    more = response['more']
    total = response['total']

    return [all_vacancies, more, total]


def predict_rub_salary_for_superJob(all_vacancies):

    payments = []

    for item in all_vacancies:
        currency = item['currency']  # rub
        payment_from = item['payment_from']
        payment_to = item['payment_to']

        if currency != 'rub':
            continue

        if payment_to == 0:
            payment = payment_from * 1.2
            payment_to = False

        if payment_from == 0:
            payment = payment_to * 0.8
            payment_from = False

        if payment_to and payment_from:
            payment = (payment_to + payment_from) / 2

        payments.append(payment)

    return payments


def get_all_predictions_superjob(all_jobs):
    all_predictions = {}
    for lang in all_jobs:
        page = 0
        total = 0
        more = True
        all_vacancies = []

        while more:
            get_page = get_superJob_page(lang, page)
            [all_vacancies.append(item) for item in get_page[0]]
            more = get_page[1]
            total += get_page[2]

        payments = predict_rub_salary_for_superJob(all_vacancies)

        if len(payments) < 1:
            continue

        all_predictions.update({lang: {
            'Наименование': lang,
            'Средняя оплата': int(sum(payments)/len(payments)),
            'Всего вакансий': total,
            'Кол-во обработанных': len(payments)
            }})

    return all_predictions
