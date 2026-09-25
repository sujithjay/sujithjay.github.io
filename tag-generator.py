#!/usr/bin/env python

'''
tag_generator.py

Copyright 2017 Long Qian
Contact: lqian8@jhu.edu

This script creates tags for your Jekyll blog hosted by Github page.
No plugins required.
'''

import glob
import os

post_dir = '_posts/'
tag_dir = 'tag/'

filenames = glob.glob(post_dir + '*md')

total_tags = []
for filename in filenames:
    f = open(filename, 'r')
    crawl = False
    for line in f:
        if crawl:
            current_tags = line.strip().split()
            if current_tags[0] == 'tags:':
                total_tags.extend(current_tags[1:])
                crawl = False
                break
        if line.strip() == '---':
            if not crawl:
                crawl = True
            else:
                crawl = False
                break
    f.close()
total_tags = set(total_tags)

# Existing tag pages are left as they are, because some carry redirect_from
# entries for retired tags that were merged into them. Only pages for tags
# no post uses any more are removed, and only missing pages are created.
for tag_filename in glob.glob(tag_dir + '*.md'):
    tag = os.path.basename(tag_filename)[:-len('.md')]
    if tag not in total_tags:
        os.remove(tag_filename)
        print("Removed unused tag page", tag)

for tag in total_tags:
    tag_filename = tag_dir + tag + '.md'
    if os.path.exists(tag_filename):
        continue
    f = open(tag_filename, 'w')
    write_str = '---\nlayout: tagpage\ntitle: \"Tag: ' + tag + '\"\ntag: ' + tag + '\nrobots: noindex\nsitemap: false\n---\n'
    f.write(write_str)
    f.close()
    print("Created tag page", tag)
print("Tags in use, count", total_tags.__len__())