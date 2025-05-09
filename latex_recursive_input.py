import os

def get_file_contents(root: str, fname: str) -> str:
    """Function that opens a .tex file, and then recursively builds a string containing the contents of the file, including all contents of \\input tags.
    fname should have the .tex filetype
    """
    fpath = os.path.join(root, fname)
    assert os.path.isfile(fpath), f"{fpath=} is not a file"
    with open(os.path.join(root, fname), 'r') as f:
        file_buffer = ""
        for line in f.readlines():
            if r"\input{" in line:
                input_split = line.split(r"\input{", 1)
                if "%" not in input_split[0]:
                    input_fname = input_split[1].split("}")[0]
                    line = get_file_contents(root=root, fname=input_fname + ".tex")
            file_buffer += line
    return file_buffer


def main():
    import argparse
    parser = argparse.ArgumentParser(prog="latex_recursive_input")
    parser.add_argument("--root", type=str, required=True, help=HELP_DICT["root"])
    parser.add_argument("--main", type=str, required=True, help=HELP_DICT["main"])
    parser.add_argument("--output", type=str, required=False, help=HELP_DICT["output"])

    args = parser.parse_args()

    root = args.root
    main = args.main
    output = args.output

    file_contents = get_file_contents(root=root, fname=main)

    if output is None:
        print(file_contents)
    else:
        with open(os.path.join(root, output), "w") as f:
            f.write(file_contents)
    exit(0)


HELP_DICT = {
    "root": "fully qualified path to the directory containing the project main document.",
    "main": "full filename within root of the main document file to be recursively generated.",
    "output": "full filename within root of the output file. If not specified, the file is printed to stdout",
}

if __name__ == "__main__":
    main()
