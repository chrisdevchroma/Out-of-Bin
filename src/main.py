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

    address_offset = 0x00000000
    if len(json_address_offset) > 0:  # Validate
        if json_address_offset[:2].lower() == '0x':
            unpacked_address = json_address_offset[2:]
            address_offset = int(unpacked_address, 16)
            pass
        else:
            unpacked_address = json_address_offset
            address_offset = int(unpacked_address)
            pass
        pass
    print('Main address offset: 0x{:08X}\n'.format(address_offset))

    addresses = list()
    for block in json_addresses:
        offset: str = block['offset']
        text: str = block['text']

        print('\nValidating block with address offset: {0}...'.format(offset))

        if offset[:2].lower() == '0x':  # Validate
            unpacked_address = offset[2:]
            entry_address_offset = int(unpacked_address, 16)
            pass
        else:
            unpacked_address = offset
            entry_address_offset = int(unpacked_address)
            pass

        if entry_address_offset < 0:  # Sanity check
            print('Could not parse offset address! Skipping...')
            continue

        if len(text) < 1:  # Sanity check
            print('No text was given! Skipping...')
            continue

        construct = dict()
        construct.update({'offset': entry_address_offset})
        construct.update({'text': text})
        if 'original' in block:
            construct.update({'original': block['original']})
            pass

        addresses.append(construct)
        continue

    print('\n\nConstructing bin file...\n')
    construct_bin(output, address_offset, addresses)
    return


def construct_bin(output: str, address_offset: int, addresses: list):
    output_file = open(output, 'xb')

    output_file.write('TRANSLATE'.encode('utf8'))  # Header
    output_file.write(struct.pack('<I', address_offset))  # Address offset
    output_file.write(struct.pack('<L', len(addresses)))  # Amount of entries
    for i in range(len(addresses)):
        block = addresses[i]

        entry_address_offset: int = block['offset']
        text: str = block['text']

        if 'original' in block:
            orig = 'Original: \"{0}\"\n'.format(block['original'])
            pass
        else:
            orig = '\n'
            pass

        print('Index: 0x{:04X}'.format(i))
        print('Address offset: 0x{:08X}'.format(entry_address_offset))
        print('Text: \"{0}\"'.format(text))
        print(orig)

        output_file.write(struct.pack('<I', i))  # Write index
        text_data = text.encode('utf-8')

        output_file.write(struct.pack('<I', entry_address_offset))  # Address
        output_file.write(struct.pack('<H', len(text_data)))  # Length of text
        output_file.write(text_data)  # Text
        # Do not write entry original_text

        continue
    output_file.close()
    return


if __name__ == '__main__':
    main()
    pass
