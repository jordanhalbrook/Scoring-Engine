import configparser
import os.path

def createConfig():
    config = configparser.ConfigParser()

    config['General'] = {'interval': '30'}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def checkSMTP():
    

def main():
    if not os.path.isfile('config.ini'):
        createConfig()

if __name__=="__main__":
    main()