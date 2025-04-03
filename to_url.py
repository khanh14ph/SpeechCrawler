import pandas as pd
import sys

# Get filename from command line arguments
filename = sys.argv[1]
print(filename)
# Read the file and extract the first column as a list
df = pd.read_csv(filename, sep="\t")
lst = df.iloc[:, 0].tolist()
with open("urls.txt","w") as f:
    for i in lst:
        f.write(i+"\n")