#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--filename', '-f', help='Имя файла')
def display(filename):
    """
    Функция (click) вывода списка существующих записей из указанного файла
    """

    try:
        workers = load_file(filename)
        print_list(workers)
        print()
    except FileNotFoundError:
        print("Ошибка в имени файла\n")


@cli.command()
@click.option('--filename', '-f', help='Имя файла')
@click.option("--surname", "-s", help="Фамилия работника")
@click.option("--name", "-n", help="Имя работника")
@click.option("--phone", "-p", help="Номер телефона работника")
@click.option("--date", "-d", help="Дата приёма работника")
def add(filename, surname, name, phone, date):
    """
    Функция (click) добавления в указанный файл новой записи
    """

    workers = load_file(filename)
    workers = add_worker(workers, surname, name, phone, date)
    save_file(filename, workers)


@cli.command()
@click.option('--filename', '-f', help='Имя файла-источника')
@click.option('--period', '-p', type=int, help='Искомый период (лет)')
def select(filename, period):
    """
    Функция (click) выбора записей из указанного файла по периоду
    """

    try:
        workers = find_member(load_file(filename), period)
        print_list(workers)
        print()
    except TypeError:
        print("Записи не найдены\n")


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

    if count != 0:
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


if __name__ == "__main__":
    """
    Основная программа
    """
    cli()
