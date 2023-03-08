#!/usr/bin/env python

# conda install -y -c conda-forge gitpython
# conda install -y -c conda-forge openai
# conda install -y -c conda-forge beautifulsoup4  # html parser
# OPENAI_API_KEY=
# Web page at 'https://tomxdi.github.io/'

import os
from pathlib import Path
import shutil
import datetime

import openai
from git import Repo
from bs4 import BeautifulSoup as soup

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
flags.DEFINE_string("topic", "Bike Riding", "Specify the blog topic")
#flags.DEFINE_bool("show", True, "Show files included zipfile")

def f():
    with open(


def update_blog(repo_path, commit_message="Update blog"):
    print(f"Update blog repo {repo_path}")  

    repo = Repo(repo_path)

    # git add .
    repo.git.add(all=True)
    # git commit -m "msg"
    repo.index.commit(commit_message)
    # git push
    origin = repo.remote(name='origin')
    origin.push()

def create_new_blog(title, content, content_path, cover_image_path):
    print(f"Create {title} blog: {content}")

    if cover_image_path:
        cover_image=Path(cover_image_path)        
        shutil.copy(cover_image, content_path)    

    num_existing_files = len(list(content_path.glob("*.html")))
    new_title = f"{num_existing_files+1}.html"
    path_to_new_content = content_path/new_title
    
    if os.path.exists(path_to_new_content):
        raise FileExistsError(f"File {path_to_new_content} already exists")
    
    with open(path_to_new_content, "w") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html>\n")
        f.write("<head>\n")
        f.write(f"<title> {title} </title>\n")
        f.write("</head>\n")
        
        f.write("<body>\n")
        f.write(f"<img src='{cover_image.name}' alt='Cover Image'> <br />\n")
        f.write(f"<h1> {title} </h1>")
        # Convert openai text response newlines with html breaks
        f.write(content.replace("\n", "<br />\n"))
        f.write("</body>\n")
        f.write("</html>\n")
        print("Blog created")
        return path_to_new_content

# absl needs argv
def main(argv):
    init = FLAGS.init
    update = FLAGS.update
    topic = FLAGS.topic    
    
    openai.api_key = os.getenv('OPENAI_API_KEY')

    PATH_TO_BLOG_REPO=Path('/home/tom/projects/github.com/tomxdi/tomxdi.github.io/.git')
    PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
    PATH_TO_CONTENT = PATH_TO_BLOG/"content"
    
    path_to_content = PATH_TO_CONTENT    
    path_to_content.mkdir(exist_ok=True, parents=True)

    title = topic
    content = str(datetime.datetime.now())
    cover_image_path = "OpenAI_Logo.svg"
    path_to_new_content = create_new_blog(title, content, path_to_content, cover_image_path)

    if update:
        update_blog(PATH_TO_BLOG_REPO)
    

if __name__ == "__main__":
    logging.set_verbosity(logging.INFO)

    err = app.run(main)  # parse absl flags   
    if err:
        sys.exit(f"ERROR: {err}")     

    print("\nSUCCESS!")    

