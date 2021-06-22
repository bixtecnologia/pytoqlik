import websocket
import requests
import ssl
import json
from random import randint
import pandas as pd
import re
import webbrowser
from IPython.display import IFrame
from IPython.core.display import display, HTML
from time import sleep

class QSEngineAPI:
    def __init__(self, host="ws://localhost:4848/app", verbose=False):
        self.host = host
        self.ws = websocket.create_connection(host, sslopt={"cert_reqs": ssl.CERT_NONE})
        result = self.ws.recv()
        if(verbose):
            print(f'Connect to {host}')

    def reconnect(self):
        self.ws = websocket.create_connection(self.host, sslopt={"cert_reqs": ssl.CERT_NONE})
        result = self.ws.recv()

    def send_request(self, request):
        self.ws.send(json.dumps(request))
        result = self.ws.recv()
        y = json.loads(result)
        return y

    def close(self):
        self.ws.close()

    def GetDocListDic():
        return {
            "handle": -1,
            "method": "GetDocList",
            "params": [],
            "outKey": -1,
            "id": randint(1, 10000000)
        }

    def CreateAppDic(qAppName):
        return {
            "handle": -1,
            "method": "CreateApp",
            "params": {
                "qAppName": qAppName,
                "qLocalizedScriptMainSection": ""
            }
        }

    def DeleteAppDic(qAppId):
        return {
            "handle": -1,
            "method": "DeleteApp",
            "params": {
                "qAppId": qAppId
            }
        }

    def OpenDocDic(qAppId):
        return {
            "jsonrpc": "2.0",
            "method": "OpenDoc",
            "handle": -1,
            "params": [
                qAppId
            ],
            "outKey": -1,
            "id": randint(1, 10000000)
        }

    def GetDocList(self):
        return self.send_request(QSEngineAPI.GetDocListDic())

    def CreateApp(self, qAppName, replace):
        is_new = 1
        result = self.send_request(QSEngineAPI.CreateAppDic(qAppName))
        if ('error' in result):
            if (result['error']['message'] == 'App already exists' and replace == True):
                app_id = \
                list(filter(lambda app: app['qTitle'] == qAppName, self.GetDocList()['result']['qDocList']))[0][
                    'qDocId']
                is_new = 0
            else:
                raise Exception('Error: ' + result['error']['message'] + '. Either use replace=True or change the appName')
        else:
            app_id = result['result']['qAppId']

        return app_id, is_new

    def DeleteApp(self, qAppId):
        return self.send_request(QSEngineAPI.DeleteAppDic(qAppId))

    def OpenDoc(self, qAppId, is_new):
        app_host = self.host + '/' + QSEngineAPI.AppIDtoURL(qAppId)
        app = QSEngineAPIApp(host=app_host, verbose=False)
        app.SetAppId(qAppId)
        app.SetIsNew(is_new)
        result = app.send_request(QSEngineAPI.OpenDocDic(qAppId))
        return {
            'result': result,
            'appConnection': app
        }

    def AppIDtoURL(qAppId):
        app_url = qAppId.replace(':', '%3A').replace('\\', '%5C').replace(' ', '%20')
        return app_url


class QSEngineAPIApp(QSEngineAPI):
    def DoSaveDic():
        return {
            "handle": 1,
	        "method": "DoSave",
	        "params": {
		        "qFileName": ""
	        },
	        "outKey": -1,
	        "id": randint(1, 10000000)
        }

    def SetScriptDic(qScript):
        return {
            "handle": 1,
            "method": "SetScript",
            "params": {
                "qScript": qScript
            },
            "outKey": -1,
            "id": randint(1, 10000000)
        }

    def CheckScriptSyntaxDic():
        return {
            "handle": 1,
            "method": "CheckScriptSyntax",
            "params": {},
            "outKey": -1,
            "id": randint(1, 10000000)
        }

    def DoReloadDic():
        return {
            "handle": 1,
            "method": "DoReload",
            "params": {
                "qMode": 0,
                "qPartial": False,
                "qDebug": False
            }
        }

    def CreateObjectSheetDic(name):
        return {
            "handle": 1,
            "method": "CreateObject",
            "params": {
                "qProp": {
                    "qInfo": {
                        "qType": "sheet"
                    },
                    "qMetaDef": {
                        "title": name,
                        "description": "Created using PyToQlik."
                    },
                    "rank": 0,
                    "thumbnail": {
                        "qStaticContentUrlDef": {}
                    },
                    "columns": 24,
                    "rows": 12,
                    "cells": []
                }
            }
        }

    def GetObjectsDic(types):
        return {
            "handle": 1,
            "method": "GetObjects",
            "params": {
                "qOptions": {
                    "qTypes": types,
                    "qIncludeSessionObjects": False,
                    "qData": {}
                }
            },
            "outKey": -1,
            "id": 10
        }

    def GetObjectDic(obj_id):
        return {
            "handle": 1,
            "method": "GetObject",
            "params": {
                "qId": obj_id
            }
        }

    def GetLayoutDic(handle):
        return {
            "handle": handle,
            "method": "GetLayout",
            "params": {},
            "outKey": -1,
            "id": randint(1, 10000000)
        }

    def GetHyperCubeDataDic(qWidth, qHeight, handle):
        return {
            "handle": handle,
            "method": "GetHyperCubeData",
            "params": {
                "qPath": "/qHyperCubeDef",
                "qPages": [
                    {
                        "qLeft": 0,
                        "qTop": 0,
                        "qWidth": qWidth,
                        "qHeight": qHeight
                    }
                ]
            }
        }

    def DoSave(self):
        return self.send_request(QSEngineAPIApp.DoSaveDic())

    def SetAppId(self, qAppId):
        self.app_id = qAppId

    def SetIsNew(self, is_new):
        self.is_new = is_new

    def SetScript(self, qScript):
        return self.send_request(QSEngineAPIApp.SetScriptDic(qScript))

    def CheckScriptSyntax(self):
        return self.send_request(QSEngineAPIApp.CheckScriptSyntaxDic())

    def DoReload(self):
        return self.send_request(QSEngineAPIApp.DoReloadDic())

    def GetObjects(self, types):
        return self.send_request(QSEngineAPIApp.GetObjectsDic(types))

    def CreateObjectSheet(self, name):
        result = self.GetObjects(['sheet'])  # Check if obj already exists
        while ('suspend' in result):  # Check if app is reloading
            result = self.GetObjects(['sheet'])
        list_ob = list(filter(lambda obj: obj['qMeta']['title'] == name, result['result']['qList']))
        if (len(list_ob) > 0):
            self.sheet = list_ob[0]['qInfo']['qId']
        else:
            #             self.ws.recv()
            result = self.send_request(QSEngineAPIApp.CreateObjectSheetDic(name))
            self.sheet = result['result']['qReturn']['qGenericId']
        return self.sheet

    def GetUrlToSheet(self):
        index_app = self.host.index('/app/')
        host_app = 'http://' + self.host[5:index_app] + '/sense' + self.host[index_app:]
        self.host_sheet = host_app + '/sheet/' + self.sheet + '/state/edit'
        return self.host_sheet

    def GetUrlToApp(self):
        index_app = self.host.index('/app/')
        host_app = 'http://' + self.host[5:index_app] + '/sense' + self.host[index_app:]
        self.host_app = host_app
        return self.host_app

    def GetObject(self, obj_id):
        result = self.send_request(QSEngineAPIApp.GetObjectDic(obj_id))
        handle = result['result']['qReturn']['qHandle']
        while ('change' in result):
            print('CHANGE: ')
            print(result)
            result = self.send_request(QSEngineAPIApp.GetObjectDic(obj_id))
        if (result['result']['qReturn']['qType'] is None):
            raise Exception(f'Object {obj_id} does not exist. Typo? Maybe reopen app using openApp()?')
        return result, handle

    def GetHyperCubeData(self, handle, qWidth=100, qHeight=100):
        return self.send_request(QSEngineAPIApp.GetHyperCubeDataDic(qWidth, qHeight, handle))

    def GetLayout(self, handle):
        return self.send_request(QSEngineAPIApp.GetLayoutDic(handle))

    def toPy(self, objectID, qWidth=10, qHeight=1000, return_json=False, verbose=False):

        if (qWidth*qHeight > 10000):
            raise Exception("qWidth * qHeight must not exceed 10000.")

        self.reconnect()
        self.send_request(QSEngineAPI.OpenDocDic(self.app_id))

        self.GetObject(objectID)
        handle = self.GetObject(objectID)[1]  # GetObject now returns a tuple whose second element contains object handle
        result = self.GetHyperCubeData(handle, qWidth, qHeight)
        if (return_json == True):
            return result

        result2 = self.GetLayout(handle)

        if (verbose):
            print('Object handle is ' + str(handle))
            print('Layout output is ' + str(result2))

        columns = [x['qFallbackTitle'] for x in result2['result']['qLayout']['qHyperCube']['qDimensionInfo']] + [
            x['qFallbackTitle'] for x in result2['result']['qLayout']['qHyperCube']['qMeasureInfo']]

        if ('columnOrder' in result2['result']['qLayout']['qHyperCube']):
            columns = [columns[i] for i in result2['result']['qLayout']['qHyperCube']['columnOrder']]

        rows = []

        for row in result['result']['qDataPages'][0]['qMatrix']:
            elem = {}
            for index, col in enumerate(row):
                elem[f'{index}'] = col['qNum'] if (col['qNum'] != 'NaN') else col['qText']
            rows.append(elem)

        df = pd.DataFrame(rows)
        df.columns = columns

        if (df.empty):  # No measures in object
            print(f'No data in {objectID} object. Is it empty?')
            print('Shape (r,c): ' + str(df.shape))
            return df
           
        else:
            print('Shape (r,c): ' + str(df.shape))
            return df

class Pytoqlik():
    ### INIT FUNCTION ###
    def __init__(self, host="ws://localhost:4848/app", api_key='', tenant='', appId='', verbose=True):
        self.host = host
        self.tenant = tenant.replace('https://', 'wss://')
        self.auth_header = {'Authorization': 'Bearer ' + api_key}
        self.CloudId = appId
        self.CloudTenant = tenant

        if (self.tenant != 'https://') and (self.auth_header != {'Authorization': 'Bearer '}):
            self.isCloud = True
            if (verbose):
                print('Successfully pointed to Qlik Cloud at: ' + str(self.tenant) + ' with API key: ' + str(api_key))
        else:
            self.isCloud = False
            if (verbose):
                print('Successfully pointed to Qlik Desktop at: ' + str(self.host))

        if (self.isCloud):
            self.ws = websocket.WebSocket()
            self.ws.connect(self.tenant + '/app/' + appId, header=self.auth_header, origin=tenant)
            print(self.ws.recv())

    ### GETTERS AND SETTERS FOR CLOUD ###
    def getActiveApp(self):
        if (self.isCloud):
            self.ws.send(json.dumps({
            "jsonrpc": "2.0",
            "id": randint(1,1000000),
            "method": "GetActiveDoc",
            "handle": -1,
            "params": []
            }))
            result = self.ws.recv()
            return result
            
    def createCloudApp(self, appName='PythonAppCloud', verbose=True):
        if (self.isCloud):
            self.ws.send(json.dumps({
            "jsonrpc": "2.0",
            "id": 6,
            "handle": -1,
            "method": "CreateApp",
            "params": {
                "qAppName": appName,
                "qLocalizedScriptMainSection": "value",
                "qLocale": "value"
                }
            }))
        result = json.loads(self.ws.recv())
        if (verbose) and result['result']['qSuccess'] == True:
            print(f'Successfully created app {appName} with ID: {result["result"]["qAppId"]}')
        return result

    def setCloudScript(self, handle=1, script='', verbose=False):
        if (self.isCloud):
            self.ws.send(json.dumps({
            "handle": handle,
            "method": "SetScript",
            "params": {
                "qScript": script
            },
            "outKey": -1,
            "id": randint(1,1000000)
        }))
        result = json.loads(self.ws.recv())
        if (verbose) and result['change'][0] == 1:
            print('Script set successfully')
        return result

    def reloadCloudApp(self, handle=1, verbose=False):
        if (self.isCloud):
            self.ws.send(json.dumps({
            "handle": handle,
            "method": "DoReload",
            "params": {
                "qMode": 0,
                "qPartial": False,
                "qDebug": False
            },
            "outKey": -1,
            "id": randint(1,1000000)
        }))
        result = json.loads(self.ws.recv())
        if (verbose) and result['change'][0] == 1:
            print('Script reloaded successfully')
        return result

    def saveCloudApp(self, handle=1, verbose=False):
        if (self.isCloud):
            self.ws.send(json.dumps({
            "handle": handle,
            "method": "DoSave",
            "params": {
                "qFileName": ""
            },
            "outKey": -1,
            "id": randint(1,1000000)
        }))
        result = json.loads(self.ws.recv())
        if (verbose) and result['change'][0] == 1:
            print('Script saved successfully')
        return result
        
    def getObject(self, objId, verbose=False):
        if (self.isCloud):
            self.ws.send(json.dumps({
            "handle": 1,
            "method": "GetObject",
            "params": {
                "qId": objId
            }
        }))
        result = json.loads(self.ws.recv())
        return result

    def getHCData(self, handle, qWidth=10, qHeight=1000):
        if (self.isCloud):
            self.ws.send(json.dumps({
            "handle": handle,
            "method": "GetHyperCubeData",
            "params": {
                "qPath": "/qHyperCubeDef",
                "qPages": [
                    {
                        "qLeft": 0,
                        "qTop": 0,
                        "qWidth": qWidth,
                        "qHeight": qHeight
                    }
                ]
            }
        }))
        result = json.loads(self.ws.recv())
        return result

    def getCloudLayout(self, handle=1, verbose=False):
        if (self.isCloud):
            self.ws.send(json.dumps({
            "jsonrpc": "2.0",
            "id": randint(1,100000),
            "handle": handle,
            "method": "GetLayout",
            "params": {}
            }))
        result = json.loads(self.ws.recv())
        return result

    def cloudReconnect(self):
        self.ws.connect(self.tenant + '/app/' + self.CloudId, header=self.auth_header, origin=self.CloudTenant)
        result = self.ws.recv()

    ### FUNCTIONALITY ###
    def toPy(self, objId):
        if (self.isCloud):
            self.cloudReconnect()
            self.getActiveApp()
            handle = self.getObject(objId)['result']['qReturn']['qHandle']
            result = self.getHCData(handle)
            result2 = self.getCloudLayout(handle)

            columns = [x['qFallbackTitle'] for x in result2['result']['qLayout']['qHyperCube']['qDimensionInfo']] + [x['qFallbackTitle'] for x in result2['result']['qLayout']['qHyperCube']['qMeasureInfo']]
            if ('columnOrder' in result2['result']['qLayout']['qHyperCube']):
                columns = [columns[i] for i in result2['result']['qLayout']['qHyperCube']['columnOrder']]

            rows = []
            for row in result['result']['qDataPages'][0]['qMatrix']:
                elem = {}
                for index, col in enumerate(row):
                    elem[f'{index}'] = col['qNum'] if (col['qNum'] != 'NaN') else col['qText']
                rows.append(elem)

            df = pd.DataFrame(rows)
            df.columns = columns

            if (df.empty):  # No measures in object
                print(f'No data in {objId} object. Is it empty?')
                print('Shape (r,c): ' + str(df.shape))
                return df
           
            else:
                print('Shape (r,c): ' + str(df.shape))
                return df

    def toQlik(self, *df,
               appName='PythonApp',
               sheetName=None,
               redirect=False,
               embedded=True,
               replace=True,
               verbose=True,
               width = 980,
               height = 800,
               decimal='.',
               separator=';',
               warning=True):

        if (self.isCloud):
            compositeScript = ''
            for dataframe in df:
                data = dataframe.to_csv(sep=separator, index=False, decimal=decimal)
                currentScript = f"""
                LOAD * INLINE\n[
                {data}\n]
                (delimiter is '{separator}');
                """
                compositeScript = compositeScript + currentScript

            self.getActiveApp()
            if (warning):
                ans = input('This will replace your current data scripts in the app. Are you sure you want to proceed? (Y/N)\n')
                if ans == 'y' or ans == 'Y':
                    self.setCloudScript(script=compositeScript)
                    self.reloadCloudApp()
                else:
                    print('Operation aborted')
            else:
                self.setCloudScript(script=compositeScript)
                self.saveCloudApp()
                self.reloadCloudApp()
            
        else:
            print(self.host)
            self.qs = QSEngineAPI(self.host, verbose=verbose)
            qs = self.qs
            app_id, is_new = qs.CreateApp(appName, replace)

            result = qs.OpenDoc(app_id,is_new)
            app = result['appConnection']

            compositeScript = ''
            for dataframe in df:
                data = dataframe.to_csv(sep=separator, index=False, decimal=decimal)
                currentScript = f"""
                LOAD * INLINE\n[
                {data}\n]
                (delimiter is '{separator}');
                """

                compositeScript = compositeScript + currentScript

            app.SetScript(compositeScript)
            result = app.CheckScriptSyntax()['result']['qErrors']
            if (len(result) > 0):
                raise Exception('Script Syntax Error: ' + str(result))
            app.DoReload()

            if (sheetName) is not None:
                app.CreateObjectSheet(sheetName)
                url = app.GetUrlToSheet()
            else:
                if (verbose):
                    print('No sheetName provided. Opening app home screen...')
                    url = app.GetUrlToApp()

            if(verbose):
                print('Current Qlik URL: ', url)
            if (redirect):
                webbrowser.open(url)
            if (embedded):
                display(IFrame(url, width, height))

            qs.close()
            return app

        s = requests.Session()
        s.headers.update(self.auth_header)

    def openApp(self, appName='PythonApp', 
                sheetName=None,
                redirect=False,
                embedded=True,
                width=980,
                height=800,
                verbose=True):
        """Opens specified Qlik app. Cloud versions can only access apps that the user's API key can access. Desktop version accesses all apps inside Qlik's folder"""

        if (self.isCloud):
            print('Connecting to Qlik Cloud...')
            self.ws.send(json.dumps(
            {
                "handle": -1,
                "method": "OpenDoc",
                "params": {
                    "qDocName": appName,
                    "qUserName": "",
                    "qPassword": "",
                    "qSerial": "",
                    "qNoData": False
                }
            }))
            result = self.ws.recv()
            result = json.loads(result)
            if result['error']['code'] == 1002:
                print(f'App {self.id} is already open. Please instatiate a new Pytoqlik() object if you want to change apps')

        else:
            self.qs = QSEngineAPI(self.host, verbose=verbose)
            qs = self.qs

            app_id, is_new = qs.CreateApp(appName, True)
            result = qs.OpenDoc(app_id, 0)
            app = result['appConnection']
            if (sheetName) is not (None):
                app.CreateObjectSheet(sheetName)
                
            if (is_new):
                print(f'No app named {appName} found. Creating new Qlik Application...')

            if (sheetName) is not None:
                app.CreateObjectSheet(sheetName)
                url = app.GetUrlToSheet()
            else:
                if (verbose):
                    print('No sheetName provided. Opening app home screen...')
                url = app.GetUrlToApp()

            if (verbose):
                print('Current Qlik URL: ' + url)
            if (redirect):
                webbrowser.open(url)
            if (embedded):
                display(IFrame(url, width, height))

            qs.close()
            return app

    def listApps(self, verbose=False, return_json=False):
        """Returns a pandas DataFrame containing information about all Qlik Apps in host. KNOWN ISSUES: returns weird results, depending on which app Pytoqlik is referring to. Doesnt return all apps"""          

        if (self.isCloud):
            self.ws.send(json.dumps({
	            "handle": -1,
	            "method": "GetDocList",
	            "params": {},
	            "outKey": -1,
	            "id": randint(1,1000000)
                }))
            result = self.ws.recv()
            result = json.loads(result)
            sizeOf = len(result['result']['qDocList'])
            for i in range(sizeOf):
                print(result['result']['qDocList'][i]['qDocName'])

            tempList = []
            if 'result' in result:
                totalLen = len(result['result']['qDocList'])
                for i in range(totalLen):
                    tempList.append([result['result']['qDocList'][i]['qDocName'], result['result']['qDocList'][i]['qDocId'], str(result['result']['qDocList'][i]['qFileSize']/1024) + ' kB'])

            appList = pd.DataFrame(tempList, columns = ['App Name', 'App Location', 'File Size'])
            pd.set_option('max_colwidth', 100)
            return appList

        else:
            self.qs = QSEngineAPI(self.host)
            qs=self.qs

            result = qs.GetDocList()
            tempList = []

            if (return_json):
                print(result)

            if 'result' in result:
                totalLen = len(result['result']['qDocList'])
                for i in range(totalLen):
                    tempList.append([result['result']['qDocList'][i]['qDocName'], result['result']['qDocList'][i]['qDocId'], str(result['result']['qDocList'][i]['qFileSize']/1024) + ' kB'])

            appList = pd.DataFrame(tempList, columns = ['App Name', 'App Location', 'File Size'])
            pd.set_option('max_colwidth', 100)
            return appList