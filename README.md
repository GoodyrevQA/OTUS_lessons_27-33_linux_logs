# OTUS_lessons_27-33_linux_logs

[![Header](https://github.com/GoodyrevQA/OTUS_auto_web_QA_2024/blob/main/assets/OTUS.jpg)](https://github.com/GoodyrevQA/OTUS_auto_web_QA_2024)

### Languages and Tools used:
[![Python](https://img.shields.io/badge/-Python-24292f??style=for-the-badge&logo=Python&logoColor=47c5fb)](https://github.com/GoodyrevQA)
[![Git](https://img.shields.io/badge/-Git-24292f??style=for-the-badge&logo=Git&logoColor=f43010)](https://github.com/GoodyrevQA)

задание - https://github.com/OtusTeam/QA-Python/blob/master/log/hw.md

Код анализирует файлы логов веб-сервера

Функция parse_log_line(line) принимает строку из log-файла, парсит ее с помощью regexp и возвращает словарь вида:
{
    "ip": str,
    "date": str,
    "method": str,
    "url": str,
    "duration": str
}

Основная функция этого кода - parse_log_file(log_file).
Эта функция принимает на вход файл логов, вызывает функцию parse_log_line(line), собирает и возвращает словарь, содержащий:
- топ 3 IP адресов, с которых было сделано наибольшее количество запросов,
- топ 3 самых долгих запросов
- количество запросов по HTTP-методам
- общее количество запросов
{
  "top_ips": {
    "1.1.1.1": 4,
    "2.2.2.2": 3,
    "3.3.3.3": 2
  },
  "top_longest": [
    {
      "ip": "1.1.1.1",
      "date": "[06/Jan/2016:12:00:02 +0100]",
      "method": "GET",
      "url": "http://www.test.com/index.php",
      "duration": 5000
    },
    {
      "ip": "2.2.2.2",
      "date": "[06/Jan/2016:18:47:57 +0100]",
      "method": "GET",
      "url": "http://www.test2.com/index.php?view=category",
      "duration": 4999
    },
    {
      "ip": "3.3.3.3",
      "date": "[23/Dec/2015:07:27:57 +0100]",
      "method": "POST",
      "url": "-",
      "duration": 4998
    }
  ],
  "total_stat": {
    "GET": 4,
    "POST": 2,
    "HEAD": 1,
    "PUT": 1,
    "OPTIONS": 1,
    "DELETE": 1
  },
  "total_requests": 10
}

Функция parse_logs_in_directory(directory_path) вызывается если в качестве аргумента был передан путь до папки.
Она ищет в папке log-файлы, вызывает для них функцию parse_log_file(log_file) и возвращает словарь вида:
{
    "имя файла": parse_log_file(file_path)
}

Функция main(input_path) определяет по типу, путь до файла или до папки был передан в качестве аргумента
и вызывает соответствующую функцию: parse_log_file(log_file) или parse_logs_in_directory(directory_path).
Результат работы выводится в терминал и сохраняется в файл(ы) вида logs_data_{log_file_name}.json

Пример запуска:
python gimme_logs.py <directory_path_or_file_path>