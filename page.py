# -*- coding: utf-8 -*-

class Paragraph:
    '''
    Describe a paragraph
    '''
    def __init__(self, *, lv='p', cont=''):
        self.level = lv
        self.content = cont

class Page:
    '''
    Describe a slide page
    '''
    def __init__(self):
        self.paras = []

