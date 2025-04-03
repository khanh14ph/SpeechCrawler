import pandas as pd
import sys

# Get filename from command line arguments
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("Error: Please provide a filename as a command line argument")
    sys.exit(1)

# Read the file and extract the first column as a list
df = pd.read_csv(filename, sep="\t")
lst = df.iloc[:, 0].tolist()
with open("urls.txt","w") as f:
    for i in lst:
        f.write(i+"\n")