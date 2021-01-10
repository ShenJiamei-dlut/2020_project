# -*- coding: utf-8 -*-

import sys, logging
import page

def error(errStr):
    logging.error(errStr)
    sys.exit(1)

class Section:
    '''
    Store section structure
    '''
    def __init__(self):
        self.pages = []

class Document:
    """
    Store data of a whole file
    """
    def __init__(self):
        self.sections = []
        self.title = ''
        self.author = ''
        self.date = ''

    # Add a paragraph to the page
    def addPara(self, paraStr, pg):
        if paraStr.startswith('# '):
            paraStr = paraStr[2:]
            logging.info('Found top title: ' + paraStr)
            # Multiple top title
            if '' != self.title:
                error('Only one top title is allowed!')
            self.title = paraStr
            para = page.Paragraph(lv='h1', cont=paraStr)
        elif paraStr.startswith('## '):
            paraStr = paraStr[3:]
            logging.info('Found sub title: ' + paraStr)
            para = page.Paragraph(lv='h2', cont=paraStr)
        elif paraStr.startswith('### '):
            paraStr = paraStr[4:]
            logging.info('Found third title: ' + paraStr)
            para = page.Paragraph(lv='h3', cont=paraStr)
        elif paraStr.startswith('- '):
            logging.info('Found an unordered list')
            para = page.Paragraph(lv='ul', cont=paraStr)
        elif paraStr.startswith('1. '):
            logging.info('Found an ordered list')
            para = page.Paragraph(lv='ol', cont=paraStr)
        elif paraStr.startswith('```'):
            paraStr = paraStr.split('\n', 1)[1]
            paraStr = paraStr.replace('\n```', '')
            logging.info('Found a code block')
            para = page.Paragraph(lv='cb', cont=paraStr)
        else:
            logging.info('Found a normal paragraph')
            para = page.Paragraph(lv='p',
                    cont=paraStr.replace('\n', ' '))
        # Lack top title
        if '' == self.title:
            error('A top title is needed before any!')
        pg.paras.append(para)

    def addPage(self, pg):
        logging.info('Adding new page')
        self.sections[-1].pages.append(pg)

    def addSec(self):
        logging.info('Adding new section')
        self.sections.append(Section())

    # Read from file
    def readFile(self, fileName):
        # Read data from file
        with open(fileName, 'r') as f:
            lines = f.readlines()
            paraStr = ''
            pg = page.Page()
            for line in lines:
                # Para break
                line = line.strip()
                if '' == line:
                    if '' != paraStr:
                        self.addPara(paraStr, pg)
                        paraStr = ''

                # Page break <- Manully
                elif line.startswith('---'):
                    logging.info('Page break')
                    if 0 != len(pg.paras):
                        self.addPage(pg)
                    paraStr = ''
                    pg = page.Page()

                # Page break <- Automatically
                elif line.startswith('# ') or line.startswith('## '):
                    logging.info('Page break')
                    if 0 != len(pg.paras):
                        self.addPage(pg)
                    self.addSec()
                    pg = page.Page()
                    self.addPara(line, pg)
                    paraStr = ''

                # Author
                elif line.startswith(r'%author: '):
                    line = line[9:]
                    logging.info('Found author: ' + line)
                    self.author = line

                # Date
                elif line.startswith(r'%date: '):
                    line = line[7:]
                    logging.info('Found date: ' + line)
                    self.date = line

                else:
                    if '' != paraStr:
                        paraStr += '\n'
                    paraStr += line

            if 0 != len(pg.paras):
                self.addPage(pg)

# Test
if '__main__' == __name__:
    logging.basicConfig(level=logging.DEBUG)
    doc = Document()
    doc.readFile('pypt.md')
    for sec in doc.sections:
        for pg in sec.pages:
            for para in pg.paras:
                pass

