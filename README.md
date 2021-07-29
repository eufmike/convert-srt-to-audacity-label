# convert-srt-to-audacity-label

- Modified by Mike Shih
- Original code credit to scateu
- GitHub Profile: https://github.com/scateu
- Repo: https://github.com/scateu/convert-srt-to-audacity-label


---

## Convert

Convert SRT file to audacity supported label. 

Useful when editing an long interview, with auto generated SRT files.

Multiple lines within a single SRT screen will be concatenated with `\\`.


## Installation

[Python 2/3](https://www.python.org/downloads/) is needed.

```bash
$ sudo pip install pysrt  #Linux or macOS
```

Or..

```bash
$ sudo easy_install pysrt
```

## Usage

### Single *.SRT file

```bash
$ python ./main.py -f /path/to/your/srt-file.srt

# for example:
$ python main.py demo.srt
# demo-LABELS.txt wrote.
```

### Folder includes *.SRT file

```bash
$ python ./main.py -d /path/to/your/

# for example:
$ python -d ./ 
# all *.srt files in ./ will be converted to .txt
# a merge file will also be created. 

# to turn merging off, add flag -nm
# for example:
$ python ./main.py -d /path/to/your/ -nm
```

## Platform

- macOS (Tested)
- Linux (Tested)
- Windows (Tested))

## Reference

- <https://github.com/agermanidis/autosub>: Command-line utility for auto-generating subtitles for any video file (Google API)
