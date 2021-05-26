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
    def __init__(self, host="ws://localhost:4848/app"):
        self.host = host
        self.ws = websocket.create_connection(host, sslopt={"cert_reqs": ssl.CERT_NONE})
        result = self.ws.recv()
        print(f'Connect to {host}')

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
        result = self.send_request(QSEngineAPI.CreateAppDic(qAppName))
        if ('error' in result):
            if (result['error']['message'] == 'App already exists' and replace == True):
                app_id = \
                list(filter(lambda app: app['qTitle'] == 'PythonApp', self.GetDocList()['result']['qDocList']))[0][
                    'qDocId']
            else:
                raise Exception('Error: ' + result['error']['message'])
        else:
            app_id = result['result']['qAppId']
        return app_id

    def DeleteApp(self, qAppId):
        return self.send_request(QSEngineAPI.DeleteAppDic(qAppId))

    def OpenDoc(self, qAppId):
        app_host = self.host + '/' + QSEngineAPI.AppIDtoURL(qAppId)
        app = QSEngineAPIApp(host=app_host)
        result = app.send_request(QSEngineAPI.OpenDocDic(qAppId))
        return {
            'result': result,
            'appConnection': app
        }

    def AppIDtoURL(qAppId):
        app_url = qAppId.replace(':', '%3A').replace('\\', '%5C').replace(' ', '%20')
        return app_url


class QSEngineAPIApp(QSEngineAPI):
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

    def CheckScriptSyntexDic():
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
                        "description": "Created using python code"
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

    def GetLayoutDic():
        return {
            "handle": 2,
            "method": "GetLayout",
            "params": {},
            "outKey": -1,
            "id": 28
        }

    def GetHyperCubeDataDic(qWidth, qHeight):
        return {
            "handle": 2,
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

    def SetScript(self, qScript):
        return self.send_request(QSEngineAPIApp.SetScriptDic(qScript))

    def CheckScriptSyntex(self):
        return self.send_request(QSEngineAPIApp.CheckScriptSyntexDic())

    def DoReload(self):
        return self.send_request(QSEngineAPIApp.DoReloadDic())

    def GetObjects(self, types):
        return self.send_request(QSEngineAPIApp.GetObjectsDic(types))

    def CreateObjectSheet(self, name):
        result = self.GetObjects(['sheet'])  # Check if obj already exists
        while ('suspend' in result):  # Check if app is reloading
            result = self.GetObjects(['sheet'])
            print(result)
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
        if (result['result']['qReturn']['qType'] is None):
            raise Exception(f'Object {obj_id} not exists')
        return result

    def GetHyperCubeData(self, qWidth=100, qHeight=100):
        return self.send_request(QSEngineAPIApp.GetHyperCubeDataDic(qWidth, qHeight))

    def GetLayout(self):
        return self.send_request(QSEngineAPIApp.GetLayoutDic())

    def toPy(self, objectID, qWidth=10, qHeight=1000, return_json=False):
        self.GetObject(objectID)
        result = self.GetHyperCubeData()
        if (return_json == True):
            return result

        result2 = self.GetLayout()
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
        return df


class Pytoqlik():
    def __init__(self, host="ws://localhost:4848/app"):
        self.host = host
        self.qs = QSEngineAPI(host)

    def toQlik(self, df,
               appName='PythonApp',
               sheetName='Dashboard',
               redirect=False,
               embedded=True,
               replace=True,
               verbose=True):
        qs = self.qs

        app_id = qs.CreateApp(appName, replace)

        result = qs.OpenDoc(app_id)
        app = result['appConnection']

        data = df.to_csv(sep=';', index=False, float_format=None)
        script = f"""
        LOAD * INLINE [
        {data}
            ](delimiter is ';');
        """
        app.SetScript(script)
        result = app.CheckScriptSyntex()['result']['qErrors']
        if (len(result) > 0):
            raise Exception('Script Syntex Error: ' + str(result))
        app.DoReload()
        app.CreateObjectSheet(sheetName)
        url = app.GetUrlToSheet()
        print(url)
        if (redirect):
            webbrowser.open(url)
        if (embedded):
            display(IFrame(url, 980, 800))

        # qs.DeleteApp(app_id)

        qs.close()
        # app.close()
        return app

    def openQlik(self, appName='PythonApp', sheet=None,
                 redirect=False,
                 embedded=True,
                 verbose=True):

        qs = self.qs

        app_id = qs.CreateApp(appName, True)

        result = qs.OpenDoc(app_id)
        app = result['appConnection']

        url = app.GetUrlToApp()
        print(url)
        if (redirect):
            webbrowser.open(url)
        if (embedded):
            display(IFrame(url, 980, 800))

        # qs.DeleteApp(app_id)

        qs.close()
        # app.close()
        return app