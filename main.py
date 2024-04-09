import string

import pandas as pd

def get_prompt_parts(input_file='phrases.csv', delimiter='this address'):
    # Read lines from 'recognition.txt'
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Process each line
    prefixes = set()
    suffixes = set()
    for line in lines:
        # Split the line using the delimiter
        parts = line.strip().split(delimiter)
        prefixes.add(parts[0])
        suffixes.add(parts[1])
        # Add the 'thanks' at the end
        suffixes.add(parts[1] + ' thanks')
        # Add alternatives for TomTom as 2 words
        suffixes.add(parts[1].replace('TomTom', 'Tom Tom'))
        suffixes.add(parts[1].replace('TomTom', 'Tom Tom') + ' thanks')
    # Sort, so that we can compare the longest variations first
    return sorted(prefixes, key=len, reverse=True), sorted(suffixes, key=len, reverse=True)

def process_recognition_file(recog_file='df1_all_files.csv', recog_index=1,
                             output_file='output.txt'):
    prefixes, suffixes = get_prompt_parts()

    df = pd.read_csv(recog_file, sep='\\t')

    # Write modified lines to 'output.txt'
    with (open(output_file, 'w') as outfile):
        for r in df.iloc[:, recog_index]:
            prefix = ''
            postfix = ''
            for p in prefixes:
                if r.lower().startswith(p.lower()):
                    prefix = p
                    r = r[len(p):]
                    break
            for p in suffixes:
                # Ignore punctuation
                r_ = r.lower().translate(str.maketrans('', '', string.punctuation))
                p_ = p.lower().translate(str.maketrans('', '', string.punctuation))
                if r_.endswith(p_):
                    postfix = p
                    r = r[:-len(p)]
                    break
            outfile.writelines(f'{prefix}\t{r}\t{postfix}\n')


# Example usage
process_recognition_file()
