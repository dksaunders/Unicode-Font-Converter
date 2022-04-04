#!/usr/bin/env python3
import json
import argparse

# HELPER FUNCTIONS - load the necessary data
def initialize_character_dictionary():
    with open('fonts.json', 'r') as character_file:
        characters = json.load(character_file)
        return characters

def calculate_offsets(initial_characters):
    offsets = dict.fromkeys( initial_characters.keys() )
    for font in initial_characters:
        offsets[font] = dict.fromkeys( initial_characters[font].keys() )
        for style in initial_characters[font]:
            offsets[font][style] = dict()
            offsets[font][style]['Capital'] = ord(initial_characters[font][style]['Capital']) - ord('A')
            offsets[font][style]['Small'] = ord(initial_characters[font][style]['Small']) - ord('a')
    return offsets

# GLOBAL VARIABLES
INITIAL_CHARACTERS = initialize_character_dictionary()
OFFSET_LOOKUP = calculate_offsets(INITIAL_CHARACTERS)

# FUNCTIONS
def is_capital(ordinal):
    return (ordinal >= 65) and (ordinal <= 90)

def is_small(ordinal):
    return (ordinal >= 97) and (ordinal <= 122)

def convert_text(font, style, text):
    offsets = OFFSET_LOOKUP[font][style]
    output =''
    for character in text:
        ordinal = ord(character)
        if is_capital(ordinal):
            output += chr(ordinal + offsets['Capital'])
        elif is_small(ordinal):
            output += chr(ordinal + offsets['Small'])
        else:
            output += chr(ordinal)
    return output
        
def main():
    parser = argparse.ArgumentParser(
        prog='funky_fonts.py',
        description='Converts text into cool fonts and shit.'
    )
    operation = parser.add_subparsers(
        dest='command'
    )
    convert = operation.add_parser('convert')
    convert.add_argument(
        'font',
        choices=INITIAL_CHARACTERS.keys(),
        help='the font'
    )
    convert.add_argument(
        'style',
        choices=['Plain', 'Bold', 'Italic', 'Bold Italic'],
        help='whether the font should be bold and/or italicized'
    )
    convert.add_argument(
        'text',
        help='the text to be converted'
    )
    show = parser.add_mutually_exclusive_group()
    show.add_argument(
        '--list-fonts',
        action='store_true',
        help='lists available fonts'
    )
    show.add_argument(
        '--list-styles',
        choices=INITIAL_CHARACTERS.keys(),
        help='lists available styles for the specified font'
    )
    show.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.1'
    )
    args = parser.parse_args()

    if (args.list_fonts):
        print('The fonts available are:')
        for font in INITIAL_CHARACTERS.keys():
            print(f'\t{font}')
    
    if (font := args.list_styles):
        print(f'The styles available for {font} are:')
        for style in INITIAL_CHARACTERS[font]:
            print(f'\t{style}')
    
    if (args.command == 'convert'):
        if (args.style not in OFFSET_LOOKUP[args.font]):
            raise ValueError(f'{args.font} doesn\'t have a style called "{args.style}".')
        
        print(
            convert_text(
                args.font,
                args.style,
                args.text
            )
        )

if __name__ == '__main__':
    main()