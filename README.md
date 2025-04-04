# Speech-Crawler: Automatic Dataset Construction for Speech Recognition from YouTube Videos
How to run:
# Cookie Authentication

Some videos are age restricted, so this module won't be able to access those videos without some sort of authentication. To do this, you will need to have access to the desired video in a browser. Then, you will need to download that pages cookies into a text file. You can use the Chrome/Edge extension [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm?hl=en) and select "Netscape" during export and paste them to cookies.txt or the Firefox extension [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt).

Once you have that, you can use the following to access age-restricted videos' captions like so.
Put the cookies.txt file in the same folder as run.sh

# In run.sh file

Change BASE_DIR, DATABASE_DIR, LANGUGAE as you want
Put the keyword in name_lst folder, as I put
```
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
