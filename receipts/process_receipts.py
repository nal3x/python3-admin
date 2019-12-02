import glob
import os
import shutil
import json

try:
    os.mkdir("./processed")
except OSError:
    print("'processed' directory already exists")

# Get a list of receipts
receipts = glob.glob('./new/receipt-[0-9]*.json')
subtotal = 0.0

for path in receipts:
    with open(path) as f:
        content = json.load(f)
        subtotal += float(content['value']) #read 'value' value from json
    name = path.split('/')[-1] #take last element from path
    destination = f"./processed/{name}"
    shutil.move(path, destination)
    print(f"moved '{path}' to '{destination}'")

print("Receipt subtotal: $%.2f" % subtotal)
