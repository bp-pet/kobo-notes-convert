"""
Exporting annotations from '.annot' file (xml format) through pandas to html table.
Annotation is the whole object, target is the text it annotates, content is the actual
added annotation (if present).
"""

import pandas as pd
from bs4 import BeautifulSoup

with open('dict.xml', 'r', encoding='utf-8') as f:
    data = f.read()
Bs_data = BeautifulSoup(data, "xml")

print(Bs_data)

annotations = Bs_data.find_all('annotation')

summary_df = pd.DataFrame(columns=["target", "content"])

for b in annotations:
    target = b.find('target')
    content = b.find('content')
    target_text = b.find('text').text
    if content is not None:
        content_text = content.find('text').text
    else:
        content_text = None

    to_be_added_dict = {"target": [target_text], "content": [content_text]}
    summary_df = pd.concat([summary_df, pd.DataFrame.from_dict(to_be_added_dict)])
summary_df.reset_index(inplace=True, drop=True)

# rename columns
summary_df = summary_df.rename(columns={"target": "Text", "content": "Annotation"})

# to html
summary_html = summary_df.to_html()

# add header
with open("header.txt", 'r') as f:
    header = f.read()
summary_html = header + "\n\n" + summary_html

# remove none
summary_html = summary_html.replace("None", "")


with open("output.html", 'w') as f:
    f.write(summary_html)