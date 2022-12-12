#Program: Pyping
#Version: 1.0
#Date: December 12th, 2022
#Author: Keratin
##
# Import the necessary modules
import sys
import time
import socket
from termcolor import colored
from statistics import mean
import re

# Check if the user has provided the necessary command line arguments
argument_count = len(sys.argv)
if argument_count == 1:
    print("""Pyping v1.0.0 - Copyright (c) 2022 Keratin\n\nSyntax: pyping [Destination IPv4] [TCP Port]\n\nOptions:\n    pyping [ip] [port] [delay] - (optional) set pause in-between pings \n""")
    exit()

# Get the IP address and port to ping from the command line arguments
ip = sys.argv[1]
port = int(sys.argv[2])

# Validate the IP address and port
if port > 65535 or port < 0:
    print("The specified port is either higher than 65535 or lower than 0.")
    exit()

# Use a regular expression to check if the IP address is valid
if re.match("^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$", ip):
    pass
else:
    print("The specified ip is not a valid ipv4.")
    exit()

# Check if the user has provided a delay between pings
if argument_count == 4:
    pause = int(sys.argv[3]) 
else:
    pause = 1

# Error strings
timeout_error_display = colored("Connection timed out.", "red")

# Class to keep track of connection statistics
class stats:
    connection_time_array = []
    attempted_pings = 0
    failed_pings = 0
    connected_ping = 0

def Main():
    try:
        while True:
            # Create a socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Set a timeout for the ping in seconds
            s.settimeout(1)

            # Record the start time
            start_time = time.time()

            # Attempt to connect to the IP and port
            s.connect((ip, port))

            # Record the end time
            end_time = time.time()

            # Calculate the ping time in milliseconds
            ping_time = round((end_time - start_time) * 1000, 2)
            stats.connection_time_array.append(ping_time)
            
            # Display IP and Port
            ip_display = colored(ip, "green")
            port_display = colored(str(port), "green")
            ms_display = colored(str(ping_time)+"ms", "green")

            # Print the ping time in milliseconds
            print(f"Connected to {ip_display}: time={ms_display} protocol=TCP port={port_display}")

            # Close the socket
            s.close()
            stats.attempted_pings += 1
            stats.connected_ping += 1 
            time.sleep(pause)

    except socket.timeout:
        # handle the timeout error
        print(timeout_error_display)
        stats.attempted_pings += 1
        stats.failed_pings += 1
        time.sleep(pause)
        Main()

try:
    Main()

except KeyboardInterrupt:
    if stats.failed_pings == 0:
        Failed_Percentage = "0.00"
    else:
        Failed_Percentage = str(round((stats.failed_pings / stats.attempted_pings) * 100, 2))

    if stats.attempted_pings == 0:
            print(f"""Connection statistics:\n        Attempted = 0, Connected = 0, Failed = 0 (0.00%)\nApproximate connection times:\n        Minimum = 0.00ms, Maximum = 0.00ms, Average = 0.00ms\n\n""")

    elif len(stats.connection_time_array) == 0:
                print(f"""Connection statistics:\n        Attempted = {str(stats.attempted_pings)}, Connected = {str(stats.connected_ping)}, Failed = {str(stats.failed_pings)} ({Failed_Percentage}%)\nApproximate connection times:\n        Minimum = 0.00ms, Maximum = 0.00ms, Average = 0.00ms\n\n""")

    else:
        print(f"""Connection statistics:\n        Attempted = {str(stats.attempted_pings)}, Connected = {str(stats.connected_ping)}, Failed = {str(stats.failed_pings)} ({Failed_Percentage}%)\nApproximate connection times:\n        Minimum = {str(min(stats.connection_time_array))}ms, Maximum = {str(max(stats.connection_time_array))}ms, Average = {str(round(mean(stats.connection_time_array), 2))}ms\n""")