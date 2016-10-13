'''
Author: Ignacio Streuly
Date: 9/21/16

Instructions for running:
- Program takes three commands, an input file and output file and a command, phone or dollars.
- Thus running from the command line looks like:

$ python IgnacioStreuly-HW2.py <INPUT_FILE> <OUTPUT_FILE> COMMAND

- The command, typed with no quotes, will be either "phone" or "dollars".
- "phone" writes the list of matches to phones.txt and "dollars" writes to dollars.txt
- Output file is specified in the command line, writes over the one in the current dir or creates a new one if the file doesn't exist.

'''

import re
import sys

def main():
    if len(sys.argv) == 4:
        INPUT_FILE = str(sys.argv[1])
        OUTPUT_FILE = str(sys.argv[2])
        COMMAND = str(sys.argv[3])
    else:
        print "Invalid use, only use three (3) commands."
        return

    FULL_PATTERN_DOLLARS = re.compile('|'.join([
      r'[\$][\d{1,3}]\,\d{1,3}\,\d{1,3}', # $1,000,000
      r'[\$][\d{1,3}]\,\d{1,3}\.\d{1,2}', # $100,000.00, $10,000.00
      r'[\$][\d{1,5}]\.\d{1,2}', # $10000.00
      r'[\$](\d+\.\d{1,2})',  # $.50, $1.50
      r'[\$][\d{1,3}]\,\d{1,3}', #$100,000, $10,000, 1,000
      r'billion|billions',
      r'trillion|trillions',
      r'million|millions'
    ]), re.IGNORECASE)

    FULL_PATTERN_PHONE = re.compile('|'.join([
      r'\(\d{3}\)[\s]\d{3}[\s-]\d{4}', # (123) 123-1234
      r'\(\d{3}\)[-]\d{3}[\s-]\d{4}', # (123)-123-1234
      # r'^\d{3}[\s.-]\d{4}', # 123-1234
      r'\d{3}[-]\d{3}[\s-]\d{4}' # 123-123-1234
    ]), re.IGNORECASE)

    PATTERN = ""
    counter = 0

    try:
        input_file = INPUT_FILE
        output_file = open(OUTPUT_FILE, 'w+')
        print "Reading from file: " + INPUT_FILE + "..."

        if COMMAND == "phone":
            PATTERN = FULL_PATTERN_PHONE
            matches = open("phones.txt", "w+")
        elif COMMAND == "dollars":
            PATTERN = FULL_PATTERN_DOLLARS
            matches = open("dollars.txt", "w+")
        else:
            print "Invalid command"
            return

        newLine = ""

        for i, line in enumerate(open(input_file)):
            newLine = line
            for match in re.finditer(PATTERN, line):
                counter += 1
                matches.write(match.group(0)+"\n")
                newLine = line.replace(match.group(0), "[" + match.group(0) + "]")

            output_file.write(newLine)

        print str(counter) + " lines written to " + OUTPUT_FILE + " finding matches for command: " + COMMAND

    except IOError:
        print ("File not found.")

main()
