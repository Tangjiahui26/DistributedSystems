import os
import sys
import json
import subprocess
import re

cur_dir = os.path.dirname( os.path.realpath(__file__) )
test_cases_file = os.path.abspath(os.path.join(cur_dir, "test_cases.json")) # file path for input test cases json file
client_path = os.path.abspath(os.path.join(cur_dir, "..", "client")) # path to program executable

# load json file for test cases into dict
with open(test_cases_file, 'r') as f:
    test_cases = json.load(f)

# loop through test cases and execute tests individually
for regexp, expected_outputs in test_cases.items():
    
    print ("Running test for regular expression " + regexp)
    
    # execute grep command at client
    try:
        output = subprocess.check_output([client_path, regexp])
    except subprocess.CalledProcessError as e:
        print ("\tError executing client command...\n\n" + e.output)
        continue

    # check for expected output
    for i,expected_output in enumerate(expected_outputs):
        my_regex = r"No Results from machine\." + str(i+1) + r"\.log.*Server cannot be connected\."
        if re.search(my_regex, output.decode()):
            print ("\tVM" + str(i+1) + " is not online")
        elif expected_output in output.decode():
            print ("\tTest passed for VM" + str(i+1))
        else:
            print ("\tTest failed for VM" + str(i+1))
