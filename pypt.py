#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging as log
# Tk graphical interfaces provided by python
import tkinter as tk
import config, document, window

def main():
    '''
    Main process of the PyPt program
    '''
    # Initialize configurations
    conf = config.Config()
    conf.readArgu()
    conf.readConf()
    conf.writeConf()
    theme = config.Config.theme
    doc = document.Document()
    doc.readFile(config.Config.inName)

    # Create window
    win = window.Window(doc, theme)

    # Allow resize
    win.master.resizable(width=True, height=True)

    # Begin main events loop
    log.info('Begin main loop')
    win.mainloop()

if '__main__' == __name__:
    # Logging config
    log.basicConfig(level=log.DEBUG,
            format='[%(asctime)s] %(levelname)s: %(message)s',
            datefmt='%H:%M:%S')
    log.info('Calling function `main`.')
    # Function main
    main()


