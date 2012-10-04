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

# A list of the names of functions to call.
# This will also determine the order of function calls.



def grab_file_data(in_file, out_good_file, out_bad_file):
    print "---------"
    print "running grab_file_data()"
    raw_input()
    with open(in_file, 'rt') as opened_file:
        read_file = csv.reader(opened_file)
        rows = []
        for row in read_file:
            rows.append(row)
        return rows, out_good_file, out_bad_file
        opened_file.close


def strip_blank_fields(rows):
    print "---------"
    print "running strip_blank_fields()"
    print "rows? %r" % bool(rows)
    raw_input()

    for row in rows:
        while "" in row:
            row.remove("")
    return rows


def strip_whitespace(rows):
    print "---------"
    print "running strip_whitespace()"
    print "rows? %r" % bool(rows)
    raw_input()
    for row in rows:
        for num, field in enumerate(row):
            row[num] = field.strip()
    return rows


def capitalize(rows):
    print "---------"
    print "running capitalize()"
    print "rows? %r" % bool(rows)
    raw_input()
    for row in rows:
        for num, field in enumerate(row):
            if "@" not in field and not field.istitle():
                row[num] = field.title()
    capitalized_list = rows
    return capitalized_list


def strip_blank_lists(rows):
    print "---------"
    print "running strip_blank_lists()"
    print "rows? %r" % bool(rows)
    raw_input()
    for row in rows:
        if row == []:
            rows.remove(row)
    return rows
    # why not this:
    # while [] in rows:
    #    rows.remove([])


def split_on_blanks(rows):
    print "---------"
    print "running split_on_blanks()"
    print "rows? %r" % bool(rows)
    raw_input()
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
    print "---------"
    print "running remove_duplicate_names()"
    print "rows? %r" % bool(rows)
    raw_input()
    for num, row in (enumerate(rows)):
        for x in xrange(len(row)):
            if row.count(row[x]) > 1:
                row.pop(x)
                break
    return rows


def remove_bad_rows(rows):
    print "---------"
    print "running remove_bad_rows()"
    print "rows? %r" % bool(rows)
    raw_input()
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

    return rows

def columnize(rows):
    print "---------"
    print "running columize()"
    print "rows? %r" % bool(rows)
    raw_input()
    titles = [
    'Mr', 'Mrs', 'Mr.', 'Mrs.', 'mr',
    'mrs', 'mr.', 'mrs.', 'Miss', 'miss'
    ]

    for row in rows:
        print "-----------"
        print "top of for loop"
        print "row = %r " % row
        raw_input()
        if set(row).isdisjoint(set(titles)):
            row.insert(0, '')

    return rows


def write_csv(rows, filename):
    print "---------"
    print "running write_csv()"
    print "rows? %r" % bool(rows)
    raw_input()
    f = open(filename, 'wt')
    try:
        writer = csv.writer(f)
        writer.writerow(('Title', 'First', 'Middle', 'Last', 'Email'))
        for row in rows:
            writer.writerow(row)
    finally:
        f.close()


# Iterate through the list of functions and execute them in order of the list.
if __name__ == "__main__":
    global functions
    global manual_repair
    functions = [
        'strip_blank_fields',
        'strip_whitespace',
        'capitalize',
        'strip_blank_lists',
        'split_on_blanks',
        'remove_duplicate_names',
        'remove_bad_rows',
        'columnize',
        ]

# Strip out all functions that were passed in as argunments (from command line)
# as false.

    manual_repair = []
    rows, good_file, file_to_repair = grab_file_data(sys.argv[1], sys.argv[2], sys.argv[3])
    for function in functions:
        next_operation = globals()[function]
        rows = next_operation(rows)
    write_csv(rows, good_file)
    if manual_repair:
        write_csv(manual_repair, file_to_repair)

