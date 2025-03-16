# file_path_lst = [
#     "/home4/khanhnd/youtube_crawler/KTSpeechCrawler/link_list_new_1.txt",
#     "/home4/khanhnd/youtube_crawler/KTSpeechCrawler/link_list_new_2.txt",
#     "/home4/khanhnd/youtube_crawler/KTSpeechCrawler/link_list_new_3.txt",
# ]
# lst = []
# for i in file_path_lst:
#     temp_lst = open(i).read().split("\n")[:-1]
#     temp_lst = [j[-11:] for j in temp_lst]
#     lst.extend(temp_lst)
# lst1 = (
#     open("/home4/khanhnd/youtube_crawler/KTSpeechCrawler/downloaded.txt")
#     .read()
#     .split("\n")[:-1]
# )
# lst1 = [i.split()[-1] for i in lst1]
# lst.extend(lst1)
# lst = list(set(lst))
# with open("existed.txt", "w") as f:
#     for i in lst:
#         f.write(i + "\n")

lst=open("/home4/khanhnd/youtube_crawler/KTSpeechCrawler/topic.txt").read().split("\n")[:-1]
lst=[i.split(".")[-1].strip().split("và") for i in lst]
lst1=[]
for i in lst:
    i=[j.strip().lower() for j in i]
    lst1.extend(i)
lst1=list(set(lst1))
# Lưu danh sách vào file văn bản
with open("/home4/khanhnd/youtube_crawler/KTSpeechCrawler/topic.txt", "w") as file:
    for topic in lst1:
        file.write(topic + "\n")