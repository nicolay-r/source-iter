import csv
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CsvService:

    @staticmethod
    def __write_core(target, lines_it, **csv_kwargs):
        with open(target, "w") as out_file:

            logger.info(f"Saving: {target}")

            csv_writer = csv.writer(
                out_file,
                delimiter=csv_kwargs.get("delimiter", ","),
                quotechar=csv_kwargs.get("quotechar", '"'),
                quoting=csv_kwargs.get("quoting", csv.QUOTE_MINIMAL))

            for content in lines_it:
                csv_writer.writerow(content)

    @staticmethod
    def write(target, data_it, header=None, it_type=None, **csv_kwargs):
        assert(isinstance(header, list) or header is None)

        def __it(content_it):

            columns_count = None
            if header is not None:
                columns_count = len(header)
                yield header

            for content in content_it:

                # If it is not None then consider it as the header for further checks.
                if columns_count is None:
                    columns_count = len(content)

                assert(len(content) == columns_count)
                yield content

        it_types = {
            # Return the actual content.
            None: lambda _it: _it,
            # This is a handy processor that allows to align data.
            "dict": lambda _it: map(lambda dict_data: [dict_data[column] for column in header], _it),
        }

        CsvService.__write_core(target=target, lines_it=__it(content_it=it_types[it_type](data_it)), **csv_kwargs)

    @staticmethod
    def read(src, skip_header=False, cols=None, as_dict=False, row_id_key=None, **csv_kwargs):
        assert (isinstance(row_id_key, str) or row_id_key is None)
        assert (isinstance(cols, list) or cols is None)

        header = None
        with open(src, newline='\n') as f:
            for row_id, row in enumerate(csv.reader(f, **csv_kwargs)):
                if skip_header and row_id == 0:
                    header = ([row_id_key] if row_id_key is not None else []) + row
                    continue

                # Determine the content we wish to return.
                if cols is None:
                    content = row
                else:
                    row_d = {header[col_ind]: value for col_ind, value in enumerate(row)}
                    content = [row_d[col_name] for col_name in cols]

                content = ([row_id-1] if row_id_key is not None else []) + content

                # Optionally attach row_id to the content.
                if as_dict:
                    assert (header is not None)
                    assert (len(content) == len(header))
                    yield {k: v for k, v in zip(header, content)}
                else:
                    yield content
