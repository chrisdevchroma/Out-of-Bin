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
    read_json_data = json.load(read_input_json, encoding='utf8')
    read_input_json.close()

    # Remove output if it exists
    if os.path.isfile(output):
        os.remove(output)
        pass

    json_address_offset = read_json_data['address_offset']
    json_addresses = read_json_data['addresses']

    output_file = open(output, 'xb')

    output_file.write('TRANSLATE'.encode('utf8'))  # Header

    address_offset = 0x00000000
    if len(json_address_offset) > 0:
        if json_address_offset[2:].lower() == '0x':
            unpacked_address = json_address_offset[2:]
            pass
        else:
            unpacked_address = json_address_offset
            pass
        address_offset = int(unpacked_address, 16)
        pass

    output_file.write(struct.pack('<I', address_offset))  # Address offset
    output_file.write(struct.pack('<L', len(json_addresses)))  # Amount of entries
    for i in range(len(json_addresses)):
        block: dict = json_addresses[i]

        offset: str = block['offset']
        text: str = block['text']

        if len(offset) < 1 or len(text) < 1:
            print('Found invalid line at index {0}\nSkipping block...'.format(i))
            continue

        if 'original' in block:
            orig = 'Original: \"{0}\"\n'.format(block['original'])
            pass
        else:
            orig = '\n'
            pass

        print('Offset: {0}'.format(offset))
        print('Text: \"{0}\"'.format(text))
        print(orig)

        output_file.write(struct.pack('<I', i))  # Write index

        if offset[2:].lower() == '0x':
            unpacked_address = offset[2:]
            pass
        else:
            unpacked_address = offset
            pass

        unpacked_address = int(unpacked_address, 16)

        if unpacked_address < 0:
            print('Invalid offset! Skipping...\n')
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
