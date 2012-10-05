import csv
import sys

# This script will expext three arguments:
# 1. File with data to be scrubbed
# 2. File name to output clean data
# 3. File name to output data that's needs manual review

class CleanCsv(object):
    def __init__(self, args):
        self.in_file = args[1]  # Storing original (necc?)
        self.clean_out_file = args[2]
        self.dirty_out_file = args[3]
        self.flags = [x for x in args[4:] if sys.argv != ""]
        # Bug?  sys.argv will never be blank----------> ^^^
        self.manual_repair = []
        self.rows = []
        self.functions = [
            'strip_blank_fields',
            'strip_whitespace',
            'capitalize',
            'strip_blank_lists',
            'split_on_blanks',
            'remove_duplicate_names',
            'remove_bad_rows',
            'columnize',
            ]

    def do_scrub(self):
            self.fxns = [x for x in self.functions if x not in self.flags]
            self.grab_file_data(self.in_file)
            for fx in self.fxns:
                next_operation = getattr(self, fx)
                next_operation()
            if self.manual_repair:
                self.write_csv(self.manual_repair, self.dirty_out_file)
            self.write_csv(self.rows, self.clean_out_file)

    def grab_file_data(self, filename):
        with open(filename, 'rt') as opened_file:
            read_file = csv.reader(opened_file)
            for row in read_file:
                self.rows.append(row)
            opened_file.close

    def strip_blank_fields(self):
        for row in self.rows:
            while "" in row:
                row.remove("")

    def strip_whitespace(self):
        for row in self.rows:
            for num, field in enumerate(row):
                row[num] = field.strip()

    def capitalize(self):
        for row in self.rows:
            for num, field in enumerate(row):
                if "@" not in field and not field.istitle():
                    row[num] = field.title()

    def strip_blank_lists(self):
        while [] in self.rows:
            self.rows.remove([])

    def split_on_blanks(self):
        for row in self.rows:
            for num, field in enumerate(row):
                if ' ' in field:
                    x = field.split(' ')
                    row.pop(num)
                    for i in x:
                        row.append(i)

        for row in self.rows:
            for num, field in enumerate(row):
                if "@" in field:
                    x = row.pop(num)
                    row.append(x)

    def remove_duplicate_names(self):
        for num, row in (enumerate(self.rows)):
            for x in xrange(len(row)):
                if row.count(row[x]) > 1:
                    row.pop(x)
                    break

    def remove_bad_rows(self):
      # Remove all rows that don't have at least three slots filled
        for num, row in enumerate(self.rows):
            if len(row) < 3:
                x = self.rows.pop(num)
                self.manual_repair.append(x)

        # Remove all self.rows that don't have an email address.
        for num, row in enumerate(self.rows):
            bad = True
            for field in row:
                if '@' in field:
                    bad = False
                    break
            if bad == True:
                x = self.rows.pop(num)
                self.manual_repair.append(x)

    def columnize(self):
        titles = [
        'Mr', 'Mrs', 'Mr.', 'Mrs.', 'mr',
        'mrs', 'mr.', 'mrs.', 'Miss', 'miss'
        ]

        for row in self.rows:
            if set(row).isdisjoint(set(titles)):
                row.insert(0, '')

    def write_csv(self, rows, name_to_write):
        f = open(name_to_write, 'wt')
        try:
            writer = csv.writer(f)
            writer.writerow(('Title', 'First', 'Middle', 'Last', 'Email'))
            for row in rows:
                writer.writerow(row)
        finally:
            f.close()

if __name__ == "__main__":
    x = CleanCsv(sys.argv)
    x.do_scrub()
