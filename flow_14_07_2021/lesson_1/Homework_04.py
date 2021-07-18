'''4. Написать программу, которая запрашивает у пользователя строку чисел, разделённых пробелом.
При нажатии Enter должна выводиться сумма чисел. Пользователь может продолжить ввод чисел, разделённых пробелом
и снова нажать Enter. Сумма вновь введённых чисел будет добавляться к уже подсчитанной сумме.
Но если вместо числа вводится специальный символ, выполнение программы завершается.
Если специальный символ введён после нескольких чисел, то вначале нужно добавить сумму этих чисел к полученной
ранее сумме и после этого завершить программу.
"""

Домашнее задание 4.'''

def sum_int(string):
    '''Function return summa of numbers of introduced string
    and validate characters'''
    is_valid = True
    summa = 0
    for i in range(len(string)):
        try:
            string[i] = int(string[i])
            summa += string[i]
        except:
            print('non-integer introduced')
            is_valid = False
            break
    return summa, is_valid

summa = 0
is_valid = True #Triger for while loop, checking non integer input
while is_valid:
    users_input = input("Input numbers separated by Space and press Enter: ")
    input_as_list = users_input.split()
    input_result = sum_int(input_as_list)
    summa += input_result[0]
    is_valid = input_result[1]
    print(f'Summa is: {summa}')
else:
    print('The programm is finished')
