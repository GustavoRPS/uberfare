"""Contains classes to handle dumping of data to various storage mediums."""

from csv import DictWriter, QUOTE_NONNUMERIC
from datetime import datetime

ESTIMATE_FIELDS = ['localized_display_name', 'distance', 'display_name',
                   'product_id', 'high_estimate', 'low_estimate', 'duration',
                   'estimate', 'currency_code', 'timestamp']


class CsvDumper:
    """This class provides convenience to CSV dumping via Context Manager."""

    def __init__(self, filename, fieldnames):

        #: filename for the output file where the data will be dumped
        self.filename = filename

        #: list of fieldnames that the CSV file will follow
        self.fieldnames = fieldnames

        #: file handle for writing to the output
        self.open_file = open(self.filename, 'a')

        #: :class:`DictWriter <DictWriter>` to handle writing dicts
        self.dict_writer = DictWriter(self.open_file, self.fieldnames,
                                      dialect='unix', quoting=QUOTE_NONNUMERIC)

    def __enter__(self):
        self._write_csv_headers()
        return self

    def __exit__(self, *args):
        self.open_file.close()

    def _write_csv_headers(self):
        """Writes the CSV data headers into the file if it's still empty."""

        if self.open_file.tell() == 0:
            self.dict_writer.writeheader()

    def dump(self, list_of_dicts):
        """Dumps the list of dicts into the CSV file for this instance.

        :param list_of_dicts: As it says.
        """

        if len(list_of_dicts) == 0:
            return

        self.dict_writer.writerows(list_of_dicts)

        print("{} | Data collected: {}".format(datetime.now().isoformat(),
              self.filename))