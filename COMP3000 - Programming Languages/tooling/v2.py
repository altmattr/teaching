import argparse
import glob
import re
import os
from pathlib import Path
import yaml
import pandoc
import base64

top_matter = "abstract"

name_conversion = {"FAT": "Application Exercise",
                   "Fat": "Application Exercise",
                   "SSE": "Self Study Exercises"}

def split_at_regex_and_put_in_dictionary(input_string, regex):
    parts = re.split(re.compile(regex, re.MULTILINE), input_string)
    key = top_matter
    res = {}
    for part in parts:
        if re.match(regex, part):
            key = part.strip()
        else:
            if part.strip() != "":
              if not key in res:
                  res[key] = []
              res[key].append(part.strip())
    return {key: "\n".join(values) for key, values in res.items()}

def open_file(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return open(file_path, "w+")
def grab_the_data():
    parser = argparse.ArgumentParser(description="Tooling v2 script")
    parser.add_argument("-g", "--glob", type=str, required=False, help="Input file path", default="src/*.md")
    args = parser.parse_args()

    topics = {}
    for file in glob.glob(args.glob):
        print(file)
        # Add your processing logic here
        # For example, read the file, modify it, etc.
        with open(file, 'r') as f:
            content = f.read()
            venues = split_at_regex_and_put_in_dictionary(content, r"^(\s*#[^#].*)$")
            data = {}
            for key, value in venues.items():
                print(f"{key} -> {value[:10]}...")
                items = split_at_regex_and_put_in_dictionary(value, r"(\s*##[^#].*\n)")
                for item_key, item_value in items.items():
                    print(f"{key} -> {item_key} -> {item_value[:10]}...")
                data[key] = items
        topics[Path(file).stem] = data
    return topics

def inline_images(text):
    def lam(image):
        encoded_string = ""
        with open("src/" + image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string
    for res in re.findall(r'<img\s+(width=["\']([^"\']+)["\'])?\s*src=["\']([^"\']+)["\'][^>]*>', text):
        print(res)
        (full, width, image) = res
        with open("src/" + image, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        print(f"Found image: {image}: {encoded_string[:10]}...")
    return re.sub(r'<img\s+(width=["\']([^"\']+)["\'])?\s*src=["\']([^"\']+)["\'][^>]*>', 
                        lambda m: f"![embedded image](data:image/png;base64,{lam(m.group(3))})", 
                        text)

def perc2width(text):
    return re.sub(r'(\d+)%', lambda m: str(float(m.group(1))/100)+"\\textwidth", text) if text else "0.5\\textwidth"

def tex_images(text):        
    return re.sub(r'<img\s+(width=["\']([^"\']+)["\'])?\s*src=["\']([^"\']+)["\'][^>]*>', 
                  lambda m: "\n\n\\" + "includegraphics[width="+perc2width(m.group(2)) + "]{src/" + m.group(3) + "}\n\n", 
                  text)

def gift_to_gift(item,question, answers):
    print(f"gift_to_gift: {item}, {question[:10]}..., {[a[:10] for a in answers]}...")
    return f"::{item}::[markdown]\n{inline_images(question)}{{\n" + "\n".join([inline_images(answer) for answer in answers]) + "\n}\n"

def gift_to_tex(item, question, answers):
    question2 = pandoc.write(pandoc.read(question, format='markdown'), format='latex')
    answers = [pandoc.write(pandoc.read(answer, format='markdown'), format='latex') for answer in answers]
    return f"\\section{{{item}}}\n"+question2+"\n\\begin{{enumerate}}\n\\item" + "\n\\item".join(answers) + "\n\\end{enumerate}\n\n"

def gift_to_md(item, question, answers):
    return f"## {item}\n\n{inline_images(question)}\n\n  *" + "\n  *".join(answers) + "\n\n"

def yaml_to_tex(item, item_parsed, isTex=False):
    if not isTex:
        item     = pandoc.write(pandoc.read(item,                            format='markdown'), format="latex")
        question = pandoc.write(pandoc.read(tex_images(item_parsed.get('question', '')), format='markdown'), format="latex")
        answer   = pandoc.write(pandoc.read(tex_images(item_parsed.get('answer', ''  )), format='markdown'), format="latex")
    else:
        question = item_parsed.get('question', '')
        answer = item_parsed.get('answer', '')
    return f"\\section*{{{item}}}\n\n{question}\n\n\\subsection*{{Answer}}\n\n{answer}\n\n"

def yaml_to_xml(item, item_parsed, isTex=False):
    if isTex:
        item     = pandoc.write(pandoc.read(item,                            format='latex'), format='markdown')
        question = pandoc.write(pandoc.read(item_parsed.get('question', ''), format='latex'), format='markdown')
        answer   = pandoc.write(pandoc.read(item_parsed.get('answer', ''  ), format='latex'), format='markdown')
    else:
        question = item_parsed.get('question', '')
        answer = item_parsed.get('answer', '')
    return f"""<question type="essay">
                 <name>
                   <text>{item}</text>
                 </name>
                 <questiontext format="markdown">
                   <text><![CDATA[{question}]]></text>
                 </questiontext>
                 <generalfeedback format="markdown">
                   <text><![CDATA[{answer}]]></text>
                 </generalfeedback>
                 <defaultgrade>1.0000000</defaultgrade>
                 <penalty>0.0000000</penalty>
                 <hidden>0</hidden>
                 <idnumber></idnumber>
                 <responseformat>editor</responseformat>
                 <responserequired>1</responserequired>
                 <responsefieldlines>25</responsefieldlines>
                 <minwordlimit></minwordlimit>
                 <maxwordlimit></maxwordlimit>
                 <attachments>0</attachments>
                 <attachmentsrequired>0</attachmentsrequired>
                 <maxbytes>0</maxbytes>
                 <filetypeslist></filetypeslist>
                 <graderinfo format="html">
                   <text></text>
                 </graderinfo>
                 <responsetemplate format="html">
                   <text></text>
                 </responsetemplate>
               </question>"""

def yaml_to_md(item, item_parsed, isTex=False):
    if isTex:
        item     = pandoc.write(pandoc.read(item,                            format='latex'), format='markdown')
        question = pandoc.write(pandoc.read(item_parsed.get('question', ''), format='latex'), format='markdown')
        answer   = pandoc.write(pandoc.read(item_parsed.get('answer', ''  ), format='latex'), format='markdown')
    else:
        question = item_parsed.get('question', '')
        answer = item_parsed.get('answer', '')
    return f"## {item}\n\n{question}\n\n**Answer:**\n\n{answer}\n\n"

def tex_topmatter(file, topic):
    file.write("""\\documentclass[twoside=false, DIV=14]{scrartcl}
                  \\input{latex_setup.tex}
                  \\title{\color{redish} \\vspace{-1em}COMP3000: """ + topic + """}

                  \\begin{document}
                    {\\color{blackish}\\maketitle}\\vspace{-7em}""")


def tex_bottommatter(file):
    file.write("\\end{document}\n")

if __name__ == "__main__":
    topics = grab_the_data()

    for topic, topic_data in topics.items():
        print(f"processing topic: {topic}")
        clean_topic = re.sub(r"<.*>", "", re.sub(r"[^a-zA-Z0-9_]", "", topic))

        # topic has the following files:
        #  * topic.gift
        #  * topic.xml
        #  * topic_all.tex
        #  * topic_all.md
        with (
            open_file(f"build/{topic}/{topic}.gift")    as gift,
            open_file(f"build/{topic}/{topic}.xml")     as xml,
            open_file(f"build/{topic}/{topic}_all.tex") as all_tex,
            open_file(f"build/{topic}/{topic}_all.md")  as all_md
            ): 
              tex_topmatter(all_tex, clean_topic.replace("_", " "))
              xml.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?><quiz>")
              for (venue, venue_data) in topic_data.items():
                # venue has the following files:
                #  * topic_venue.tex
                #  * topic_venue.md
                cleanish_venue = re.sub(r"<.*>", "", re.sub(r"[^a-zA-Z0-9_]", "", venue)).strip()
                clean_venue = re.sub(r"<.*>", "", re.sub(r"[^a-zA-Z0-9_]", "", venue)).strip()
                print(f"  processing venue: {clean_venue}")
                if clean_venue in name_conversion:
                    clean_venue = name_conversion[clean_venue]
                if not venue == top_matter:
                    all_tex.write(f"\\newpage\n\\part*{{{clean_venue}}}\n")
                print(f"  processing venue: {clean_venue}")
                with (
                    open_file(f"build/{topic}/{cleanish_venue}.tex") as venue_tex,
                    open_file(f"build/{topic}/{cleanish_venue}.md") as venue_md
                ):
                  tex_topmatter(venue_tex, clean_topic.replace("_", " ") +r" $\rightarrow$ " + clean_venue)
                  for (item, item_data) in venue_data.items():
                    item_type = re.search(r"<(.*)>", item).group(1) if re.search(r"<(.*)>", item) else "nil"
                    clean_item = re.sub(r"[^a-zA-Z0-9_ ]", "", re.sub(r"<.*>", "", item)).strip()
                    if item_type == "gift":
                      print("this item data is")
                      print(item_data)
                      question, rest = re.split(r"(?<!\\){", item_data)
                      answers = re.findall(r"([=~].*)", rest)
                      # write all the files
                      gift.write(f"\n\n$CATEGORY: {clean_topic}/{clean_venue}\n\n")  # will get more than I need, but also won't get the surplus ones, so it is a win in my book
                      # TODO: write gift files to xml as well - then you can turf the gift format entirely
                      gift.write(gift_to_gift(clean_item,question,answers))
                      all_tex.write(gift_to_tex(clean_item, question, answers))
                      venue_tex.write(gift_to_tex(clean_item, question, answers))
                      all_md.write(gift_to_md(clean_item, question, answers))
                      venue_md.write(gift_to_md(clean_item, question, answers))
                    elif item_type == "essay" or item_type == "tex-essay":
                      isTex = True if item_type == "tex-essay" else False
                      item_parsed = yaml.safe_load(item_data)
                      # write all the files
                      xml.write(f"<question type=\"category\"><category><text>{clean_topic}/{clean_venue}</text></category><info format=\"html\"><text></text></info><idnumber></idnumber></question>")
                      xml.write(yaml_to_xml(clean_item, item_parsed, isTex))
                      all_tex.write(yaml_to_tex(clean_item, item_parsed, isTex))
                      venue_tex.write(yaml_to_tex(clean_item, item_parsed, isTex))
                      all_md.write(yaml_to_md(clean_item, item_parsed, isTex))
                      venue_md.write(yaml_to_md(clean_item, item_parsed, isTex))
                    else:
                      all_md.write(f"## {clean_item}\n\n{item_data}\n\n")
                      venue_md.write(f"# {clean_item}\n\n{item_data}\n\n")
                  tex_bottommatter(venue_tex)
                os.system(f"latexmk -pdf -interaction=nonstopmode -output-directory=build/{topic} build/{topic}/{cleanish_venue}.tex > /dev/null")
              tex_bottommatter(all_tex)
              xml.write("</quiz>")
        os.system(f"latexmk -pdf -interaction=nonstopmode -output-directory=build/{topic} build/{topic}/{topic}_all.tex > /dev/null")