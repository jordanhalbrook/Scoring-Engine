import configparser
import os.path

def createConfig():
    config = configparser.ConfigParser()

    config['General'] = {'interval': '30'}
    config['HTTP'] = {'page': 'testpage.html'}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def readConfig():
    config = configparser.ConfigParser()

    config.read('config.ini')

    interval = config.get('General', 'interval')
    httpPage = config.get('HTTP', 'page')

    configValues = {
        'interval': interval,
        'httpPage': httpPage
    }

    return configValues

def checkSMTP(configData):
    print("placeholder")

def checkHTTP(configData):
    print("placeholder")

def main():
    if not os.path.isfile('config.ini'):
        createConfig()
    configData = readConfig()

if __name__=="__main__":
    main()