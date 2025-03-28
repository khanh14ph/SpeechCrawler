# -*- coding: utf-8 -*-
import sys
import os
import json
import io
import termcolor
import re
from tqdm import tqdm
from youtube_helpers import get_hash, getsize
from utils import extract_audio_part_segment
from filters import Pipeline, OverlappingSubtitlesRemover, SubtitleCaptionTextFilter, SubtitleMerger,\
    CaptionLengthFilter, CaptionRegexMatcher, CaptionDurationFilter, CaptionLeaveOnlyAlphaNumCharacters, CaptionNormalizer
from youtube_helpers import load_all_subtitles


class RESULT:
    GOOGLE_TEST_NOT_PASSED = 0
    OK = 1


good_chars_regexp = re.compile(r"[a-zA-Z_ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ]+$/", re.IGNORECASE)
pipeline = Pipeline([
    OverlappingSubtitlesRemover(),
    SubtitleCaptionTextFilter(),
    CaptionNormalizer(),
    # CaptionRegexMatcher(good_chars_regexp),
    CaptionLengthFilter(min_length=5),
    # CaptionLeaveOnlyAlphaNumCharacters(),
    SubtitleMerger(max_len_merged_sec=10),
    CaptionDurationFilter(min_length=1, max_length=20.0)
])



if __name__ == "__main__":
    video_file = sys.argv[1]
    print("video_file: ",video_file)
    idv=video_file.split("/")[6][0:11]
    target_dir = sys.argv[2]

    ext = "m4a"

    subtitle_file_vtt = video_file.replace(f'.{ext}', '.vi.vtt')
    subtitle_file_srt = video_file.replace(f'.{ext}', '.vi.srt')
    info_file = video_file.replace(f'.{ext}', '.info.json')
    overall_info = {"sub_file" : subtitle_file_vtt, "info" : info_file}
    log_file = open("./log.json", "a+")
    print("srt exist :", os.path.exists(subtitle_file_srt))
    print("vtt exist :",os.path.exists(subtitle_file_vtt))
    print("--------")
    result = RESULT.OK
    try:
        if not os.path.exists(info_file) or  (os.path.exists(subtitle_file_vtt)==False and os.path.exists(subtitle_file_srt)==False):
            termcolor.cprint("Subtitle file or Info files do not exist. {}".format(video_file), color="red" )
            raise Exception("Subtitle file or Info files do not exist.")

        #Download google subtitle to cross check with closed captions
        with open(info_file) as f:
            metadata = json.load(f)
        #youtube_link = metadata['webpage_url']
        print("Parsing subtitle")
        if os.path.exists(subtitle_file_vtt):
            subtitle_file=subtitle_file_vtt
            subtitles = load_all_subtitles(subtitle_file,"vtt")
        else:
            subtitle_file=subtitle_file_srt
            subtitles = load_all_subtitles(subtitle_file,"srt")
        print(len(subtitles))
        input = {
            'subtitles': subtitles,
            'video_file': video_file
        }
        overall_info["num_subtitles"] = len(subtitles)
        termcolor.cprint("Got {} candidates".format(len(subtitles)), color="yellow")


        filtered_input = pipeline(input)
        filtered_subtitles = filtered_input["subtitles"]

        termcolor.cprint("Writing {} samples".format(len(filtered_subtitles)), color="cyan")
        for idx,t in enumerate(tqdm(filtered_subtitles)):
            idx=str(idx)
            # hash = get_hash(subtitle_file + t["original_phrase"] + str(t["ts_start"]))
            wav_file_dir = os.path.join(target_dir, "wav", idv)
            txt_file_dir = os.path.join(target_dir, "txt", idv)
            metadata_dir = os.path.join(target_dir, "metadata", idv)

            os.makedirs(wav_file_dir, exist_ok=True)
            os.makedirs(txt_file_dir, exist_ok=True)
            os.makedirs(metadata_dir, exist_ok=True)

            target_wav_file = os.path.join(wav_file_dir, idx + ".wav")
            target_txt_file = os.path.join(txt_file_dir, idx + ".txt")
            target_metadata_file = os.path.join(metadata_dir, idx + ".json")

            text = t["original_phrase"]
            if len(text) == 0:
                continue
            if not os.path.exists(target_wav_file) or not os.path.exists(target_txt_file):
                extract_audio_part_segment(video_file, t["ts_start"], t["ts_end"], target_wav_file)
                
                with io.open(target_txt_file, "w", encoding='utf-8') as f:
                    f.write(text)

                with io.open(target_metadata_file, "w", encoding='utf-8') as f:
                    t["ts_start"] = str(t["ts_start"])
                    t["ts_end"] = str(t["ts_end"])
                    t["metadata"] = metadata
                    json.dump(t, f)
                
                assert os.path.exists(target_txt_file) and os.path.exists(target_wav_file) \
                       and getsize(target_wav_file) > 4 * 1024, "{} not created".format(target_wav_file)
    except Exception as e:
        termcolor.cprint(e, color="red")
    finally:
        print("DONE AUDIO WITH ID ",idv)
        overall_info["result"] = result
        log_file.write(json.dumps(overall_info) + "\n")
        log_file.flush()
        log_file.close()
        #if os.path.exists(video_file):
        #    os.remove(video_file)
            #if os.path.exists(subtitle_file):
            #    os.remove(subtitle_file)
            #if os.path.exists(info_file):
            #    os.remove(info_file)
