# Script to read detailed statistics from Phasmophobia savegames

## Usage

Run without arguments, the script attempts to use the default savegame-path. To specify a custom location, use flag --path: `python3 main.py --path </path/to/SaveFile.txt>`

By default, output is in basic human-readable textform with stats grouped into categories. For further visualization purposes, it can be exported into csv-form: `python3 main.py --csv <filename.csv>`

Examples of both text and csv-output can be found in the examples directory.