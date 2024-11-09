from os.path import join

from source_iter.service_csv import CsvService
from utils import TEST_DATA_DIR


def it_json_data():
    # Read content.
    for line in CsvService.read(join(TEST_DATA_DIR, "sample.csv"), skip_header=True, as_dict=True, delimiter="\t"):
        yield line


# Save content.
header = ["entity"]
CsvService.write(join(TEST_DATA_DIR, "write_sample.csv"), header=header, data_it=it_json_data(), it_type="dict")
