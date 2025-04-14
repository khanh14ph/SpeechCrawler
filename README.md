# Speech-Crawler: Automatic Dataset Construction for Speech Recognition from YouTube Videos
How to run:

Some note:
Ờm nếu dùng cookies thì sẽ qua được giới hạn độ tuổi. Tuy nhiên mình crawl liên tục vs lắm quá từ cookies đấy thì bọn youtube ban me account của mình (tạm thời). Nên mọi người có thể xem xét k cần dùng cookies (sửa ở file getlink.py với cả script yt-dlp ở get_audio, nó sẽ có arg --cookies cookies.txt, thêm hay k tuỳ b)

Nếu get_metadata hay get_audio thấy video not available liên tục thì là do youtube ban IP của mình cmnr, bật cloudfare (1.1.1.1) lên là crawl dc tiếp

# Cookie Authentication

Some videos are age restricted, so this module won't be able to access those videos without some sort of authentication. To do this, you will need to have access to the desired video in a browser. Then, you will need to download that pages cookies into a text file. You can use the Chrome/Edge extension [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en) and select "Netscape" during export and paste them to cookies.txt or the Firefox extension [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt).

Once you have that, you can use the following to access age-restricted videos' captions like so.
Put the cookies.txt file in the same folder as run.sh

# First step:
Tạo file .env:

LANGUAGE="de"
BASE_DIR="/Users/khanh/dev/crawler/SpeechCrawler"
NAME_LST_FOLDER=/Users/khanh/dev/crawler/SpeechCrawler/keywords/${LANGUAGE}
DATABASE="/Users/khanh/dev/crawler/database"

cái LANGUAGE kia thì search gu gồ ngôn ngữ + iso 2 char là ra

# Second step:
python mkdir_keywords.py
lệnh này để tạo file còn ghi keywords/query vào thôi

# Third step:
```
bash get_metadata.sh`
```
Đại khái thì nó sẽ đi lấy toàn bộ meta của vid rồi lưu vào folder. Cái này chưa support continue download dc nên mọi người cố gắng ko interupt cái lệnh này. Tại đằng nào nó chạy cũng nhanh, chỉ lấy metadata.
```
bash get_audio.sh
```
Giờ mình có đống meta data rồi, mình sẽ đi download audio. Cái này sẽ mất thời gian hơn, nhưng mà bạn có thể tắt giữa chừng rồi download tiếp được 

```
cd SpeechCrawler
pip intall -r requirements.txt
bash run.sh
```
##
```
## Citation

@article{lakomkin2018kt,
  title={KT-Speech-Crawler: Automatic Dataset Construction for Speech Recognition from YouTube Videos},
  author={Lakomkin, Egor and Magg, Sven and Weber, Cornelius and Wermter, Stefan},
  journal={EMNLP 2018},
  pages={90},
  year={2018}
}
