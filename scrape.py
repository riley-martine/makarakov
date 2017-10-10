from bs4 import BeautifulSoup
import pickle
import os
import re

if not os.path.isfile("all.pickle"):
    with open("archive.html", 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')


    exp = re.compile("\[...?.?\]")
    def find_span(tag):
        return tag.name == "span" and tag.parent.name == "section" and not exp.search(str(tag.contents))
    def find_log(tag):
        return tag.name == "div" and (tag.button and tag.button.string in ["pesterlog", "sriousbiz", "dialoglog", "spritelog"]) or (not tag.button and 'class' in tag and tag['class'] == "log") 

   # b = []
   # for div in soup.find_all(lambda t: t.name == "div" and t.button):
   #     if div.button.string not in b:
   #         b.append(div.button.string)
   # print(b)

    logs = soup.find_all(find_log)
    pages = [list(map(lambda s:s.contents, span)) for span in [log.section.find_all(find_span) for log in logs]]

    all = []
    for page in pages:
       for message in page:
          if len(message) == 1 and str(message[0])[0] != '[':
              all.append(message[0])

    all = list(map(str, all))
    with open("all.pickle", 'wb') as f:
        pickle.dump(all, f)
else:
    with open("all.pickle", 'rb') as f:
        all = pickle.load(f)

handles = []
for line in all:
    split = line.split(":")
    if len(split) > 1:
       handle = split[0]
       if handle not in handles:
           handles.append(handle)

# Cleanup
for handle in handles:
    if handle[0] in ['*', '<', " ", '(']:
        handles.remove(handle)
for handle in handles:
    if '!' in handle:
        handles.remove(handle)
handles.remove("(JOHN)")

split = [line.split(":") for line in all]
split = (filter(lambda x: x[0] in handles, split))
split = (filter(lambda x: len(x) > 1, split))
def f(x):
    i = []
    i.append(x[0])
    i.append(''.join(x[1:]))
    return i
split = map(f, split)
split = map(lambda x: [x[0], x[1].strip()], split)

handle_map = {}
for line in split:
    if line[0] not in handle_map:
        handle_map[line[0]] = []
    handle_map[line[0]].append(line[1])

for handle in sorted(handles):
    print(handle)

print(handle_map['TG'][0:10])
