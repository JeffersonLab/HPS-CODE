#!/bin/env python
import sys,re,math
file_count = 0
input_count = 0
output_count = 0
for filename in sys.argv[1:]:
    with open(filename) as file:
        for line in file:
            match = re.match(r'Read (\d+) events, wrote (\d+) of them',line)
            if match:
                print filename+": "+line[:-1]
                #print match.groups()
                file_count += 1
                input_count += int(match.group(1))
                output_count += int(match.group(2))
                break
print "totals from {0} files: {1} input events, {2} output events".format(file_count, input_count, output_count)
print "average per file: {0:.1f} input events, {1:.1f} output events".format(float(input_count)/file_count, float(output_count)/file_count)
print "efficiency: {0:.4f} pm {1:.4f}".format(float(output_count)/input_count,math.sqrt(output_count)/input_count)
