import configparser
import os
import time

versionCode='bluebanana'

def createConfig():
    config = configparser.ConfigParser()

    config['General'] = {'verCode': versionCode, 'interval': '30'}
    config['HTTP'] = {'page': 'testpage.html'}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def readConfig():
    config = configparser.ConfigParser()

    config.read('config.ini')

    verCode = config.get('General', 'verCode')
    interval = config.get('General', 'interval')
    httpPage = config.get('HTTP', 'page')

    configValues = {
        'verCode': verCode,
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
    if not configData['verCode']==versionCode:
        print("[WARNING]: Config Mismatch Found!")
        print("The configuration file stored on your device has a different version code than the Scoring Engine you are running.")
        print("Enter [Y] to delete the old config and rebuild a new one.")
        print("Enter [N] to INGORE VERSION MISMATCH and go on vibes.")
        print("Other input will EXIT.")
        configdelChoice=input("Y/N:")
        if configdelChoice == 'Y' or 'y':
            os.remove("./config.ini")
            createConfig()
        if configdelChoice == 'N' or 'n':
            print("Fine then.")
            print("Attempting to continue with mismatched Config!")
        else:
            print("")
            print("EXITING")
            time.sleep (3)
if __name__=="__main__":
    main()
