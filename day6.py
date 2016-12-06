import collections, fileinput

print("Taking input from stdin, Ctrl-Z to stop")
with fileinput.input() as lines:
    lines = list(lines)
    flipped_lines = zip(*lines[::-1]) # http://stackoverflow.com/q/8421337

    error_corrected = ""
    error_corrected_2 = ""
    for column in flipped_lines:
        counter = collections.Counter(column)
        highest_key = max(counter, key=(lambda x: counter[x])) # http://stackoverflow.com/q/268272/#comment19151924_268285
        lowest_key = min(counter, key=(lambda x: counter[x]))

        error_corrected += highest_key
        error_corrected_2 += lowest_key

    print(" - The error-corrected code is {} -".format(error_corrected.strip()))
    print(" - The alternately error-corrected code is {} -".format(error_corrected_2.strip()))
