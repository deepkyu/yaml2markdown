from pathlib import Path
import argparse

from ruamel.yaml import YAML

from table import TableGenerator


WITH_DESCRIPTION = True
SAVE_AS = '.md'
_COMMENT_TOKEN_INDEX = 2  # Do not modify!

table_generator = TableGenerator()

def read_yaml_with_comment(filepath="example/test.yaml"):
    yaml_with_comment = YAML()
    
    with open(filepath, 'r') as f:
        yaml_str = f.read()
    
    data = yaml_with_comment.load(yaml_str)
    # assert print(list(data['train'].ca.items.keys()) == list(data['train'].keys()))
    return data

def generate_header(max_depth, with_description=True):    
    header = [f"Attr[{i}]" for i in range(1, max_depth + 1)]
    if with_description:
        header += ["Description"]
    return header
    

def generate_list_from_dict(data, max_depth, depth=0):
    elem_list = _generate_list_from_dict(data, max_depth, depth)
    return elem_list

def write_csv_from_dict(data, result_path="yaml.csv"):
    extension = Path(result_path).suffix
    max_depth = _depth(data)
    
    table_generator.num_col = max_depth + WITH_DESCRIPTION
    header = generate_header(max_depth, with_description=WITH_DESCRIPTION)
    table_generator.header = header

    elem_list = generate_list_from_dict(data, max_depth)
    table_generator.extend(elem_list)
    
    output = table_generator.generate(format=extension)
    with open(result_path, 'w') as f:
        f.write(output)

def _extract_comment(data, key):
    if key in data.ca.items:
        raw_comment = data.ca.items[key][_COMMENT_TOKEN_INDEX].value
        return raw_comment.strip()
    return

def _generate_list_from_dict(data, max_depth, depth=0):
    total_list = []
    if isinstance(data, dict):
        for key in data:
            # current_elem = _as_list(key, max_depth, depth+1, description=_extract_comment(data, key))
            current_elem = _as_list(key, max_depth, depth+1)
            child_list_candidate = _generate_list_from_dict(data[key], max_depth, depth+1)
            if isinstance(child_list_candidate, list):
                total_list.append(current_elem)
                total_list.extend(child_list_candidate)
            else:
                current_elem[depth+1] = f"{child_list_candidate} (`default`)"
                if WITH_DESCRIPTION:
                    current_elem[-1] = _extract_comment(data, key)
                total_list.append(current_elem)

        return total_list
    elif isinstance(data, list):
        total_list.append(_as_list("(LIST)", max_depth, depth+1))
        for elem in data:
            total_list.extend(_generate_list_from_dict(elem, max_depth, depth+1))
            
        return total_list
    
    return data

def _depth(data):
    if isinstance(data, dict):
        return 1 + (max(map(_depth, data.values())) if data else 0)
    if isinstance(data, list):
        return 1 + (max(map(_depth, data)) if data else 0)
    return 1

def _as_list(key, max_depth, depth):
    _template = ["" for _ in range(max_depth + WITH_DESCRIPTION)] # +1 for description column
    _template[depth - 1] = key
    return _template

def parse_args():
    
    parser = argparse.ArgumentParser(description="Parser for snippet about yaml2markdown converter")
    
    # -------- User arguments ----------------------------------------
    
    parser.add_argument(
        '-i', '--input', type=str, required=True,
        help="Input yaml path")
    
    parser.add_argument(
        '-o', '--output', type=str, default='README.md',
        help="Output markdown path")

    args, _ = parser.parse_known_args()    
    
    return args


if __name__ == "__main__":
    
    args = parse_args()
    suffix = Path(args.output).suffix.lower()
    
    if not suffix in ['.csv', '.tsv', '.md']:
        raise AssertionError(f"The extension is not supported!")

    data = read_yaml_with_comment(filepath=args.input)
    write_csv_from_dict(data, result_path=args.output)