import configparser
import os
import hashlib
import requests

def createConfig():
    config = configparser.ConfigParser()

    config['General'] = {'interval': '30'}
    config['Addresses'] = {'Ecomm': '127.0.0.1'}
    config['EComm'] = {'page': 'testecomm.html', 'enabled': '1'}
    config['UbuntuWeb'] = {'page': 'testubuntu.html', 'enabled': '1'}
    config['Webmail'] = {'page': 'testmail.html', 'enabled': '1'}

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def readConfig():
    config = configparser.ConfigParser()

    config.read('config.ini')

    interval = config.get('General', 'interval')
    ecommPage = config.get('EComm', 'page')
    ecommAddress = config.get('Addresses', 'Ecomm')
    ecommEnabled = config.get('EComm', 'Enabled')

    configValues = {
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

    if configData['ecommEnabled'] == '1':
        ecommUp = checkHTTP(configData, 'ecomm')
        print(ecommUp)

if __name__=="__main__":
    main()