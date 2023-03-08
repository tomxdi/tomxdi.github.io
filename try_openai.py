#!/usr/bin/env python

# conda install -y -c conda-forge gitpython
# conda install -y -c conda-forge openai
# conda install -y -c conda-forge beautifulsoup4  # html parser
# OPENAI_API_KEY=
# Web page at 'https://tomxdi.github.io/'

import os
import sys
from pathlib import Path
import shutil
import datetime

import openai
from git import Repo
from bs4 import BeautifulSoup as Soup  # HTML parser

from absl import app
from absl import flags
from absl import logging
from absl.logging import PythonFormatter

FLAGS = flags.FLAGS
flags.DEFINE_string("path_to_blog_repo", "/home/tom/projects/github.com/tomxdi/tomxdi.github.io/.git", "Specify the blog's git repo location")
flags.DEFINE_string("topic", "Bike Riding", "Specify the blog topic")
flags.DEFINE_bool("publish", False, "Publish by pushing to the git repo")
# flags.DEFINE_bool("init", False, "Do any one time initialization")

def check_for_duplicate_links(path_to_new_content, links):
        urls = [str(link.get("href")) for link in links]    # [1.html,2.html,..]
        content_path= str(Path(*path_to_new_content.parts[-2:]))
        return content_path in urls

def update_index(index_path, path_to_new_content):
    print(f"index_path={index_path}")
    print(f"path_to_new_content={path_to_new_content}")

    with open(index_path) as index:
        soup =Soup(index.read(), features="html.parser")
        #print(str(soup))

    # Fetch all anchor links
    links = soup.find_all('a')
    #print(links)
    last_link = links[-1]

    if check_for_duplicate_links(path_to_new_content, links):
        raise ValueError(f"Link {path_to_new_content} already exists")

    link_to_new_blog = soup.new_tag("a", href=Path(*path_to_new_content.parts[-2:]))
    # print(f"{Path(*path_to_new_content.parts[-2:])}")  # content/10.html
    # print(f"link_to_new_blog={link_to_new_blog}")      # <a href="content/11.html"></a>

    # path.name() is like basename() (filename w/o path elements)
    link_to_new_blog.string = path_to_new_content.name.split('.')[0]   # 11
    # print(f"link_to_new_blog={link_to_new_blog}")      # <a href="content/11.html">11</a>

    last_link.insert_after(link_to_new_blog)

    with open(index_path, "w") as index:
        index.write(str(soup.prettify(formatter='html')))

def publish_content(repo_path, commit_message="Update blog"):
    print(f"Update blog repo {repo_path}")  

    repo = Repo(repo_path)

    # git add .
    repo.git.add(all=True)
    # git commit -m "msg"
    repo.index.commit(commit_message)
    # git push
    origin = repo.remote(name='origin')
    origin.push()

def create_new_content(title, content_image_path, content, content_dir):
    print(f"Create {title} blog: {content}")

    content_image=Path(content_image_path)        
    shutil.copy(content_image, content_dir)    

    num_existing_files = len(list(content_dir.glob("*.html")))
    new_title = f"{num_existing_files+1}.html"
    path_to_new_content = content_dir/new_title
    
    if os.path.exists(path_to_new_content):
        raise FileExistsError(f"File {path_to_new_content} already exists")
    
    with open(path_to_new_content, "w") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html>\n")
        f.write("<head>\n")
        f.write(f"<title> {title} </title>\n")
        f.write("</head>\n")
        
        f.write("<body>\n")
        f.write(f"<img src='{content_image.name}' alt='Content Image'> <br />\n")
        f.write(f"<h1> {title} </h1>")
        # Convert openai text response newlines with html breaks
        f.write(content.replace("\n", "<br />\n"))
        f.write("</body>\n")
        f.write("</html>\n")
        print("Blog created")
    
    return path_to_new_content



# absl needs argv
def main(argv):
    topic = FLAGS.topic    
    publish = FLAGS.publish

    openai.api_key = os.getenv('OPENAI_API_KEY')

    path_to_blog_repo = Path(FLAGS.path_to_blog_repo)
    path_to_blog = path_to_blog_repo.parent
    path_to_index = path_to_blog/"index.html"
    content_dir = path_to_blog/"content"    
    content_dir.mkdir(exist_ok=True, parents=True)

    title = topic
    content_image = "OpenAI_Logo.svg"    
    content = str(datetime.datetime.now())
    path_to_new_content = create_new_content(title, content_image, content, content_dir)
    update_index(path_to_index, path_to_new_content)

    if publish:
        publish_content(path_to_blog_repo)

    

if __name__ == "__main__":
    logging.set_verbosity(logging.INFO)

    err = app.run(main)  # parse absl flags   
    if err:
        sys.exit(f"ERROR: {err}")     

    print("\nSUCCESS!")    

