import os
from setuptools import setup

install_requires = ["pysrt"]

base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name = "srt-movie-split",
    version = "1.0.dev",
    description = "Splits a video based on words from the subtitles",
    long_description = open(os.path.join(base_dir, "README.md"), "r").read(),
    url = "https://github.com/niroyb/srtMovieSplit",
    author = "Nick R",
    author_email = "niroyb+github@gmail.com",
    packages = ["srt-movie-split"],
    zip_safe = False,
    install_requires = ["pysrt"],
)
