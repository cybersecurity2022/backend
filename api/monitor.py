import difflib
import os
import pickle
import pandas as pd
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends
import requests

# from model.Predictions import detect_defacement
from models import User
from schemas.users import url_in_json
from utils import get_current_user

monitor_router = APIRouter(prefix="/monitor", tags=['Monitor'])

dist_path = os.path.join(os.getcwd(), 'scraped_pages')


class Update:
    def __init__(self):
        self.old = 0
        self.coun = 1

    def update_old(self, val):
        self.old = val

    def update_coun(self, val):
        self.coun = val

    def counter(self):
        self.coun = self.coun + 1
        if self.coun >= 3:
            self.update_old(self.old + 1)


# if user already exit
glob_obj = Update()

# store the counters for a register user to track the scraped files
recorde = {}


def show_diff(seqm):
    """Unify operations between two compared strings
seqm is a difflib.SequenceMatcher instance whose a & b are strings"""
    output = []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append("<ins>" + seqm.b[b0:b1] + "</ins>")
            # output.append('<span style = "color:blue" >'+ seqm.b[b0:b1] + '< / span >')
        elif opcode == 'delete':
            output.append("<del>" + seqm.a[a0:a1] + "</del>")
            # output.append('<span style = "color:red" >'+ seqm.a[a0:a1] + '< / span >')
        elif opcode == 'replace':
            pass
        else:
            raise RuntimeError("unexpected opcode")
    return ''.join(output)


@monitor_router.post("/scrape", description="place web page url")
def scrap_page(url:str, current_user: User = Depends(get_current_user)):
    global recorde
    global detect
    result = requests.get(url)
    content = result.text

    soup = BeautifulSoup(content, "html.parser")
    # full website scrape
    # with open("website.html", 'w') as file:
    #     file.write(soup.prettify())

    """
        save complete html of the scraping website on the scraped_pages directory
    """

    if not os.path.exists(dist_path):
        os.makedirs(dist_path)

    dist_pat = f'{dist_path}/{current_user.user_name}'
    if not os.path.exists(f'{dist_pat}'):
        # re instantiation of object for new user to assemble the old and next counter
        glob_obj.coun = 1
        glob_obj.old = 0
        os.makedirs(f'{dist_pat}')
        # create json file to track user files
        open(f"{dist_pat}/track_{current_user.user_name}_file.json", "wb")
    else:
        # load the tracker if session is regenerated
        if glob_obj.coun == 1:
            session = "new"
            with open(f"{dist_pat}/track_{current_user.user_name}_file.json", "rb") as json:
                data = pickle.load(json)
                glob_obj.update_old(data["old"] + 1)
                glob_obj.update_coun(data["coun"] + 1)

    # if session is "old":
    if not os.path.exists(f'{dist_pat}/ textFile{glob_obj.coun}.txt'):
        with open(f"{dist_pat}/textFile{glob_obj.coun}.txt", 'w') as file:
            file.write(soup.get_text())
        with open(f"{dist_pat}/htmlFile{glob_obj.coun}.html", 'w') as file:
            file.write(soup.prettify())
        if glob_obj.coun >= 3:
            os.remove(f'{dist_pat}/htmlFile{glob_obj.old}.html')
            os.remove(f'{dist_pat}/textFile{glob_obj.old}.txt')

        if glob_obj.coun >= 2:
            first_file = open(f"{dist_pat}/htmlFile{glob_obj.coun - 1}.html", "r")
            second_file = open(f"{dist_pat}/htmlFile{glob_obj.coun}.html", "r")

            sm = difflib.SequenceMatcher(None, first_file.read(), second_file.read())
            with open(f"{dist_pat}/highlited.html", 'w') as file:
                file.write(show_diff(sm))

            first_file_txt = f"{dist_pat}/textFile{glob_obj.coun - 1}.txt"
            second_file_txt = f"{dist_pat}/textFile{glob_obj.coun}.txt"

            first_file_lines = open(first_file_txt).readlines()
            second_file_lines = open(second_file_txt).readlines()
            """
                Changes
            """
            difference = difflib.HtmlDiff().make_file(first_file_lines, second_file_lines, first_file_txt,
                                                      second_file_txt)
            difference_report = open(f"{dist_pat}/text_difference_report.html", "w")
            difference_report.write(difference)
            difference_report.close()

            soup = BeautifulSoup(difference, "html.parser")
            with open("website.html", 'w') as file:
                file.write(soup.prettify())

            added_text = []
            for text in soup.find_all(class_="diff_add"):
                added_text.append(text.get_text())

            with open(f"{dist_pat}/addedtext_change.txt", mode="w", ) as file:
                file.write(str(added_text).replace("\\xa0", ""))
            if os.path.exists(f"{dist_pat}/addedtext_change.txt"):
                """
                    Newly Added text is
                """
                pd.DataFrame(added_text).to_csv("model/data.csv", index=False)

                # detect = detect_defacement()

    # save the tracker of the file
    with open(f"{dist_pat}/track_{current_user.user_name}_file.json", "wb") as json:
        recorde["old"] = glob_obj.old
        recorde["coun"] = (glob_obj.coun)
        pickle.dump(recorde, json)

    glob_obj.counter()
    # if detect:
    #     return {"this is defacement"}
    # else:
    #     return "scrap another"
    return "scrap another"


# monitor_router.get('/defacement_check')
# def check():
#     detect = detect_defacement()
#     if detect:
#         return "yes"
#     else:
#         return "no"