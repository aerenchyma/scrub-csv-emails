# TODO: Change the strip_blank_fields function to use a with statement
import csv
import sys

# This script will expext three arguments:
# 1. File with data to be scrubbed
# 2. File name to output clean data
# 3. File name to output data that's needs manual review

# argv style:
# opened_file = open(argv[1], 'rt)'
# opened_file

manual_repair = []


def strip_blank_fields(file):
    try:
        opened_file = open(file, 'rt')
        read_file = csv.reader(opened_file)
        blankless = []
        for row in read_file:
            while "" in row:
                row.remove("")
            blankless.append(row)
    finally:
        opened_file.close()
    return blankless


def strip_whitespace(rows):
    for row in rows:
        for num, field in enumerate(row):
            row[num] = field.strip()
    return rows


def capitalize(rows):
    for row in rows:
        for num, field in enumerate(row):
            if "@" not in field and not field.istitle():
                row[num] = field.title()
    capitalized_list = rows
    return capitalized_list


def strip_blank_lists(rows):
    for row in rows:
        if row == []:
            rows.remove(row)
    return rows
    # why not this:
    # while [] in rows:
    #    rows.remove([])


def split_on_blanks(rows):
    for row in rows:
        for num, field in enumerate(row):
            if ' ' in field:
                x = field.split(' ')
                row.pop(num)
                for i in x:
                    row.append(i)

    for row in rows:
        for num, field in enumerate(row):
            if "@" in field:
                x = row.pop(num)
                row.append(x)

    return rows


def remove_duplicate_names(rows):
    for num, row in (enumerate(rows)):
        for x in xrange(len(row)):
            if row.count(row[x]) > 1:
                row.pop(x)
                break
    return rows


def remove_bad_rows(rows):
    global manual_repair

  # Remove all rows that don't have at least three slots filled
    for num, row in enumerate(rows):
        if len(row) < 3:
            x = rows.pop(num)
            manual_repair.append(x)

    # Remove all rows that don't have an email address.
    for num, row in enumerate(rows):
        bad = True
        for field in row:
            if '@' in field:
                bad = False
                break
        if bad == True:
            x = rows.pop(num)
            manual_repair.append(x)

    return manual_repair


def columnize(rows):
    titles = [
    'Mr', 'Mrs', 'Mr.', 'Mrs.', 'mr',
    'mrs', 'mr.', 'mrs.', 'Miss', 'miss'
    ]

    for row in rows:
        if set(row).isdisjoint(set(titles)):
            row.insert(0, '')

    return rows


def write_csv(rows, filename):
    f = open(filename, 'wt')
    try:
        writer = csv.writer(f)
        writer.writerow(('Title', 'First', 'Middle', 'Last', 'Email'))
        for row in rows:
            writer.writerow(row)
    finally:
        f.close()

    print open(filename, 'rt').read()


