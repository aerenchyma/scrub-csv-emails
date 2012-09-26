import csv
import sys
import pprint

# This script will expext two arguments:
# 1. File with data to be scrubbed
# 2. File name to output

# argv style:
# opened_file = open(argv[1], 'rt)'
# opened_file

pp = pprint.PrettyPrinter(depth=4)


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


def capitalize(lists):
    for list in lists:
        for num, field in enumerate(list):
            if "@" not in field and field != field.title():
                list[num] = field.title()
    capitalized_list = lists
    return capitalized_list


def strip_blank_lists(lists):
    for list in lists:
        if list == []:
            lists.remove(list)
    return lists


def test_email_integrity(lists):
    """Test if there is an email address
    present in the row(list).  Takes a list
    and returns a tuple: 0) len(bad_list)
    1) bad_list 2) list.  Does not remove bad data."""
    bad_list = []

    for list in lists:
        bad = True
        for field in list:
            if '@' in field:
                bad = False
        if bad == True:
            bad_list.append(list)
    len_bad_list = len(bad_list)
    return len_bad_list, bad_list, lists


def remove_bad_lists(bad_list):  # Interactively later
    pass
