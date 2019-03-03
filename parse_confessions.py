import re
import argparse
from datetime import datetime

# Hardcoding first confession number in file
# number = 20584
# raw = 'mit_confessions.txt'

def parse_confessions(raw, confessed, confession_number):
    confessions = []
    with open(raw, "r") as f:
        lines = f.readlines()
        in_confession = False
        confession = ""
        # Keeps track of line to get the date on the previous line where
        idx = 0
        for line in lines:
            # According to format
            # confession_number = "#" + str(number)
            pattern = re.compile(confession_number)
            match = pattern.match(line)
            if match:
                # Found new confession, confession_number separated by confession
                # with space
                date_line = lines[idx - 1]
                # Need to be able to extract date
                if "Yesterday" not in date_line and "hrs" not in date_line and ("PM" in date_line or "AM" in date_line):
                    # print(date_line[:-4] + "T")
                    # print(idx)
                    date_object = datetime.strptime(date_line[:-4], '%B %d at %I:%M %p')
                    date = date_object.strftime('%m/%d/2019 %H:%M:%S')
                    confession = date + ", \"" + line[len(match.group(0)) + 1:] + '\"'
                    in_confession = True
            else:
                if in_confession:
                    if "Comment" not in line:
                        confession += line
                    else:
                        confessions.append(confession)
                        confession = ""
                        in_confession = False
            idx += 1

    # print(confessions)
    # write to output
    with open(confessed, "w") as c:
        for confession in confessions:
            confession = confession.replace("\n", "")
            c.write(confession + "\n")

    print("done")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", action="store", dest="raw", type=str, required=True)
    parser.add_argument("-o", "--output", action="store", dest="confessed", type=str, required=True)
    parser.add_argument("-r", "--regex", action="store", help="Regex for numbering format", dest="confession_number", type=str, required=True)

    args = parser.parse_args()
    parse_confessions(args.raw, args.confessed, args.confession_number)
