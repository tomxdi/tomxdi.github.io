#!/usr/bin/env python

# conda install -c conda-forge gitpython
# conda install -c conda-forge openai
# OPENAI_API_KEY=

import os
from pathlib import Path

import openai
from git import Repo

from absl import app
from absl import flags
from absl import logging
from absl.logging import PythonFormatter

openai.api_key = os.getenv('OPENAI_API_KEY')

PATH_TO_BLOG_REPO=Path('/home/tom/projects/github.com/tomxdi/tomxdi.github.io/.git')
PATH_TO_XXX = Path('https://tomxdi.github.io/')

FLAGS = flags.FLAGS
flags.DEFINE_string("topic", "Bike riding", "Specify the blog topic")
#flags.DEFINE_bool("show", True, "Show files included zipfile")

# absl needs argv
def main(argv):
    topic = FLAGS.topic
    
    openai.api_key = os.getenv('OPENAI_API_KEY')

    PATH_TO_BLOG_REPO=Path('/home/tom/projects/github.com/tomxdi/tomxdi.github.io/.git')
    PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
    PATH_TO_CONTENT = PATH_TO_BLOG/"content"
    print(PATH_TO_CONTENT)
    PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)

    def update_blog(commit_message="Update blog"):
        repo = Repo(PATH_TO_BLOG_REPO)
        # git add .
        repo.git.add(all=True)
        # git commt -m "msg"
        repo.index.commit(commit_message)
        # git push
        origin = repo.remote(name='origin')
        origin.push()

    random_text_string = "xxxxxx"

    with open(PATH_TO_BLOG/"index.html", "w") as f:
        f.write(random_text_string)
    
    update_blog()
    

    # Path('https://tomxdi.github.io/')





if __name__ == "__main__":
    logging.set_verbosity(logging.INFO)

    err = app.run(main)  # parse absl flags   
    if err:
        sys.exit(f"ERROR: {err}")     

    print("\nSUCCESS!")    

