#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
import argparse
import os.path


def print_help():
    """
    Функция вывода доступных пользователю команд
    """

    print("list - вывод всех добавленных записей")
    print("add - добавление новых записей")
    print("find - найти запись по фамилии")
    print("exit - завершение работы программы")


def add_worker(workers, surname, name, phone, date):
    """
    Функция добавления новой записи, возвращает запись
    """

    workers.append(
        {
            "surname": surname,
            'name': name,
            'phone': phone,
            'date': date
        }
    )

    return workers


def print_list(list):
    """
    Функция выводит на экран список всех существующих записей
    """

    for member in list:
        print(f"{member['surname']} {member['name']} | "
              f"{member['phone']} | {member['date']}")


def find_member(workers, period):
    """
    Функция для вывода на экран всех записей, чьи фамилии совпадают
    с введённой (не возвращает никаких значений)
    """

    count = 0
    members = []

    for member in workers:
        year = datetime.strptime(member['date'], "%d.%m.%Y").year
        if datetime.now().year - period >= year:
            members.append(member)
            count += 1

    if count == 0:
        print("Записи не найдены")
    else:
        return members


def save_file(filename, data):
    """
    Сохранение списка сотрудников в файл формата JSON
    """

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_file(filename):
    """
    Загрузка данных о сотрудниках из указанного JSON-файла
    """

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def parse_datetime(value):
    try:
        return datetime.strptime(value, "%d.%m.%Y")
    except ValueError:
        print("Error")


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    parser = argparse.ArgumentParser("workers")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new worker"
    )
    add.add_argument(
        "-s",
        "--surname",
        action="store",
        required=True,
        help="The worker's surname"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The worker's name"
    )
    add.add_argument(
        "-p",
        "--phone",
        action="store",
        help="The worker's phone"
    )
    add.add_argument(
        "-d",
        "--date",
        action="store",
        required=True,
        help="The date of hiring"
    )

    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all workers"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the workers"
    )
    select.add_argument(
        "-p",
        "--period",
        action="store",
        type=int,
        required=True,
        help="The required period"
    )

    args = parser.parse_args(command_line)

    is_dirty = False
    if os.path.exists(args.filename):
        workers = load_file(args.filename)
    else:
        workers = []

    if args.command == "add":
        workers = add_worker(
            workers,
            args.surname,
            args.name,
            args.phone,
            args.date
        )
        is_dirty = True

    elif args.command == "display":
        print_list(workers)

    elif args.command == "select":
        selected = find_member(workers, args.period)
        print_list(selected)

    if is_dirty:
        save_file(args.filename, workers)


if __name__ == "__main__":
    """
    Основная программа
    """
    main()
