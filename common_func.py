
def calculate_avarage_salary(salary_from, salary_to):

    if not salary_from:
        avarage_salary = salary_to * 0.8

    if not salary_to:
        avarage_salary = salary_from * 1.2

    if salary_to and salary_from:
        avarage_salary = (salary_to + salary_from)/2

    return avarage_salary
