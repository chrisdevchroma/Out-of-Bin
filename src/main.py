#!/usr/bin/env python3

import argparse
import os
import json
import struct

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input', required=True, nargs=1, type=str, help='Input json file')
    parser.add_argument('--output', dest='output', required=True, nargs=1, type=str, help='Output bin file')
    args = parser.parse_args()

    _input = args.input[0]
    output = args.output[0]

    if not os.path.isfile(_input):
        print('Translated input json file does not exist!')
        return

    read_input_json = open(_input, 'r+t', encoding='utf8')
    blocks = json.load(read_input_json, encoding='utf8')
    read_input_json.close()

    if os.path.isfile(output):
        os.remove(output)
        pass

    output_file = open(output, 'xb')

    output_file.write('TRANSLATE'.encode('utf8'))  # Header
    output_file.write(struct.pack('<L', len(blocks)))  # Amount of entries
    for i in range(len(blocks)):
        block: dict = blocks[i]

        offset: str = block['offset']
        text: str = block['text']

        if len(offset) < 1 or len(text) < 1:
            print('Found invalid line at index {0}\nSkipping block...'.format(i))
            continue

        if 'original' in block:
            orig = ' Original: \"{0}\"'.format(block['original'])
            pass
        else:
            orig = ''
            pass

        print('Found block\nOffset: {0}, Text: \"{1}\"{2}\n'.format(offset, text, orig))

        output_file.write(struct.pack('<I', i))  # Write index

        if offset[2:].lower() == '0x':
            unpacked_address = offset[2:]
            pass
        else:
            unpacked_address = offset
            pass

        unpacked_address = int(unpacked_address, 16)

        if unpacked_address < 0:
            print('Invalid offset! Skipping block...')
            continue

        text_data = text.encode('utf-8')

        output_file.write(struct.pack('<I', unpacked_address))  # Address
        output_file.write(struct.pack('<H', len(text_data)))  # Length of text
        output_file.write(text_data)  # Text

        continue
    output_file.close()
    return


if __name__ == '__main__':
    main()
    pass
