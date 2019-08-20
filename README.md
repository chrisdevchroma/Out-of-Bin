# Out-of-Bin


## Info
Please give credit where it's due if using my tool.


## Before using:
Install [Python](https://www.python.org/downloads/) (project is built using [3.7.3](https://www.python.org/downloads/release/python-373/))</br>


## Usage

#### Arguments:
- `--input` [`INPUT_JSON`] - Input json file
- `--output` [`OUTPUT_BIN`] - Output bin file

#### Example:
```
python main.py --input=INPUT_JSON_FILE --output=translated.bin
```

#### Tested on:
- Linux (Fedora 29) using Python 3.7.3

#### Input Json File Syntax:
```json
{
    "address_offset": "0x00000000",
    "addresses": [
          {
            "offset": "0x00FFFFFF",
            "text": "TEXT 1",
            "original": "SOME ORIGINAL TEXT 1"
          },
          {
            "offset": "0x00FFFFFF",
            "text": "TEXT 2",
            "original": "SOME ORIGINAL TEXT 2"
          }
     ]
}
```

#### How to find address offsets:
TODO
