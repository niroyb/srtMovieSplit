"""Splits a video based on words from the subtitles"""
import re
import subprocess
import datetime
import os

import pysrt


def srt_movie_split(path_video, path_subtitle, prefix, pattern, use_reencoding=True):
    """Creates a movie clip based on a regex search of the subtitles"""

    # Select a subset of subtitles
    all_subs = pysrt.open(path_subtitle)
    subs_to_extract = filter_subs(all_subs, pattern)
    print len(subs_to_extract), 'parts to extract'

    # Quick exit
    if len(subs_to_extract) is 0:
        return

    # Create clips
    extension = get_extension(path_video)
    clip_names = get_clip_names(subs_to_extract, extension, prefix)
    extract_clips(path_video, subs_to_extract, clip_names, use_reencoding)

    # Merge clips
    output_name = '{}_merge{}'.format(prefix, extension)
    merge_clips(clip_names, output_name)

    # Cleanup
    map(os.remove, clip_names)


def get_ffmpeg_concact(file_names):
    """Returns the file names in a formatted string for the 'ffmpeg concat' command"""
    lines = ["file '{}'".format(f) for f in file_names]
    return '\n'.join(lines)


def merge_clips(clip_names, output_name):
    """Merges the clips to the given output file name"""
    concat = output_name + '_concat.txt'
    with open(concat, 'w') as f:
        f.write(get_ffmpeg_concact(clip_names))

    subprocess.call('ffmpeg -f concat -i {} -c copy {}'.format(concat, output_name))
    os.remove(concat)


def time_to_timedelta(time):
    """Converts a python time object to a deltatime one"""
    return datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second,
                              milliseconds=time.microsecond / 1000)


def extract_clip(path_video, sub, filename, reencode):
    """Extracts a clip from the given video path based on the time codes of the subtitle object"""
    start = time_to_timedelta(sub.start.to_time()) - datetime.timedelta(seconds=0.5)
    duration = (sub.end - sub.start).to_time()
    extended = time_to_timedelta(duration) + datetime.timedelta(seconds=0.5)

    if reencode:
        args = 'ffmpeg -i "{}" -ss {} -t {} -vcodec libx264 -async 1 {}'.format(path_video, start, extended, filename)
    else:
        args = 'ffmpeg -i "{}" -ss {} -t {} -acodec copy -vcodec copy -async 1 {}'.format(path_video, start, extended,
                                                                                          filename)
    subprocess.call(args)


def extract_clips(path_video, subs, clip_names, reencode=True):
    """Creates a clip from a movie for each subtitle object"""
    for sub, clip_name in zip(subs, clip_names):
        extract_clip(path_video, sub, clip_name, reencode)


def get_clip_names(subs, extension, prefix=''):
    """Returns a list of unique clip names based on the subtitle objects"""
    return ['{}_{}{}'.format(prefix, sub.index, extension) for sub in subs]


def filter_subs(subs, pattern):
    """Returns a list of subtitles who's text contains the given regex pattern"""
    ret = []
    for sub in subs:
        if re.search(pattern, sub.text, re.MULTILINE):
            ret.append(sub)
    return ret


def get_extension(file_path):
    """Returns the extension of a file path with the dot"""
    extension = os.path.splitext(file_path)[1]
    return extension


def main():
    # Demo use: you can simply run this script
    path_video = 'DemoData/Sintel.2010.x264-VODO.mp4'
    path_srt = 'DemoData/sintel_en.srt'
    srt_movie_split(path_video, path_srt, 'scales', '(s|S)cales')
    #srt_movie_split(path_video, path_srt, 'you', '(y|Y)ou')


if __name__ == '__main__':
    main()