import pysrt
import re
import subprocess
import datetime
import os

VID_FILE = 'Example.avi'
SRT_FILE = 'Example.srt'
USE_REENCODING = True

def get_subs():
    subs = pysrt.open(SRT_FILE)
    return subs

def filter_subs(subs, pattern):
    ret = []
    for sub in subs:
        if re.search(pattern, sub.text, re.MULTILINE):
            ret.append(sub)
    return ret

def time_to_timedelta(time):
    return datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second, milliseconds=time.microsecond/1000)

def extract_clip(sub, filename):
    start = sub.start.to_time()
    duration = (sub.end - sub.start).to_time()
    extended = time_to_timedelta(duration) + datetime.timedelta(seconds=1)
    if USE_REENCODING:
        args = 'ffmpeg -i "{}" -ss {} -t {} -vcodec libx264 -async 1 {}'.format(VID_FILE, start, extended, filename)
    else:
        args = 'ffmpeg -i "{}" -ss {} -t {} -acodec copy -vcodec copy -async 1 {}'.format(VID_FILE, start, extended, filename)
    # print args
    subprocess.call(args)

def get_extension(file_path):
    extension = os.path.splitext(file_path)[1]
    return extension

def get_clip_names(subs, prefix=''):
    extension = get_extension(VID_FILE)
    return ['{}_{}{}'.format(prefix, sub.index, extension) for sub in subs]

def extract_clips(subs, clip_names):
    for sub, clip_name in zip(subs, clip_names):
        extract_clip(sub, clip_name)

def get_ffmpeg_concact(file_names):
    lines = ["file '{}'".format(f) for f in file_names]
    return '\n'.join(lines)

def merge_clips(clip_names, output_name):
    concat = output_name + '_concat.txt'
    with open(concat, 'w') as f:
        f.write(get_ffmpeg_concact(clip_names))

    subprocess.call('ffmpeg -f concat -i {} -c copy {}'.format(concat, output_name))
    os.remove(concat)

def srt_cut(prefix, pattern):
    all_subs = get_subs()
    subs_to_extract = filter_subs(all_subs, pattern)
    print len(subs_to_extract), 'parts to extract'
    if len(subs_to_extract) is 0:
        return
    clip_names = get_clip_names(subs_to_extract, prefix)
    extract_clips(subs_to_extract, clip_names)

    output_name = '{}_merge{}'.format(prefix, get_extension(VID_FILE))
    merge_clips(clip_names, output_name)
    map(os.remove, clip_names)

def main():
    srt_cut('prefix', '(r|R)egex')

if __name__ == '__main__':
    main()