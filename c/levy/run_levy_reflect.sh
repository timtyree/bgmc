#!/bin/bash

# Compile the program
gcc levy_reflect.c -o levy_reflect.x

# Execute the program
./levy_reflect.x

# Remove the executable
rm levy_reflect.x
