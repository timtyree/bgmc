#!/bin/bash

# Compile the program
gcc levy_periodic.c -o levy_periodic.x

# Execute the program
./levy_periodic.x

# Remove the executable
rm levy_periodic.x
