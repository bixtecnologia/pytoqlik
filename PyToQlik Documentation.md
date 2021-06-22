# Pytoqlik()
Pytoqlik() instatiates a Python and Qlik connection and allows usage of the methods below to manipulate, import/export data and effectively control Qlik applications using Python. 

In Qlik Cloud, you might need to log in your tenant using your browser to refresh cookies in order to get access to some of the functionalities.

### Usage:
```python
Pytoqlik(host='ws://localhost:4848/app', api_key='', tenant='', appId='', verbose=True)
```

### Argument breakdown:
- **host**: string. Set the host address of your Qlik Server. This is used to connect to the Qlik Desktop API. If you want to use the Qlik Cloud API, leave this field unchanged. Default: 'ws://localhost:4848/app'.
- **api_key**: string. This field is related to Qlik Cloud API. You must ask your tenant developers or have the developer role to create an API Key inside your profile. Leave unchanged if you want to connect to Qlik Desktop. Default: ''.
- **tenant**: string. URL of your Qlik Cloud tenant. For example: "https://my-tenant.us.qlikcloud.com/". Leave unchanged if connecting to Qlik Desktop. Default: ''
- **appId**: string. Part of the URL of the Qlik Cloud application you want to access. All Qlik Cloud applications have an ID in the form of: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", such as "5078a285-39f8-4bd1-8b1b-351d6cef77ea". You can access this by simply entering the app through your browser and copying the string after "/sense/app/". Leave unchanged if accessing Qlik Desktop. Default: ''
- **verbose**: boolean. Toggles verbose printing. Default: True.

### Example:
```python
import pytoqlik
p2q = pytoqlik.Pytoqlik()
# (Connects to Qlik Sense Desktop version)
```

------------------------------------------------------------------------------------------
# toQlik()
toQlik() is a method called on a Pytoqlik object previously created. It is used to create a new Qlik application using pandas DataFrames as data sources, or to append pandas DataFrames to an existing Qlik application by setting the appName and/or sheetName (Desktop only). Running toQlik() on an existing app will overwrite the scripts being run in it. 

The data is loaded using Qlik's Data Load Editor, and as such, you might want to synchronize the scripted tables inside Qlik once you load your pandas DataFrame.

For Qlik Cloud version, this method will rewrite the script of the currently selected Qlik application. That is, it will only work on the current application class Pytoqlik(). That means you cannot set the appName nor sheetName. It will also not create a new application by default.

### Usage:
```python
Pytoqlik().toQlik(*df, appName='PythonApp', sheetName='Dashboard', redirect=False, embedded=True, replace=True, verbose=False, width = 980, height = 800, decimal='.', separator=';', warning=True)
```

### Argument breakdown:
- **df**: pandas DataFrame. This data structure will be converted to a .csv file and added to desired Qlik application. This is a required argument, and you can pass multiple DataFrames in a single call of toQlik().
- **appName**: string. The data will be loaded to the Qlik application with this name. If no existing applications match the name, a new one will be created. Default: 'PythonApp'.
- **sheetName**: string. The command automatically creates a new sheet inside de application for you to work on, whose name can be set in this argument. Default: 'Dashboard'.
- **redirect**: boolean. When set to True, executing the toQlik() method will open the Qlik application in your web browser. Default: False.
- **embedded**: boolean. When set to False, toQlik() will not display the embedded Qlik editor in your Jupyter Notebook. Useful if using redirect. Default: True.
- **replace**: If replace is set to False, trying to use toQlik() in an application that already exists returns an error. If set to True, calling toQlik() to an application that already exists replaces it with the new data. Default: True.
- **verbose**: boolean. Whether or not toQlik() will print out results in the console. Default: True.
- **width / height**: integers. Set embedded display size in pixels. Default: 980px by 800px (w x h).
- **decimal**: string.  Decimal separator for real numbers in your pandas DataFrame. Default: '.'.
- **separator**: string.  Value separator in your pandas DataFrame. Default: ';'.
- **warning**: boolean. Toggle an input warning telling you this method will rewrite all scripts currently in your app. Cloud version only. Default: True.


### Example:
```python
import pytoqlik
import seaborn

p2q = pytoqlik.Pytoqlik()

data1 = seaborn.load_dataset('tips')
data2 = seaborn.load_dataset('iris')

p2q.toQlik(data1, data2, appName='MyQlikApplication')
```

------------------------------------------------------------------------------------------
# toPy()
toPy() converts a Qlik objectID to a pandas DataFrame. You can fetch the Qlik objectID by right-clicking the object in view mode > share > embed. Then copy the objectID and use it as a string parameter in toPy(). Currently works for bar charts, combo charts, line charts, bullet charts, pie charts, treemap charts, gauges, KPIs, text.

toPy() returns an empty DataFrame if the object has no dimensions and measures. 
If there are dimensions but no measures, it returns all dimensions in a single column.
If there are measures but no dimensions, returns all measures in different columns, but all in a single row (index 0).
If there are both measures and dimensions, returns a complete DataFrame as expected.

### Disclaimer
Empty dimensions (in blank) must be set to null in QlikSense.


### Usage:
```python
app.toPy(objectID, qWidth=10, qHeight=1000, return_json=False, verbose=False)
```

### Argument breakdown:
- **objectID**: string. Qlik's objectID of the element you want to convert to a pandas DataFrame. This is a required argument.
- **qWidth**: integer. Qlik's HyperCube width to extract from the object. Default: 10.
- **qHeight**: integer. Qlik's HyperCube height to extract from the object. Default: 1000.
- **return_json**: boolean. Determines whether or not running toPy() returns the JSON format of the output. Default: False.
- **verbose**: boolean. Whether or not to print results in console. Default: False.

Note: Qlik's data pages limit HyperCube area to up to 10000 cells. As such, for now, (qWidth*qHeight) must always be < 10000.
### Example:
```python
import pytoqlik
p2q = pytoqlik.Pytoqlik()

app = p2q.openApp(appName='MyQlikApplication')
# Now grab objectID of element you want to convert to a pandas DataFrame
app.toPy('aaWTm')
```

------------------------------------------------------------------------------------------
# openApp()
openApp() is a method called on a Pytoqlik object previously created. This method is used to open and display a Qlik Application inside your Jupyter Notebook or redirect you to it in your web browser.
If there are no Qlik Applications with the name you input, this method will create a new Qlik Application with the specified name and warn you about it.

Qlik Cloud versions use a different kind of connection to applications, and as such, this method does not work for Qlik Cloud. Instead, it returns a message asking for a new Pytoqlik() object pointing to the new app to be created.

### Usage:
```python
Pytoqlik().openApp(appName='PythonApp', sheetName=None, redirect=False, embedded=True, width=980, height=800, verbose=True)
```

### Argument breakdown:
- **appName**: string. Represents the name of the application you want to open. Do not include the .qvf extension, just the file name. Default: PythonApp.
- **sheetName**: string. Select which of the sheets inside the application you want to open. If left on None, openApp() will open the application overview page. Default: None.
- **redirect**: boolean. When set to True, executing the openApp() method will open the Qlik application in your web browser. Default: False.
- **embedded**: boolean. When set to False, openApp() will not display the embedded Qlik editor in your Jupyter Notebook. Useful if using redirect. Default: True.
- **width** / **height**: integers. Set embedded display size in pixels. Default: 980px by 800px (w x h).
- **verbose**: boolean. Whether or not openApp() will print out results in the console. Default: True.

### Example:
```python
import pytoqlik
p2q = pytoqlik.Pytoqlik()

# We wanna open the app inside our web browser, so change redirect to True and embedded to False
p2q.openApp(appName='MyQlikApplication', redirect=True, embedded=False)
```

------------------------------------------------------------------------------------------
# listApps()
listApps() is a method called on a Pytoqlik object previously created. This method is used to list and display all Qlik Applications currently saved in your host. When called on a Pytoqlik object in Desktop mode, returns a pandas DataFrame containing the application name, it's path and file size. When called on a Qlik SaaS objectm returns a pandas DataFrame containing the application name, it's ObjectID and file size.

### Known Issues:
Qlik Cloud version of listApps() return a somewhat random selection of apps, and also, not a complete rundown of your tenant. This might be due to permission issues and a connectivity issue. We remind you that PyToQlik is still under active development as such issues are to be expected.

### Usage:
```python
Pytoqlik().listApps()
```

### Argument breakdown:
- **return_json**: boolean. Whether or not calling this function returns the JSON file the API provides. Default: False.

### Example:
```python
import pytoqlik
p2q = pytoqlik.Pytoqlik()

p2q.listApps()
```

------------------------------------------------------------------------------------------




