# Simple script that gets wifi profiles and prints our thier passwords

import subprocess
import re

# Run subprocess for netsh to grab wifi ID and decode it to be used in a string
output = subprocess.run(["netsh", "wlan", "show", "profiles"],
                        capture_output=True).stdout.decode()

# Use regular expressions to get just the names
profiles = (re.findall("All User Profile     : (.*)\r", output))

# list for wifi profiles
profile_list = list()

# Loop through profiles where we have names
if len(profiles) != 0:
    for name in profiles:
        # Create dictionary for each connection
        profile = dict()

        # Run similar command as above but for getting security keyt info
        profile_info = subprocess.run(
            ["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()

        # Use regular expression to get correct info
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            # Grab the profilew name
            profile["ssid"] = name
            # Run comand to grab password
            profile_info_pass = subprocess.run(
                ["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
            # Use regular expression to get just the password
            password = re.search(
                "Key Content            : (.*)\r", profile_info_pass)

            # Check if we found a password
            if password == None:
                profile["password"] = None
            else:
                profile["password"] = password[1]

            # Append wifi info to the list
            profile_list.append(profile)

# Print out passwords
print()
for x in range(len(profile_list)):
    print(profile_list[x])
print()
