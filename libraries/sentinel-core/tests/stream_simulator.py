from pathlib import Path
from typing import Generator
import csv

PAYSIM_DIR = '/home/lucas/github/argus/data'

def stream_simulator(data: str) -> Generator[list[str], None, None]:
    """
    Simulates an infinite 'stream' of the data from the csv file by looping through it continuously.
    It yields a generator object and defines no .send method or finishing return statement.

    Args:
        str: The name of the csv file.
    Yields:
        List[str]: A generator object that can iterate continuously through the csv rows.

    """
    base_dir = Path(PAYSIM_DIR)
    filestring = Path(data)
    full_path = base_dir / filestring

    if not data:
        raise ValueError('No data source provided.')
    if not data.endswith('.csv'):
        raise TypeError
    if not full_path.exists():
        raise FileNotFoundError(f'File {data} not found.')

    else:
        while True:
            file_obj = open(f'{full_path}', 'r')

            reader_obj = csv.reader(file_obj)
            # Skip header
            next(reader_obj, None)
            first_data_row = next(reader_obj, None)

            if first_data_row is None:
                raise ValueError('Error: No data in stream.')

            # yield first row of data if data was found
            yield first_data_row
            # followed by rest of data (may be empty)
            for row in reader_obj:
                yield row

