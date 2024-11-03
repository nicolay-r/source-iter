import json


class JsonlService(object):

    @staticmethod
    def read(src, row_id_key=None):
        with open(src, "r") as out_file:
            for line_ind, line in enumerate(out_file.readlines()):
                content = json.loads(line)
                if row_id_key is not None:
                    content[row_id_key] = line_ind
                yield content

    @staticmethod
    def write(target, data_it, **json_kwargs):

        # Make sure that we are not encountered with encoding problem.
        if "ensure_ascii" not in json_kwargs:
            json_kwargs["ensure_ascii"] = False

        with open(target, "w") as out_file:
            for item in data_it:
                content = json.dumps(item, **json_kwargs)
                out_file.write(f"{content}\n")
