"""
Кравченко Андрій 141гр.    Варіант 4|3
Завдання:
1. Запитати у користувача код регіону
2. Отримати ЗВО з вказаного користувачем регіону
3. Зберегти всі дані у файл universities.csv у форматі csv
4. Збережіть ті ж дані у файл universities_<код регіону>.csv, наприклад universities_80.csv
5. Якщо регіон не зі списку доступних, то повідомити про це користувачеві у консолі
Завдання #1
4. Назви та EDRPOU в файл EDRPOU.csv
Завдання #2
3. З роком заснування між 1950 та 1999
Завдання 3
Ускладніть програму з другого завдання можливістю фільтрування за будь-яким з наявних значень поля
Підказка - сформуйте список всіх значень що зустрічають і дайте користувачеві обрати
"""


import requests
import csv

region_key = str(input('Введите код региона = '))

reg_int = [12, 18, 21, 23, 26, 32, 35, 44, 46, 48, 51, 53, 56, 59, 61, 63, 65, 68, 71, 73, 74, 80, 85]
reg_str = ['01', '05', '07']
val_0 = int(region_key) in reg_int
val_1 = reg_int in reg_str


if val_0 is False:
    if val_1 is False:
        print('Код региона не в списке доступных. Повторите ввод')
        exit(0)

r = requests.get('https://registry.edbo.gov.ua/api/universities/?ut=1&lc='+region_key+'&exp=json')
universities: list = r.json()


filtered_data = [{k: row[k] for k in ['university_name',
                                          'university_parent_id',
                                          'university_edrpou',
                                          'university_director_fio',
                                          'university_email',
                                          'university_phone',
                                          'post_index',
                                          'university_address',
                                          'university_financing_type_name',
                                          'registration_year'
                                          ]} for row in universities]

with open('universities_' + region_key + '.csv', mode='w', encoding='CP1251') as f:
    writer = csv.DictWriter(f, fieldnames=filtered_data[0].keys())
    writer.writeheader()
    writer.writerows(filtered_data)


filtered_data_1 = [{k: row[k] for k in ['university_name',
                                        'university_edrpou',
                                      ]} for row in universities]
with open('EDRPOU.csv', mode='w', encoding='CP1251') as f:
    writer = csv.DictWriter(f, fieldnames=filtered_data[0].keys())
    writer.writeheader()


print("\nThere are some items that can be added:\n",
      "З формою фінансування (key 1)\n",
      "З посадою керівника Ректор (key 2)\n",
      "З роком заснування між 1950 та 1999 (key 3)\n")


_choice = int(input())


if _choice == 1:
    financing_type = input("Enter financing type (Державна|Приватна|Комунальна): ")
    if financing_type not in ["Державна", "Приватна", "Комунальна"]:
        exit(0)
    filtered_data = [{k: row[k] for k in ['university_name',
                                          'university_financing_type_name']} for k in ['university_financing_type_name']
                    for row in universities
                    if row[k] == financing_type]

    with open('financing_type_' + region_key + '.csv', mode='w', encoding='CP1251') as f:
        writer = csv.DictWriter(f, fieldnames=filtered_data[0].keys())
        writer.writeheader()
        writer.writerows(filtered_data)
if _choice == 2:
    filtered_data_ = [{k: row[k] for k in ['university_name',
                                           'university_director_fio', ]} for row in universities]

    with open('rector_fio_' + region_key + '.csv', mode='w', encoding='CP1251') as f:
        writer = csv.DictWriter(f, fieldnames=filtered_data_[0].keys())
        writer.writeheader()
        writer.writerows(filtered_data_)
if _choice == 3:
    filtered_data = [
        {k: row[k] for k in ['university_name', 'university_address', 'university_email', 'registration_year']}
        for row in list(filter(lambda x: 1999 > int(x['registration_year'] or 0) > 1950, universities))]

    with open('websites+year.csv', mode='w', encoding='CP1251') as f:
        writer = csv.DictWriter(f, fieldnames=filtered_data[0].keys())
        writer.writeheader()
        writer.writerows(filtered_data)
