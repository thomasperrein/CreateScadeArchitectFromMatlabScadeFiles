# coding : utf-8
"""
Script pour parser un fichier .xscade et en dégager les data d'intérêts 
"""

import json


def read_file(input_path):
    """ read file in arg """
    with open(f'{input_path}', encoding='utf-8') as user_file:
        file_contents = user_file.read()
    parsed_json = json.loads(file_contents)
    return parsed_json


def main():
    """ main function """
    return read_file(r'Tests\atomic.json')


if __name__ == "__main__":
    main()
