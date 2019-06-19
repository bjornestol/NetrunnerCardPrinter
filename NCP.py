#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, requests, shutil, os

# Fetch NRDB api etc
nrdburl = "https://netrunnerdb.com/api/2.0/public/cards"
nrdb_card_api = requests.get(nrdburl).json()
imgdict = {}
for item in nrdb_card_api["data"]:
    name = item['title']
    if "image_url" in item:
        imgdict[name] = (item["image_url"], item["code"])
    else:
        imgdict[name] = ("https://netrunnerdb.com/card_image/{}.png".format(item["code"]), item["code"])



listOfCards = []
listOfCodes = []

with open("cards.txt", 'r') as f:
    for line in f:
        s = line.split()
        num = int(s[0])
        name = " ".join(s[1:])
        listOfCards.append((name, num))

for name, num in listOfCards:
    (img, code) = imgdict[name]
    response = requests.get(img, stream=True)
    with open("{}.png".format(code), 'wb') as f:
        shutil.copyfileobj(response.raw, f)
    for i in range(num):
        listOfCodes.append(code)




# Create LaTeX doc here

texdoc = """\documentclass[a4paper]{article}
\usepackage[margin=0.5in]{geometry}
\usepackage{graphicx}
\\begin{document}
\pagestyle{empty}
\\noindent
"""

imgstr = "\includegraphics[height=89mm]{{{0}}}\hspace{{-1mm}}\n"

for code in listOfCodes:
    texdoc += imgstr.format(code)

texdoc += "\end{document}"

with open("NCP.tex", "w+") as f:
    f.write(texdoc)

os.system("pdflatex NCP.tex")
