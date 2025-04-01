import configparser
import os

import time
import hashlib
import requests
versionCode='bluebanana'

def createConfig():
    config = configparser.ConfigParser()

    config['General'] = {'verCode': versionCode, 'interval': '30'}
    config['Addresses'] = {'Ecomm': '127.0.0.1'}
    config['EComm'] = {'page': 'testecomm.html', 'enabled': '1'}
    config['UbuntuWeb'] = {'page': 'testubuntu.html', 'enabled': '1'}
    config['Webmail'] = {'page': 'testmail.html', 'enabled': '1'}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def readConfig():
    config = configparser.ConfigParser()

    config.read('config.ini')

    verCode = config.get('General', 'verCode')
    interval = config.get('General', 'interval')
    ecommPage = config.get('EComm', 'page')
    ecommAddress = config.get('Addresses', 'Ecomm')
    ecommEnabled = config.get('EComm', 'Enabled')

    configValues = {
        'verCode': verCode,
        'interval': interval,
        'ecommPage': ecommPage,
        'ecommAddress': ecommAddress,
        'ecommEnabled': ecommEnabled
    }

    return configValues

def checkSMTP(configData):
    print("placeholder")

def checkHTTP(configData, service):
    IP = configData[service + 'Address']
    testpage = configData[service + 'Page']
    hashFunc = hashlib.md5()

    with open(testpage, 'rb') as file:
        while chunk := file.read(8192):
            hashFunc.update(chunk)
    md5Hash = hashFunc.hexdigest()

    response = requests.get('http://' + IP + '/' + testpage)
    hashedResponse = hashlib.md5(response.content).hexdigest()

    return hashedResponse == md5Hash

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

    if configData['ecommEnabled'] == '1':
        ecommUp = checkHTTP(configData, 'ecomm')
        print(ecommUp)

if __name__=="__main__":
    main()
