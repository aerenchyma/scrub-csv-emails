import csv
import sys
import pprint

# This script will expext three arguments:
# 1. File with data to be scrubbed
# 2. File name to output clean data
# 3. File name to output data that's needs manual review

# argv style:
# opened_file = open(argv[1], 'rt)'
# opened_file

pp = pprint.PrettyPrinter(depth=4)
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


# Option1: Remove original, then extend, and later move email to last
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


def find_duplicate_names(rows):
    # grab a row
    # grab the first item in the row, and then check all the other items against it
    # if any of them match, figure out which position they are matching, and determine through that if it
    # is the first name or last name to delete
    for num, row in (enumerate(rows)):
        for x in xrange(len(row)):
            if row.count(row[x]) > 1:
                row.pop(x)
                break
    return rows


# If there is a title, use that instead of adding a blank
def remove_titles(rows):
    """If a row has Mr. or Mrs. in it,
    remove that title."""
    titles = ['Mr', 'Mrs', 'Mr.', 'Mrs.', 'mr', 'mrs', 'mr.', 'mrs.', 'Miss', 'miss']

    for row in rows:
        for num, field in enumerate(row):
            if field in titles:
                row[num].remove()
    return rows


def test_for_email(rows):
    """Test if there is an email address
    present in the row(list).  Takes a list
    and returns a tuple: 0) len(manual_repair)
    1) manual_repair 2) rows.  Does not remove bad data."""
    global manual_repair

    for row in rows:
        bad = True
        for field in row:
            if '@' in field:
                bad = False
        if bad == True:
            manual_repair.append(row)
    len_bad_list = len(manual_repair)
    return len_bad_list, manual_repair, rows


def remove_bad_lists(manual_repair):  # Interactively later
    pass
