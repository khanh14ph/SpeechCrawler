import glob
import sys

# Get filename from command line arguments
if len(sys.argv) > 1:
    foldername = sys.argv[1]
else:
    print("Error: Please provide a filename as a command line argument")
    sys.exit(1)
lst=glob.glob(f"{foldername}/*")
count=0
sub_count=0
all_lst=[]
for i in lst:
    temp_lst=open(i).read().splitlines()
    all_lst.extend(temp_lst)
all_lst=set(all_lst)
for j in all_lst:
    link,dur,sub_dur=j.split("\t")
    count+= float(dur)
    sub_count+=float(sub_dur)
print("Audio duration:",count)
print("Subtile duration: ",sub_count)
