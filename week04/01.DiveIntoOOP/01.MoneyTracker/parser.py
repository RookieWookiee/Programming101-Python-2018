from datetime import datetime

class Parser:
    def __init__(self, fname):
        self.fname = fname

    def parse(self):
        self.data = {}
        self.order_of_insert = []

        with open(self.fname, 'r') as f:
            date = ''

            for line in f:
                line = line.strip()
                if line.startswith('===') and line.endswith('==='):
                    date = _parse_date(line)
                    self.order_of_insert.append(date)
                    self.data[date] = []
                else:
                    self.data[date].append(line.split(', '))

        return self.data


#TODO: helper.py++
def _parse_date(date):
    return datetime.strptime(date, '=== %d-%m-%Y ===')
