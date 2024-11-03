from os.path import join

from source_iter.service_jsonl import JsonlService
from utils import TEST_DATA_DIR


def it_json_data():
    for line in JsonlService.read(join(TEST_DATA_DIR, "sample.jsonl")):
        yield line


JsonlService.write(target=join(TEST_DATA_DIR, "write_sample.jsonl"),
                   data_it=it_json_data())