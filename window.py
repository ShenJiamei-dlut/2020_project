# -*- coding: utf-8 -*-

import logging as log
import tkinter as tk
import tkinter.messagebox as msgbox
import webbrowser as web
import config, page, document

# Executed directly
if '__main__' == __name__:
    log.error('This file should not be executed directly!')

# Window class inherited from Frame
class Window(tk.Frame):
    '''
    Defined as a single page window
    '''
    # Constructor
    def __init__(self, doc, theme, master=None):
        # Parent constructor
        tk.Frame.__init__(self, master, bg='#252525')
        log.info('Parent window created')
        self.pack(expand='yes', fill='both')
        log.info('Main frame packed')
        # Load document and theme
        self.doc = doc
        self.theme = theme
        self.row = 0
        self.column = 0
        # Register key bindings
        bindedKeys = ['<Escape>', '<q>',
                '<h>', '<j>', '<k>', '<l>',
                '<Left>', '<Down>', '<Up>', '<Right>',
                'o']
        for seq in bindedKeys:
            self.master.bind(sequence=seq, func=self.eventHandler)
        log.info('Key bindings applied')
        # Initialize
        log.info('Initializing widgets...')
        self.initWidgets()
        # Refresh page
        log.info('Loading page...')
        self.update()
        self.loadPage()

    # Initialize widgets
    def initWidgets(self):
        # Set window attributes
        self.master.title('PyPt - ' + self.doc.title)
        # Window geometry
        width = 1024
        height = 600
        scrwid = self.master.winfo_screenwidth()
        scrhgt = self.master.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height,
                (scrwid-width)/2, (scrhgt-height)/2)
        self.master.geometry(geometry)
       # Top label
        self.labelTop = tk.Label(self,
                text=self.doc.title + ' - ' + self.doc.date,
                font=self.theme['p'],
                fg='white', bg='#252525',
                height=1)
        self.labelTop.pack(side='top', expand='no', fill='both')
        # Bottom label
        self.textBottom = tk.StringVar()
        self.textBottom.set (self.doc.author + ' - <0,0>')
        self.labelBottom = tk.Label(self,
                textvariable=self.textBottom,
                font=self.theme['p'],
                fg='white', bg='#252525',
                height=1)
        self.labelBottom.pack(side='bottom', expand='no', fill='both')
        log.info('Topbar & bottombar created')
        # Content text
        self.textField = tk.Text(self,
                fg='white', bg='#252525', bd=0,
                autoseparators=False)
        self.textField.pack(expand='yes')
        self.textField.config(state='disabled')
        log.info('Text field created')
        # Load tag config
        log.info('Applying font config...')
        for key, value in config.Config.theme.items():
            self.textField.tag_config(key,
                    font=value,
                    wrap='word')
        for heading in ('h1', 'h2', 'h3'):
            self.textField.tag_config(heading, justify='center')
        for listing in ('ol', 'ul'):
            self.textField.tag_config(listing,
                    font=config.Config.theme['p'],
                    lmargin1=128, lmargin2=160)
        for underlined in ('ln', ):
            self.textField.tag_config(underlined,
                    foreground='blue', underline=True)
        # Tag bindings
        log.info('Applying link format...')
        self.textField.tag_bind('ln', '<Enter>',
                lambda e: self.textField.config(cursor='hand1'))
        self.textField.tag_bind('ln', '<Leave>',
                lambda e: self.textField.config(cursor=''))

    def loadPage(self):
        # Update page number
        self.textBottom.set (self.doc.author
                + ' - <' + str(self.column) + ',' + str(self.row) + '>')
        # Enable text widget
        field = self.textField
        field.config(state='normal')
        page = self.doc.sections[self.column].pages[self.row]
        # Clear current content
        field.delete('1.0', 'end')
        log.info('Text field cleared')
        # Draw
        for para in page.paras:
            begin = field.index('insert')
            field.insert('insert', '\n'+para.content+'\n')
            end = field.index('insert')
            if 'h1' == para.level:
                field.tag_add('h1', begin, end)
            elif 'h2' == para.level:
                field.tag_add('h2', begin, end)
            elif 'h3' == para.level:
                field.tag_add('h3', begin, end)
            elif 'cb' == para.level:
                field.tag_add('cb', begin, end)
            elif 'ol' == para.level:
                field.tag_add('ol', begin, end)
            elif 'ul' == para.level:
                field.tag_add('ul', begin, end)
            else:
                field.tag_add('p', begin, end)
                # Apply bold, italic, bolditalic, code
                for thm, sign in {
                        'bdit': '***', 'bd': '**', 'it': '*', 'cb': '`'
                        }.items():
                    # Search matched
                    left = field.search(sign, begin, 'end')
                    while left:
                        for _ in sign:
                            field.delete(left)
                        right = field.search(sign, left, 'end')
                        field.tag_add(thm, left, right)
                        for _ in sign:
                            field.delete(right)
                        # Search next
                        left = field.search(sign, right, 'end')
                # Support links
                left = field.search('[', begin, 'end')
                while left:
                    field.delete(left)
                    # Search `](`
                    right = field.search('](', left, 'end')
                    field.delete(right)
                    field.delete(right)
                    field.tag_add('ln', left, right)
                    link = field.get(left, right) # Link name
                    left = right
                    # Search `)`
                    right = field.search(')', left, 'end')
                    address = field.get(left, right) # Link address
                    log.info('Found link: ' + link + ': ' + address)
                    for _ in address:
                        field.delete(left)
                    # Note link and address
                    field.insert('insert', '\n'+link+' -> '+address+'\n')
                    # Search next `[`
                    left = field.search('[', left, 'end')
        log.info('Text field updated')
        # Disable text widget
        field.config(state='disabled')

    # Event handler
    def eventHandler(self, event):
        key = event.keysym
        log.info('Key <' + key + '> Pressed.')
        # Terminate
        if 'Escape' == key or 'q' == key:
            if 'yes' == msgbox.askquestion('Info',
                    'Terminate slide show?'):
                log.info('Destroying window...')
                self.master.destroy()
        # Navigate
        elif 'Left' == key or 'h' == key:
            if 0 == self.column:
                pass
            else:
                self.column -= 1
                self.row = 0
                self.loadPage()
        elif 'Right' == key or 'l' == key:
            if len(self.doc.sections) == 1 + self.column:
                pass
            else:
                self.column += 1
                self.row = 0
                self.loadPage()
        elif 'Up' == key or 'k' == key:
            if 0 == self.row:
                pass
            else:
                self.row -= 1
                self.loadPage()
        elif 'Down' == key or 'j' == key:
            if len(self.doc.sections[self.column].pages) == 1 + self.row:
                pass
            else:
                self.row += 1
                self.loadPage()
        # Overview
        elif 'o' == key:
            pass

