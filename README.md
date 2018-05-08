md-httpd ist a small web server that serves pages formatted using Markdown.
More specifically, these Markdown files are produced using MarkDrop and are
stored inside Dropbox.

Basically, I am quite happy with ~~Epistle~~ markDrop. But one thing annoyed
me: what to do with these nice Markdown files in my Dropbox folder? I could
convert them manually to HTML files (I did), but that was so ... manually.
Since I want to learn a little bit about Flask, I decided to spend some hours
to learn it by programming a web server that serves these files. Voila.

### Prerequisites

* Unix-like OS, e.g. Linux, OSX, ... (maybe it works on Windows too, but I
  tested it just on OSX)
* Python 2.6 (should work with Python 2.7)
* Flask
* Markdown2 

### Getting Started

* Install the required software
* Start the program: python mdhttpd.py
* Open your browser at http://127.0.0.1:28525
