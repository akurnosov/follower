# Follower
* Аналог команды tail в Unix (с некоторыми ограничениями).
* Позволяет просмотреть конец файла с возможностью "подписаться" за обновлением.
* На производительность не влияет размерность файла, что позволяет работать с бесконечно большими файлами.

## Как использовать ##
Нужно выполнить в коммандной строке команду,
которая состоит из следующих параметров: 

1) Интерпритатор Python 3 
2) Путь к файлу follower.py
3) Путь к файлу, который нужно анализировать
4) Количество строк с конца файла или символ "f", чтобы подписаться на обновления

Пример 1:

    python3 follower.py /var/log/system.log f
    
Пример 2:

    python3 follower.py /var/log/system.log 14
    

## Особенности ##

1) Есть два режима: 
* Вывести минимум 10 строк с конца файла и следить за обновлением
* Вывести определенное количество строк с конца файла

2) Предупреждения:
* Если строк в файле меньше, чем мы хотим вывести
* Если путь к файлу это дирректория
* Если файла не существует
* Если файл нельзя прочитать
* Если в коммандной строке параметров больше, чем ожидается
