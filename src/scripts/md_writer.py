#
# The dirties implementation of a md-table writer.
#
# This avoids the requirement of external python modules.


class MyMarkdownTableWriter:
    def __init__(self):
        self.status_header = "" # "# Gsymblib symbols list, updated "+datetime.date.today().strftime("%B %d, %Y")+"\n"
        self.table_name = None
        self.headers = None #
        self.value_matrix = None
        self.buffer = ""

    def write_table(self):
        buffer = ""
        buffer = buffer + self.status_header + "\n"
        buffer = buffer + '|'.join(self.headers) + "\n"
        buffer = buffer + '---|' * len(self.headers) + "\n"
        for r in self.value_matrix:
            buffer = buffer + '|'.join(r) + "\n"
        self.buffer = buffer
            
    def dumps(self):
        return self.buffer
