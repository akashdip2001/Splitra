import os
import json

def recombine():
    with open("header.json", "r") as f:
        data = json.load(f)
    with open("output_" + data['original_filename'], "wb") as outfile:
        for part in data['parts']:
            with open(part, "rb") as infile:
                outfile.write(infile.read())
    print("Video recombined successfully as output_" + data['original_filename'])

if __name__ == "__main__":
    recombine()
