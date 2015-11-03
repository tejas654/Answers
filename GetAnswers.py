import re
import os
import csv
from pydocx import PyDocX
import shutil
import codecs


def _main_(tournament):
    os.chdir('C:\School\Quiz Bowl\Quizbowl Packets\\' + tournament)
    files = os.listdir(os.curdir)
    q = open(tournament + ' answers.csv', 'w')
    writer = csv.DictWriter(q, fieldnames=['Full Answer', 'Underlined Answer', 'Tournament', 'Packet'],
                            lineterminator='\n')
    writer.writeheader()
    for f in files:
        html = PyDocX.to_html(f).decode('Windows-1252').encode('utf-8')
        html = clean_file(html)
        answers = re.findall(r'ANSWER: (?P<id>.*?)(?:</li>|<br />|</p>)', html)
        und = []
        for a in answers:
            underlined = re.findall(r'<span class=\"pydocx-underline\">(?P<id>.*?)</span>', a)
            output = ""
            for u in underlined:
                output += ' ' + u.strip()
            und.append(output.strip())

        for i in range(0, len(answers)):
            answer = re.sub(r'<[^>]*>', '', answers[i]).strip()
            writer.writerow({'Full Answer': answer.encode('utf-8'), 'Underlined Answer': und[i].encode('utf-8'),
                            'Tournament': tournament, 'Packet': f})
    q.close()
    shutil.copy(tournament + ' answers.csv', 'C:\School\Quiz Bowl\Stats\Answers')
    os.remove(tournament + ' answers.csv')


def clean_file(text):
    text = re.sub(r'<em>|</em>|<strong>|</strong>|\[[^\]]*\]|\([^\)]*\)|&lt;[^&]*&gt;', '', text)
    text = re.sub(r'\xe0|\xe1|\xe2|\xe3|\xe4|\xe5', 'a', text)
    text = re.sub(r'\xe6', 'ae', text)
    text = re.sub(r'\xe7', 'c', text)
    text = re.sub(r'\xe8|\xe9|\xea|\xeb', 'e', text)
    text = re.sub(r'\xec|\xed|\xee|\xef', 'i', text)
    text = re.sub(r'\xf0', 'd', text)
    text = re.sub(r'\xf1', 'n', text)
    text = re.sub(r'\xf2|\xf3|\xf4|\xf5|\xf6|\xf8', 'o', text)
    text = re.sub(r'\xf9|\xfa|\xfb|\xfc', 'u', text)
    text = re.sub(r'\x22', '\"', text)
    text = re.sub(r'\x27', '\'', text)
    return text


def combine_tournaments():
    os.chdir('C:\School\Quiz Bowl\Stats\Answers')
    files = os.listdir(os.curdir)
    q = open('All Answers.csv', 'w')
    writer = csv.DictWriter(q, fieldnames=['Full Answer', 'Underlined Answer', 'Tournament', 'Packet'],
                            lineterminator='\n')
    writer.writeheader()
    for f in files:
        with open(f, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                writer.writerow({'Full Answer': row[0], 'Underlined Answer': row[1], 'Tournament': row[2],
                                'Packet': row[3]})

set = 'Penn Bowl 2014'
_main_(set)
#combine_tournaments()

