# -*- coding: utf-8 -*-

import configparser as parser
import logging as log
import sys, getopt

# Executed directly
if '__main__' == __name__:
    log.error('This file should not be executed directly!')

class Config:
    '''
    Defined to store configurations
    '''
    confParser = parser.ConfigParser(allow_no_value=True)
    inName = 'demo.md'
    configName = 'pypt.conf'
    theme = {}
    theme['h1'] = ['Sans', 24, 'bold']
    theme['h2'] = ['Sans', 20, 'bold italic']
    theme['h3'] = ['Serif', 14, 'bold italic']
    theme['p'] = ['Serif', 16, '']
    theme['it'] = ['Serif', 16, 'italic']
    theme['bd'] = ['Sans', 16, 'bold']
    theme['bdit'] = ['Sans', 16, 'bold italic']
    theme['cb'] = ['Mono', 16, 'bold italic']
    theme['ln'] = ['Serif', 16, 'italic']

    def readArgu(self):
        # Command arguments
        opts, _ = getopt.getopt(sys.argv[1:],
                'hi:c:', ['help', 'input=', 'config='])
        for key, value in opts:
            if key in ('-h', '--help'):
                self.usage()
                sys.exit()
            elif key in ('-i', '--input'):
                Config.inName = value
            elif key in ('-c', '--config'):
                Config.configName = value

    def readConf(self):
        # Read configurations
        log.info('Reading config file...')
        Config.confParser.read(Config.configName)
        for sec in Config.confParser.sections():
            for key, value in Config.confParser.items(sec):
                if 'font' == key:
                    Config.theme[sec][0] = value
                elif 'size' == key:
                    Config.theme[sec][1] = value
                elif 'form' == key:
                    Config.theme[sec][2] = value
        log.info('Configurations loaded')

    def writeConf(self):
        # Write configurations
        log.info('Generating config file...')
        for key in Config.theme.keys():
            if not Config.confParser.has_section(key):
                Config.confParser.add_section(key)
            Config.confParser.set(key, 'font', Config.theme[key][0])
            Config.confParser.set(key, 'size', str(Config.theme[key][1]))
            Config.confParser.set(key, 'form', Config.theme[key][2])
        Config.confParser.write(open(Config.configName, 'w'))
        log.info('Config file saved to ' + Config.configName)

    # Help message
    def usage(self):
        print('Usage:')
        print('python pypt.py [options [argus]]')
        print('    -h')
        print('    --help              Print help message')
        print('    -i [file]')
        print('    --input=[file]      Input file')
        print('    -c [file]')
        print('    --config=[file]     Configuration file')

