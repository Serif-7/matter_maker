#!/usr/bin/env python3

buf = []
questions = []

with open("pandoc_output.md", mode="r") as file:
    buf = file.readlines()

#filter out empty lines
buf = list(filter(lambda s : s != '\n', buf))

#extract questions
for line in buf:
    cursor = 0
    for c in line:
        if not c.isalpha():
            cursor += 1
        else:
            questions.append(line[cursor:])
            break

print(questions)

# This list will become the lines of the output file
lines = []

    
#create output file
#with open("output.yml", mode="x") as file:
    
