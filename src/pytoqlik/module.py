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
    def __init__(self, host="ws://localhost:4848/app", userDirectory='', userId='', connectionType='cert', certs='', verbose=False):
        # Connect to Enterprise
        # UserID and userDirectory can be found in the Qlik Management Console (QMC)
        # Certificates can also be exported in the QMC (https://help.qlik.com/en-US/sense-admin/February2021/Subsystems/DeployAdministerQSE/Content/Sense_DeployAdminister/QSEoW/Administer_QSEoW/Managing_QSEoW/export-certificates.htm)
        # Auth here: https://help.qlik.com/en-US/sense-developer/June2019/Subsystems/RepositoryServiceAPI/Content/Sense_RepositoryServiceAPI/RepositoryServiceAPI-Example-Connect-cURL-Certificates.htm
        if (userDirectory != ''):
            certs = ({"ca_certs":'root.pem',
                      "certfile": 'client.pem',
                      "keyfile": 'client_key.pem',
                      "cert_reqs": ssl.CERT_REQUIRED,
                      "server_side": False})
            websocket.create_connection(host, sslopt=certs, header={f"'X-Qlik-User':  'UserDirectory={connectionType}; UserId={userId}'"})

        # Connect to Desktop
        else:
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

    def GetDocListDic(self):
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

    def GetActiveAppDic(self):
        return {
            "jsonrpc": "2.0",
            "id": randint(1,1000000),
            "method": "GetActiveDoc",
            "handle": -1,
            "params": []
        }

    def GetDocList(self):
        return self.send_request(QSEngineAPI.GetDocListDic(self))

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

    def CreateSessionObjectDic(self, dim, dimLabel, measure):
        qMeasuresList = []
        for i in range(len(measure)):
            qMeasuresList.append({
                                "qLibraryId": "",
                                "qSortBy": {
                                    "qSortByState": 0,
                                    "qSortByFrequency": 0,
                                    "qSortByNumeric": 0,
                                    "qSortByAscii": 0,
                                    "qSortByLoadOrder": 1,
                                    "qSortByExpression": 0,
                                    "qExpression": {
                                        "qv": ""
                                    }
                                },
                                "qDef": {
                                    "qLabel": "P2Q",
                                    "qDescription": "Created using PyToQlik",
                                    "qTags": [
                                        "tags"
                                    ],
                                    "qGrouping": "N",
                                    "qDef": measure[i]
                                },
                                "qAttributeExpressions": [
                                    {
                                        "qExpression": ""
                                    }
                                ]
                            })

        return {
        "jsonrpc": "2.0",
        "id": randint(1,100000),
        "method": "CreateSessionObject",
        "handle": 1,
        "params": [
            {
                "qInfo": {
                    "qId": "PTQTempObject",
                    "qType": "Chart"
                },
                "qHyperCubeDef": {
                    "qStateName": "$",
                    "qDimensions": [
                        {
                            "qLibraryId": "",
                            "qNullSuppression": False,
                            "qIncludeElemValue": False,
                            "qDef": {
                                "qGrouping": "N",
                                "qFieldDefs": [
                                    dim
                                ],
                                "qFieldLabels": [
                                    dimLabel
                                ],
                                "qSortCriterias": [
                                    {
                                        "qSortByState": 0,
                                        "qSortByFrequency": 0,
                                        "qSortByNumeric": 0,
                                        "qSortByAscii": 0,
                                        "qSortByLoadOrder": 1,
                                        "qSortByExpression": 0,
                                        "qExpression": {
                                            "qv": ""
                                        }
                                    },
                                    {
                                        "qSortByState": 0,
                                        "qSortByFrequency": 0,
                                        "qSortByNumeric": 0,
                                        "qSortByAscii": 0,
                                        "qSortByLoadOrder": 1,
                                        "qSortByExpression": 0,
                                        "qExpression": {
                                            "qv": ""
                                        }
                                    }
                                ]
                            }
                        }
                    ],
                    "qMeasures": 
                        qMeasuresList,
                    "qInitialDataFetch": [
                        {
                            "qTop": 0,
                            "qLeft": 0,
                            "qHeight": 1000,
                            "qWidth": 10
                        }
                    ]
                }
            }
        ],
        "outKey": -1
        }

    def DestroySessionObjectDic(self, id):
        return {
        "handle": 1,
        "method": "DestroySessionObject",
        "params": {
            "qId": id
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

    def GetActiveAppHandle(self):
        result = self.send_request(self.GetActiveAppDic())
        try: 
            if result['error']['code'] == 1007:
                raise Exception('Please refresh the application in your browser')
        except:
            return result['result']['qReturn']['qHandle']

    def CreateSessionObject(self, dim, dimLabel, measures):
        result = self.send_request(self.CreateSessionObjectDic(dim=dim, dimLabel=dimLabel, measure=measures))
        return result

    def DestroySessionObject(self, id):
        result = self.send_request(self.DestroySessionObjectDic(id=id))
        return result

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

    def fetchData(self, dim, dimLabel, measures, measureLabels, verbose=False):
            self.reconnect()
            self.GetActiveAppHandle() # Used just to instantiate API Doc class
            sessionObject = self.CreateSessionObject(dim, dimLabel, measures=measures)
            sessionHandle = sessionObject['result']['qReturn']['qHandle']
            resultData = self.GetHyperCubeData(sessionHandle)

            columns = [dimLabel]
            for x in measureLabels:
                columns.append(x)

            rows = []  # List of dicts containing dimension values
            for row in resultData['result']['qDataPages'][0]['qMatrix']:  # For every index in qMatrix do...
                elem = {}
                for index, col in enumerate(row):
                    elem[f'{index}'] = col['qNum'] if (col['qNum'] != 'NaN') else col['qText']
                rows.append(elem)

            df = pd.DataFrame(rows)
            df.columns = columns
            self.DestroySessionObject("PTQTempObject") # Purge Session Object

            if (df.empty):  # No measures in object
                if (verbose):
                    print(f'No data. Is it empty?')
                    print('Shape (r,c): ' + str(df.shape))
                return df
           
            else:
                if (verbose):
                    print('Shape (r,c): ' + str(df.shape))
                return df


class QSEngineAPICloud:
    def __init__(self, key='', tenant='', appId='', verbose=False, return_json=False):
        self.key = key
        self.tenant = tenant.replace('https://', 'wss://')
        self.appId = appId
        self.auth_header = {'Authorization': 'Bearer ' + key}
        self.CloudTenant = tenant.replace('wss://', 'https://')
        self.CloudId = appId

        self.isCloud = True
        if verbose:
            print('Pointed to Qlik Cloud at: ' + self.tenant + ' with API key: ' + self.key)

        self.ws = websocket.WebSocket()
        self.ws.connect(self.tenant + '/app/' + self.appId, header=self.auth_header, origin=self.CloudTenant)
        result = json.loads(self.ws.recv())
        if (return_json):
            print(result)
        if (result['params']['qSessionState'] == 'SESSION_ATTACHED') and verbose:
            print('Session attached successfully.')
        elif (result['params']['qSessionState'] == 'SESSION_CREATED') and verbose:
            print('Session created successfully.')
        elif (result['params']['qSessionState'] != 'SESSION_ATTACHED') and (result['params']['qSessionState'] != 'SESSION_CREATED'):
            raise Exception('Failed to create or attach session. Please check authentication and tenant parameters.')

    def send_request(self, request):
        self.ws.send(json.dumps(request))
        result = self.ws.recv()
        y = json.loads(result)
        return y

    def OpenAppDic(self, appName):
        return {
            "handle": -1,
            "method": "OpenDoc",
            "params": {
                "qDocName": appName,
                "qUserName": "",
                 "qPassword": "",
                "qSerial": "",
                "qNoData": False
            }
        }
            
    def GetActiveAppDic(self):
        return {
            "jsonrpc": "2.0",
            "id": randint(1,1000000),
            "method": "GetActiveDoc",
            "handle": -1,
            "params": []
        }

    def GetDocListDic(self):
        return {
	        "handle": -1,
	        "method": "GetDocList",
	        "params": {},
	        "outKey": -1,
	        "id": randint(1,1000000)
        }

    def SetScriptDic(self, handle, script):
        return {
            "handle": handle,
            "method": "SetScript",
            "params": {
                "qScript": script
            },
            "outKey": -1,
            "id": randint(1,1000000)
        }

    def SaveAppDic(self, handle):
        return {
            "handle": handle,
            "method": "DoSave",
            "params": {
                "qFileName": ""
            },
            "outKey": -1,
            "id": randint(1,1000000)
        }

    def ReloadDic(self, handle):
        return {
            "handle": handle,
            "method": "DoReload",
            "params": {
                "qMode": 0,
                "qPartial": False,
                "qDebug": False
            },
            "outKey": -1,
            "id": randint(1,1000000)
        }

    def GetObjectDic(self, objId):
        return {
            "handle": 1,
            "method": "GetObject",
            "params": {
                "qId": objId
            }
        }

    def GetHCDataDic(self, handle, qWidth, qHeight):
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

    def GetLayoutDic(self, handle):
        return {
            "jsonrpc": "2.0",
            "id": randint(1,100000),
            "handle": handle,
            "method": "GetLayout",
            "params": {}
        }

    def GetScriptDic(self, handle):
        return {
            "handle": handle,
            "method": "GetScript",
            "params": {},
            "outKey": -1,
            "id": randint(1,100000)
        }

    def EvaluateDic(self, handle, expression):
        return {
            "handle": handle,
            "method": "Evaluate",
            "params": {
                "qExpression": expression
            },
            "id": randint(1,100000),
            "jsonrpc": "2.0"
        }

    def CreateSessionObjectDic(self, dim, dimLabel, measure):
        qMeasuresList = []
        for i in range(len(measure)):
            qMeasuresList.append({
                                "qLibraryId": "",
                                "qSortBy": {
                                    "qSortByState": 0,
                                    "qSortByFrequency": 0,
                                    "qSortByNumeric": 0,
                                    "qSortByAscii": 0,
                                    "qSortByLoadOrder": 1,
                                    "qSortByExpression": 0,
                                    "qExpression": {
                                        "qv": ""
                                    }
                                },
                                "qDef": {
                                    "qLabel": "P2Q",
                                    "qDescription": "Created using PyToQlik",
                                    "qTags": [
                                        "tags"
                                    ],
                                    "qGrouping": "N",
                                    "qDef": measure[i]
                                },
                                "qAttributeExpressions": [
                                    {
                                        "qExpression": ""
                                    }
                                ]
                            })

        return {
        "jsonrpc": "2.0",
        "id": randint(1,100000),
        "method": "CreateSessionObject",
        "handle": 1,
        "params": [
            {
                "qInfo": {
                    "qId": "PTQTempObject",
                    "qType": "Chart"
                },
                "qHyperCubeDef": {
                    "qStateName": "$",
                    "qDimensions": [
                        {
                            "qLibraryId": "",
                            "qNullSuppression": False,
                            "qIncludeElemValue": False,
                            "qDef": {
                                "qGrouping": "N",
                                "qFieldDefs": [
                                    dim
                                ],
                                "qFieldLabels": [
                                    dimLabel
                                ],
                                "qSortCriterias": [
                                    {
                                        "qSortByState": 0,
                                        "qSortByFrequency": 0,
                                        "qSortByNumeric": 0,
                                        "qSortByAscii": 0,
                                        "qSortByLoadOrder": 1,
                                        "qSortByExpression": 0,
                                        "qExpression": {
                                            "qv": ""
                                        }
                                    },
                                    {
                                        "qSortByState": 0,
                                        "qSortByFrequency": 0,
                                        "qSortByNumeric": 0,
                                        "qSortByAscii": 0,
                                        "qSortByLoadOrder": 1,
                                        "qSortByExpression": 0,
                                        "qExpression": {
                                            "qv": ""
                                        }
                                    }
                                ]
                            }
                        }
                    ],
                    "qMeasures": 
                        qMeasuresList,
                    "qInitialDataFetch": [
                        {
                            "qTop": 0,
                            "qLeft": 0,
                            "qHeight": 1000,
                            "qWidth": 10
                        }
                    ]
                }
            }
        ],
        "outKey": -1
        }

    def DestroySessionObjectDic(self, id):
        return {
        "handle": 1,
        "method": "DestroySessionObject",
        "params": {
            "qId": id
            } 
        }

    def reconnect(self, verbose=False):
        self.ws.connect(self.tenant + '/app/' + self.CloudId, header=self.auth_header, origin=self.CloudTenant)
        result = self.ws.recv()
        result = json.loads(result)
        if verbose:
            if (result['params']['qSessionState'] == 'SESSION_ATTACHED') and verbose:
                print('Session attached successfully.')
            elif (result['params']['qSessionState'] == 'SESSION_CREATED') and verbose:
                print('Session created successfully.')
            elif (result['params']['qSessionState'] != 'SESSION_ATTACHED') and (result['params']['qSessionState'] != 'SESSION_CREATED'):
                raise Exception('Failed to create or attach session. Please check authentication and tenant parameters.')
        return result

    def reload(self, handle, verbose=False):
        result = self.send_request(self.ReloadDic(handle=handle))
        if verbose:
            print('Reload successful')
        return result

    def SaveApp(self, handle, verbose=False):
        result = self.send_request(self.SaveAppDic(handle=handle))
        if (verbose) and result['change'][0] == 1:
            print('Application saved successfully')
        return result

    def GetActiveApp(self, verbose=False):
        result = self.send_request(self.GetActiveAppDic())
        if verbose:
            print('Selected app is: ' + result['result']['qReturn']['qGenericId'])
        return result

    def GetActiveAppHandle(self):
        result = self.send_request(self.GetActiveAppDic())
        try: 
            if result['error']['code'] == 1007:
                raise Exception('Please refresh the application in your browser')
        except:
            return result['result']['qReturn']['qHandle']

    def GetObject(self, objId, verbose=False):
        result = self.send_request(self.GetObjectDic(objId=objId))
        if verbose:
            print('Object handle: ' + str(result['result']['qReturn']['qHandle']) + ' | Object type: ' + str(result['result']['qReturn']['qGenericType']))
        return result

    def GetHCData(self, handle, qWidth=10, qHeight=1000):
        result = self.send_request(self.GetHCDataDic(handle=handle, qWidth=qWidth, qHeight=qHeight))
        return result

    def GetLayout(self, handle):
        result = self.send_request(self.GetLayoutDic(handle=handle))
        return result

    def OpenApp(self, appName):
        result = self.send_request(self.OpenAppDic(appName=appName))
        return result

    def GetDocList(self):
        result = self.send_request(self.GetDocListDic())
        return result

    def GetScript(self, handle):
        result = self.send_request(self.GetScriptDic(handle=handle))
        return result

    def SetScript(self, handle, script, verbose=False):
        result = self.GetScript(handle=handle)
        scriptString = result['result']['qScript']
        pytoqlikTab = '///$tab PyToQlik Script\r\n'
        if pytoqlikTab in scriptString:
            # There is a PyToQlik Script section. Overwrite it!
            if (verbose):
                print('Application already has a PyToQlik Script dedicated section. Overwriting it.')

            start = '///$tab PyToQlik Script\r\n'
            end = '///$tab'
            replaceable = scriptString.split(start)[1].split(end)[0]
            
            newScript = scriptString.replace(replaceable, script)

            result = self.send_request(self.SetScriptDic(handle=handle, script=newScript))
            return result

        else:
            # There isn't a PyToQlik Script section yet. Append it to script!
            if (verbose):
                print('Application has no PyToQlik Script dedicated section. Creating it.')

            newScript = scriptString + pytoqlikTab + script

            result = self.send_request(self.SetScriptDic(handle=handle, script=newScript))
            return result

    def Evaluate(self, handle, expression):
        result = self.send_request(self.EvaluateDic(handle=handle, expression=expression))
        return result

    def CreateSessionObject(self, dim, dimLabel, measures):
        result = self.send_request(self.CreateSessionObjectDic(dim=dim, dimLabel=dimLabel, measure=measures))
        return result

    def DestroySessionObject(self, id):
        result = self.send_request(self.DestroySessionObjectDic(id=id))
        return result
    

class Pytoqlik():
    def __init__(self, host="ws://localhost:4848/app", userDirectory='', userId='', connectionType='cert', api_key='', tenant='', appId='', verbose=False, return_json=False):
        self.host = host
        self.tenant = tenant.replace('https://', 'wss://')
        self.key = api_key
        self.auth_header = {'Authorization': 'Bearer ' + api_key}
        self.CloudId = appId
        self.CloudTenant = tenant

        self.isCloud = False
        self.isEnterprise = False

        # If user has inputted a valid tenant and auth is not empty
        if (self.tenant != 'https://') and (self.auth_header != {'Authorization': 'Bearer '}):
            self.isCloud = True
            self.qsc = QSEngineAPICloud(key=self.key, tenant=self.tenant, appId=self.CloudId, verbose=verbose, return_json=return_json)

        # If user has changed hostname and no cloud auth is provided, start Enterprise
        if (host != 'ws://localhost:4848/app') and (self.auth_header == {'Authorization': 'Bearer '}):
            self.isEnterprise = True

            self.ServerUrl = f"wss://{host}/app"
            ssl.match_hostname = lambda cert, hostname: True  # Checks server-client identity

            self.qse = QSEngineAPI(host=self.ServerUrl, userDirectory=userDirectory, userId=userId, connectionType=connectionType, certs=self.certs)
            return self.qse
        
            
    ### IN DEVELOPMENT ###
    def displayIFrame(self):
        url = 'https://redacted-redacted.us.qlikcloud.com/sense/app/5078a285-39f8-4bd1-8b1b-351d6cef77ea/sheet/c44bfc0c-749f-4fcc-8378-c80905b29f18/state/analysis'
        display(IFrame(url, 700, 700))

    ### FUNCTIONALITY ###
    def toPy(self, objId, verbose=False):
        if (self.isCloud):
            self.qsc.reconnect(verbose=verbose)
            self.qsc.GetActiveApp(verbose=verbose)
            handle = self.qsc.GetActiveAppHandle()
            result = self.qsc.GetHCData(handle)
            result2 = self.qsc.GetLayout(handle)

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
                if (verbose):
                    print(f'No data in {objId} object. Is it empty?')
                    print('Shape (r,c): ' + str(df.shape))
                return df
           
            else:
                if (verbose):
                    print('Shape (r,c): ' + str(df.shape))
                return df

    def toQlik(self, *df,
               appName='PythonApp',
               sheetName=None,
               redirect=False,
               embedded=True,
               replace=True,
               verbose=False,
               width = 980,
               height = 800,
               decimal='.',
               separator=';',
               warning=True):

        if (self.isCloud):
            self.qsc.reconnect(verbose=verbose)
            compositeScript = ''
            for dataframe in df:
                data = dataframe.to_csv(sep=separator, index=False, decimal=decimal)
                currentScript = f"""
                LOAD * INLINE\n[
                {data}\n]
                (delimiter is '{separator}');
                """
                compositeScript = compositeScript + currentScript

            handle = self.qsc.GetActiveAppHandle()
            if (warning):
                ans = input('This will replace your current data scripts in the application. Are you sure you want to proceed? (Y/N)\n')
                if ans == 'y' or ans == 'Y':
                    self.qsc.SetScript(handle, script=compositeScript, verbose=verbose)
                    self.qsc.SaveApp(handle, verbose=verbose)
                    self.qsc.reload(handle, verbose=verbose)
                    if verbose:
                        print('Script successfully imported')
                else:
                    print('Operation aborted')
            else:
                self.qsc.SetScript(handle, script=compositeScript, verbose=verbose)
                self.qsc.SaveApp(handle, verbose=verbose)
                self.qsc.reload(handle, verbose=verbose)
                if verbose:
                    print('Script successfully imported')
            
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
                verbose=False):
        """Opens specified Qlik app. Cloud versions can only access apps that the user's API key can access. Desktop version accesses all apps inside Qlik's folder"""

        if (self.isCloud):
            print('Connecting to Qlik Cloud...')
            result = self.qsc.OpenApp(appName)
            if result['error']['code'] == 1002:
                print(f'App {self.CloudId} is already open. Please instatiate a new Pytoqlik() object if you want to change apps. Opening {self.CloudId} in browser... (Will not work in Google Colab)')
                url = self.CloudTenant + '/sense/app/' + self.CloudId
                webbrowser.open(url)

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

    def listApps(self, return_json=False):
        """Returns a pandas DataFrame containing information about all Qlik Apps in host. KNOWN ISSUES: might return only currently opened apps (including other users)"""          

        if (self.isCloud):
            result = self.qsc.GetDocList()
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

    def fetchData(self, dim, dimLabel, measures, measureLabels, verbose=False):
        """Gets data using the Qlik Engine, similar to toPy, but doesn't require you to pass an actual object. Instead, just pass the dimension and its label, and measures and its labels"""

        if (self.isCloud):
            self.qsc.reconnect(verbose=verbose)
            self.qsc.GetActiveAppHandle() # Used just to instantiate API Doc class
            sessionObject = self.qsc.CreateSessionObject(dim, dimLabel, measures=measures)
            sessionHandle = sessionObject['result']['qReturn']['qHandle']
            resultData = self.qsc.GetHCData(sessionHandle)

            columns = [dimLabel]
            for x in measureLabels:
                columns.append(x)

            rows = []  # List of dicts containing dimension values
            for row in resultData['result']['qDataPages'][0]['qMatrix']:  # For every index in qMatrix do...
                elem = {}
                for index, col in enumerate(row):
                    elem[f'{index}'] = col['qNum'] if (col['qNum'] != 'NaN') else col['qText']
                rows.append(elem)

            df = pd.DataFrame(rows)
            df.columns = columns
            self.qsc.DestroySessionObject("PTQTempObject") # Purge Session Object

            if (df.empty):  # No measures in object
                if (verbose):
                    print(f'No data. Is it empty?')
                    print('Shape (r,c): ' + str(df.shape))
                return df
           
            else:
                if (verbose):
                    print('Shape (r,c): ' + str(df.shape))
                return df
        
        else:
            # IS DESKTOPVERSION: runs on QSEngineAPIApp
            pass
