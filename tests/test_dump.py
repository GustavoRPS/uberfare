from csv import QUOTE_NONNUMERIC
import unittest.mock as mock
import uberfare.dump as dump
from uberfare.fields import ESTIMATE_FIELDS


@mock.patch('builtins.open', new_callable=mock.mock_open)
@mock.patch('uberfare.dump.DictWriter', spec=True)
def test_csv_dumper(mock_dict_writer, mock_open):

    data = [{'currency_code': 'v1'}, {'timestamp': 'v2'}]
    output_file = 'test-out.csv'

    # force the file handler to have an empty file
    mock_open.return_value.tell.return_value = 0

    with dump.CsvDumper(output_file, ESTIMATE_FIELDS) as dumper:

        # test if instantiated correctly
        mock_open.assert_called_once_with(output_file, 'a')
        mock_dict_writer.assert_called_once_with(
                mock_open(), dumper.fieldnames, dialect='unix',
                quoting=QUOTE_NONNUMERIC)

        # using this instead of assert_called_once() since python3.5 has a prob
        assert mock_dict_writer.return_value.writeheader.call_count == 1

        dumper.dump(data)

        # test if called delegated objects correctly
        mock_dict_writer().writerows.assert_called_once_with(data)

    # make sure that file handle has been closed after exiting context manager
    mock_open.assert_has_calls([mock.call().close()])
