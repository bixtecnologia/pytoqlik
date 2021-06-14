import websocket
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
    def __init__(self, host="ws://localhost:4848/app"):
        self.host = host

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
               separator=';' 
               ):

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
       
    def openApp(self, appName='PythonApp', 
                sheetName=None,
                redirect=False,
                embedded=True,
                width=980,
                height=800,
                verbose=True):

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

    def listApps(self):

        self.qs = QSEngineAPI(self.host)
        qs=self.qs

        appListRaw = str(qs.GetDocList())
        
        def find_all(string, substring):
            start = 0
            while True:
                start = string.find(substring, start)
                if start == -1: 
                    return
                yield start
                start += len(substring)

        indexes = list(find_all(appListRaw, 'qTitle'))
        appNames = []
        for _ in indexes:
            name = appListRaw[_+10:]  # 10 is the offset from qTitle to beginning of name
            name = name.rsplit("'")[0]  # rsplit up to next single '
            appNames.append(name)

        indexes = list(find_all(appListRaw, 'qDocId'))
        appLocations = []
        for _ in indexes:
            loc = appListRaw[_+10:]  # 10 is the offset from qDocId to beginning of path
            loc = loc.rsplit("'")[0]  # rsplit up to next single '
            loc = loc.replace('\\\\', '\\') # Replace double backslash with singles. Python requires two backslashes to represent one
            appLocations.append(loc)

        indexes = list(find_all(appListRaw, 'qFileSize'))
        appSizes = []
        for _ in indexes:
            size = appListRaw[_+12:]  # 12 is the offset from qFileSize to beginning of size
            size = size.rsplit(",")[0]  # rsplit up to next  ,
            size = round(int(size)/1000, 2)
            size = str(size) + ' kB'
            appSizes.append(size)

        tempList = []
        for _ in range(appListRaw.count('qTitle')):
            tempList.append([appNames[_], appLocations[_], appSizes[_]])
    
        appList = pd.DataFrame(tempList, columns = ['App Name', 'App Location', 'File Size'])
        pd.set_option('max_colwidth', 100)
        return appList


