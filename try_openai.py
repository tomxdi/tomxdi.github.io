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
flags.DEFINE_bool("init", False, "Do one time initialization")
flags.DEFINE_bool("update", False, "Update the git blog")
flags.DEFINE_string("topic", "Bike riding", "Specify the blog topic")
#flags.DEFINE_bool("show", True, "Show files included zipfile")

def update_blog(repo_path, commit_message="Update blog"):
    print("Update blog repo {repo_path}")  

    repo = Repo(repo_path)
    
    # git add .
    repo.git.add(all=True)
    # git commt -m "msg"
    repo.index.commit(commit_message)
    # git push
    origin = repo.remote(name='origin')
    origin.push()


# absl needs argv
def main(argv):
    init = FLAGS.init
    update = FLAGS.update
    topic = FLAGS.topic    
    
    openai.api_key = os.getenv('OPENAI_API_KEY')

    PATH_TO_BLOG_REPO=Path('/home/tom/projects/github.com/tomxdi/tomxdi.github.io/.git')
    PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
    PATH_TO_CONTENT = PATH_TO_BLOG/"content"
    
    if init:
        PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)

    random_text_string = "xxxxxx"

    with open(PATH_TO_BLOG/"index.html", "w") as f:
        f.write(random_text_string)
    
    if update:
        update_blog(PATH_TO_BLOG_REPO)
    

    # Path('https://tomxdi.github.io/')





if __name__ == "__main__":
    logging.set_verbosity(logging.INFO)

    err = app.run(main)  # parse absl flags   
    if err:
        sys.exit(f"ERROR: {err}")     

    print("\nSUCCESS!")    

