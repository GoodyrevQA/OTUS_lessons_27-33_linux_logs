import os
import sys
import json
import re
from collections import defaultdict


def parse_log_line(line: str):
    """функция парсит полученную строку и возвращает словарь"""
    line = line.strip()

    m = re.search(
        r"(?P<ip>^.+) - .+ (?P<date>\[.+\]) \"(?P<method>[A-Z]{3,}) .*\"(?P<url>.+?)\" \".*\" (?P<duration>\d+)",
        line,
    )
    if m:
        log_line = {
            "ip": m.group("ip"),
            "date": m.group("date"),
            "method": m.group("method"),
            "url": m.group("url"),
            "duration": int(m.group("duration")),
        }
        return log_line
    return None


def parse_log_file(log_file):
    """функция парсит log-файл и возвращает словарь"""
    flag = True
    top_longest = []
    total_requests = 0
    http_methods = defaultdict(int)
    ips = defaultdict(int)

    with open(log_file) as f:
        for line in f:
            log_data = parse_log_line(line)
            if log_data:
                total_requests += 1
                http_methods[log_data["method"]] += 1
                ips[log_data["ip"]] += 1

            if len(top_longest) < 3:
                top_longest.append(log_data)

            else:
                # если набор менялся, ищем какой из логов теперь занимает 3-е место по длительности
                if flag:
                    min_of_tops = min(top_longest, key=lambda x: x["duration"])

                if min_of_tops["duration"] < log_data["duration"]:
                    top_longest.remove(min_of_tops)
                    top_longest.append(log_data)
                    flag = True
                else:
                    flag = False

    top_3_ips = dict(sorted(ips.items(), key=lambda x: x[1], reverse=True)[:3])
    dct = {
        "top_ips": top_3_ips,
        "top_longest": top_longest,
        "total_stat": dict(http_methods),
        "total_requests": total_requests,
    }
    return dct


def parse_logs_in_directory(directory_path):
    """функция ищет в папке log-файлы, парсит их и возвращает словарь"""
    logs_data = {}
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".log"):
                file_path = os.path.join(root, file)
                logs_data[file] = parse_log_file(file_path)
    return logs_data


def main(input_path):
    """функция выводит в терминал и записывает в json-файлы результаты парсинга log-файлов"""
    if os.path.isdir(input_path):
        logs_data = parse_logs_in_directory(input_path)
    elif os.path.isfile(input_path):
        logs_data = {os.path.basename(input_path): parse_log_file(input_path)}
    else:
        print("Error: Invalid input path.")
        return

    # Вывод результатов в терминал с отступами
    for log_file, log_data in logs_data.items():
        print(json.dumps(log_data, indent=4))

    # Запись результатов в файлы JSON
    for log_file, log_data in logs_data.items():
        log_file_name = os.path.splitext(os.path.basename(log_file))[0]
        output_file = f"logs_data_{log_file_name}.json"
        with open(output_file, "w") as json_file:
            json.dump(log_data, json_file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gimme_logs.py <directory_path_or_file_path>")
    else:
        input_path = sys.argv[1]
        main(input_path)
