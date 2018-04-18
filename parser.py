# -*- coding: utf-8 -*-

from __future__ import print_function
import fileinput
import os
import re

def prs(file, id_list):
    tag = '[Tags]'
    super_tag = 'ps-qcc-used'
    another_tag = 'ps_qcc_used'

    appended_tag = '    ' + super_tag + '\n'
    i = 0
    for line in fileinput.FileInput(file, inplace=True):
        if line.find(tag) > -1 and line.find(super_tag) == -1 and line.find(another_tag) == -1:
            start = line.find('testrailid=') + 11
            end = line.find(' ', start)
            testrail_id = line[start:end]
            if testrail_id in id_list:
                line = line[:-1] + appended_tag
                i += 1
        print(line, end='')
    return i

def parser(file):
    i = 0
    tag = '[Tags]'
    super_tag = 'ps-qcc-used'
    appended_tag = '    ' + super_tag + '\r\n'

    with open(file, 'r+') as f:
        for line in f:
            if line.find(tag) > -1 and line.find(super_tag) == -1:
                start = line.find('testrailid=') + 10
                end = line.find(' ', start)
                testrail_id = line[start:end]
                i += 1
                new_line = line[:-1] + appended_tag
                print(line)
                line = line.replace(line, new_line)
    return i

def table(file):
    with open(file) as f:
        list = []
        number = ''
        for line in f:
            for l in line:
                if l != ";":
                    number = number + l
                else:
                    list.append(number)
                    number = ''
                    break
    return list

def files(root_dir):
    rx = re.compile(r'\.(robot)')
    r = []
    for path, dnames, fnames in os.walk(root_dir):
        r.extend([os.path.join(path, x) for x in fnames if rx.search(x)])
    ret = []
    for a in r:
        a = a.replace('\\', '/')
        ret.append(a)
    return ret


file_list = files('C:/TORS')

for i in file_list:
    print(i)



id_list = table('table.csv')

parsing_success = 0        #сСколько раз был вставлен тег

for f in file_list:
    parsing_success = parsing_success + prs(f, id_list)

print('parsing_success  ', parsing_success)


