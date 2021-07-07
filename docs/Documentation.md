
# The PyToQlik Library Documentation
Hello, welcome the the official PyToQlik Documentation. In here, we will break down the most relevant objects and methods to enable data extraction, data inputting and manipulation from both Qlik Cloud SaaS version and Qlik Desktop version.

## Table of Contents

- [Pytoqlik (main class)](#pytoqlik)
- [toQlik](#toqlik)
- [toPy](#topy)
- [openApp](#openapp)
- [listApps](#listapps)
- [fetchData](#fetchdata)

# Pytoqlik()
Pytoqlik() instatiates a Python and Qlik connection and allows usage of methods to manipulate, import/export data and effectively control Qlik applications using Python. This is the main object that will be created in most use cases. We recommend storing it in an easy to remember variable such as **p2q**.

### Disclaimer

- For **Qlik Desktop**, your Jupyter Notebook MUST BE hosted in your local machine. This means the Desktop version can only access your local apps, and something like a Google Colaboratory Notebook will not be able to access your local applications. We recommend using Anaconda3 to host your Notebook automatically, using the default address 'ws://localhost:4848/app'.

- For **Qlik Cloud**, you might need to log in your tenant using your browser to refresh cookies in order to get access to some of the functionalities. This is especially needed if you run into any Exceptions mentioning 'result'. Qlik Sense SaaS has a timeout interval that must be manually refreshed by logging into your tenant.


### Usage:
```python
Pytoqlik(host="ws://localhost:4848/app", api_key='', tenant='', appId='', verbose=False, return_json=False)
```

### Argument breakdown:

| **ARGUMENT**|**DATA TYPE**|**DESCRIPTION**|**DEFAULT**|
|-------------|-----------|-------------|---------|
|     **host**    |   string  |Set the host address of your Qlik Server. This is used to connect to the Qlik Desktop API. If you want to use the Qlik Cloud API, leave this field unchanged and change the others|"ws://localhost:4848/app"|
|   **api_key**   |   string  |This field is related to Qlik Cloud API. You must ask your tenant developers or have the developer role to create an API Key inside your profile. Leave unchanged if you want to connect to Qlik Desktop|""|
|    **tenant**   |   string  |URL of your Qlik Cloud tenant. For example: "https://my-tenant.us.qlikcloud.com/". Leave unchanged if connecting to Qlik Desktop |""|
|    **appId**    |   string  |Part of the URL of the Qlik Cloud application you want to access. All Qlik Cloud applications have an ID in the form of: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", such as "5078a285-39f8-4bd1-8b1b-351d6cef77ea". You can access this by simply entering the app through your browser and copying the string after "/sense/app/". Leave unchanged if accessing Qlik Desktop|""|
|   **verbose**   |  boolean  |Toggles verbose printing|False|
| **return_json** |  boolean  |Toggles JSON printing in some methods|False|

### Example 1:
```python
import pytoqlik
p2q = pytoqlik.Pytoqlik()
# (Connects to Qlik Sense Desktop version)
```

### Example 2 - Cloud:
```python
import pytoqlik
key = 'eyJhbGciOiJFUzM4NCIsImtpZCI6IjczZWUwNDgzLTc1NGYtNDc3Yy1hZTQyLTBiMTQyMjNiYzA1YyIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiSlg3bWE2eTRrd0syUHhrQXgzajJKalpMWUZJa2ZibjMiLCJqdGkiOiI3M2VlMDQ4My03NTRmLTQ3N2MtYWU0Mi0wYjE0MjIzYmMwNWMiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoieklfR3paeWJqTi1tRUlQVnZxd2ZGUm5jU25DMzhJMTMifQ.W18i31VqtS3WORXfIAouSDAEAuiaLIDy0CvZ-R1t3gv3Hy7B1f9_eyZUyxDefZSnM2Y8t6ZSMWOEjGY0Y9fMWpxxUOc3mgVpJY676Koy24OZUZ-ABx149HKnpbES57m3'
tenant = 'https://my-tenant.us.qlikcloud.com/'
ID = '5078a285-39f8-4bd1-8b1b-351d6cef77ea'

p2q = pytoqlik.Pytoqlik(api_key=key, tenant=url, appId=ID)
# (Connects to Qlik Sense Cloud at provided tenant=url, opening appId=ID and authenticate with api_key=key)
```

------------------------------------------------------------------------------------------
# toQlik()
toQlik() is a method called on a Pytoqlik object previously created. It is used to create a section called **PyToQlik Scripts** in your applications *Data Load Editor*, and the *pandas DataFrames'* data will be converted to a *.csv* file and imported to the section. Any previous scripts contained within that section will be overwritten, but not any scripts in any other sections.

In Qlik Desktop, calling this with an *appName* parameter of an application that does not currently exist will create such application, and then proceed to import the data into it.

For Qlik Cloud version, this method will write the scripts on the same section (and create such section if it does not exist yet), but it will not create a new application or any sheets. Instead, it only works on the application object previously created using Pytoqlik().

### Usage:
```python
toQlik(*df, appName='PythonApp', sheetName='Dashboard', redirect=False, embedded=True, replace=True, verbose=False, width = 980, height = 800, decimal='.', separator=';', warning=True)
```

### Argument breakdown:
| **ARGUMENT** | **DATA TYPE**    | **DESCRIPTION**                                                                                                                                                                                                 | **DEFAULT**  |
|--------------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| **df**           | pandas DataFrame | This data structure will be converted to a .csv file and added to desired Qlik application. This is a required argument, and you can pass multiple DataFrames in a single call of toQlik()                      | **REQUIRED** |
| **appName**      | string           | The data will be loaded to the Qlik application with this name. If no existing applications match the name, a new one will be created. Used for Desktop version only                                            | "PythonApp"  |
| **sheetName**    | string           | The command automatically creates a new sheet inside de application for you to work on, whose name can be set in this argument. Used for Desktop version only                                                   | "Dashboard"  |
| **redirect**     | boolean          | When set to True, executing the toQlik() method will open the Qlik application in your web browser                                                                                                              | False        |
|**embedded**     | boolean          | When set to False, toQlik() will not display the embedded Qlik editor in your Jupyter Notebook. Useful if using redirect                                                                                        | True         |
| **replace**      | boolean          | If replace is set to False, trying to use toQlik() in an application that already exists returns an error. If set to True, calling toQlik() to an application that already exists replaces it with the new data | True         |
| **verbose**      | boolean          | Whether or not toQlik() will print out results in the console                                                                                                                                                   | True         |
| **width**        | integer          | Set embedded display size width in pixels if using *embedded*                                                                                                                                                   | 980          |
| **height**       | integer          | Set embedded display size height in pixels if using *embedded*                                                                                                                                                  | 800          |
| **decimal**      | string           | Decimal separator for real numbers in your pandas DataFrame                                                                                                                                                     | "."          |
| **separator**    | string           | Value separator in your pandas DataFrame                                                                                                                                                                        | ";"          |
| **warning**      | boolean          | Toggle an input warning telling you this method will rewrite all scripts currently in your app's *PyToQlik Scripts* section. Used in Cloud version only.  |True|


### Example 1:
```python
import pytoqlik
import seaborn

p2q = pytoqlik.Pytoqlik()

data1 = seaborn.load_dataset('tips')
data2 = seaborn.load_dataset('iris')

p2q.toQlik(data1, data2, appName='MyQlikApplication', sheetName='Visualization')
```

### Example 2 - Cloud:
```python
import pytoqlik
import seaborn

key =  'eyJhbGciOiJFUzM4NCIsImtpZCI6IjczZWUwNDgzLTc1NGYtNDc3Yy1hZTQyLTBiMTQyMjNiYzA1YyIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiSlg3bWE2eTRrd0syUHhrQXgzajJKalpMWUZJa2ZibjMiLCJqdGkiOiI3M2VlMDQ4My03NTRmLTQ3N2MtYWU0Mi0wYjE0MjIzYmMwNWMiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoieklfR3paeWJqTi1tRUlQVnZxd2ZGUm5jU25DMzhJMTMifQ.W18i31VqtS3WORXfIAouSDAEAuiaLIDy0CvZ-R1t3gv3Hy7B1f9_eyZUyxDefZSnM2Y8t6ZSMWOEjGY0Y9fMWpxxUOc3mgVpJY676Koy24OZUZ-ABx149HKnpbES57m3' 
tenant =  'https://my-tenant.us.qlikcloud.com/' 
ID =  '5078a285-39f8-4bd1-8b1b-351d6cef77ea' 

p2q = pytoqlik.Pytoqlik(api_key=key, tenant=url, appId=ID)
data = seaborn.load_dataset('flights')

p2q.toQlik(flights, warning=False)
```

------------------------------------------------------------------------------------------
# toPy()
toPy() converts a Qlik objectID to a pandas DataFrame. You can fetch the Qlik objectID by right-clicking the object in view mode > Share > Embed. Then copy the objectID and use it as a string parameter in toPy(). Currently works for bar charts, combo charts, line charts, bullet charts, pie charts, treemap charts, gauges, KPIs, text widgets & other dimension/measure based objects.

toPy() returns an empty DataFrame if the object has no dimensions and measures. 
If there are dimensions but no measures, it returns all dimensions in a single column.
If there are measures but no dimensions, returns all measures in different columns, but all in a single row (with index 0).
If there are both measures and dimensions, returns a complete DataFrame as expected.

### Disclaimer
Empty dimensions (in blank) must be set to *null* in QlikSense. If an empty dimension is not set to null in QlikSense, an error will be raised. Please make sure there are no empty values that are not *null* in your data

### Usage:
```python
# If using Desktop Mode
toPy(objectID, qWidth=10, qHeight=1000, return_json=False, verbose=False)

# If using Cloud Mode
toPy(objectID)
```

### Argument breakdown:
| **ARGUMENT**    | **DATA TYPE** | **DESCRIPTION**                                                                | **DEFAULT**  |
|-----------------|---------------|--------------------------------------------------------------------------------|--------------|
| **objectID**    | string        | Qlik's objectID of the element you want to convert to a pandas DataFrame       | **REQUIRED** |
| **qWidth**      | integer       | Qlik's HyperCube width to extract from the object. Desktop only                | 10           |
| **qHeight**     | integer       | Qlik's HyperCube height to extract from the object. Desktop only               | 1000         |
| **return_json** | boolean       | Determines whether or not running toPy() returns the JSON format of the output | False        |
| **verbose**     | boolean       | Whether or not to print results in console                                     | False        |

### Disclaimer 
Qlik's data pages limit HyperCube area to up to 10000 cells. As such, until a better solution is developed, (qWidth*qHeight) must always be < 10000.
### Example 1:
```python
import pytoqlik
p2q = pytoqlik.Pytoqlik()

app = p2q.openApp(appName='MyQlikApplication')
# Now grab objectID of element you want to convert to a pandas DataFrame (right click on the object > Share > Embed)
app.toPy('aaWTm')
```

### Example 2 - Cloud:
```python
import pytoqlik

key =  'eyJhbGciOiJFUzM4NCIsImtpZCI6IjczZWUwNDgzLTc1NGYtNDc3Yy1hZTQyLTBiMTQyMjNiYzA1YyIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiSlg3bWE2eTRrd0syUHhrQXgzajJKalpMWUZJa2ZibjMiLCJqdGkiOiI3M2VlMDQ4My03NTRmLTQ3N2MtYWU0Mi0wYjE0MjIzYmMwNWMiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoieklfR3paeWJqTi1tRUlQVnZxd2ZGUm5jU25DMzhJMTMifQ.W18i31VqtS3WORXfIAouSDAEAuiaLIDy0CvZ-R1t3gv3Hy7B1f9_eyZUyxDefZSnM2Y8t6ZSMWOEjGY0Y9fMWpxxUOc3mgVpJY676Koy24OZUZ-ABx149HKnpbES57m3' 
tenant =  'https://my-tenant.us.qlikcloud.com/' 
ID =  '5078a285-39f8-4bd1-8b1b-351d6cef77ea' 

p2q = pytoqlik.Pytoqlik(api_key=key, tenant=url, appId=ID)

# Now grab objectID of element you want to convert to a pandas DataFrame
p2q.toPy('cVnYs')
```

------------------------------------------------------------------------------------------
# openApp()
openApp() is a method called on a Pytoqlik object previously created. This method is used to open and display a Qlik Application inside your Jupyter Notebook or redirect you to it in your web browser.
If there are no Qlik Applications with the name you input, this method will create a new Qlik Application with the specified name and warn you about it.

Qlik Cloud versions use a different kind of connection to applications, and as such, this method does not work for Qlik Cloud. Instead, it returns a message asking for a new Pytoqlik() object pointing to the new app to be created, and redirects you to the original object's URL in your browser. (Does not work inside Google Colaboratory).

### Usage:
```python
openApp(appName='PythonApp', sheetName=None, redirect=False, embedded=True, width=980, height=800, verbose=True)
```

### Argument breakdown:
| **ARGUMENT**  | **DATA TYPE** | **DESCRIPTION**                                                                                                                        | **DEFAULT** |
|---------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------|-------------|
| **appName**   | string        | Represents the name of the application you want to open. Do not include the .qvf extension, just the file name                         | "PythonApp" |
| **sheetName** | integer       | Select which of the sheets inside the application you want to open. If left on None, openApp() will open the application overview page | None        |
| **redirect**  | integer       | When set to True, executing the openApp() method will open the Qlik application in your web browser                                    | False       |
| **embedded**  | boolean       | When set to False, openApp() will not display the embedded Qlik editor in your Jupyter Notebook. Useful if using redirect              | True        |
| **width**     | integer       | Set embedded display size width in pixels if using *embedded*                                                                          | 980         |
| **height**    | integer       | Set embedded display size height in pixels if using *embedded*                                                                         | 800         |
| **verbose**   | boolean       | Whether or not openApp() will print out results in the console                                                                         | False       |

### Example:
```python
import pytoqlik
p2q = pytoqlik.Pytoqlik()

# We wanna open the app inside our web browser, so change redirect to True and embedded to False
p2q.openApp(appName='MyQlikApplication', redirect=True, embedded=False)
```

------------------------------------------------------------------------------------------
# listApps()
listApps() is a method called on a Pytoqlik object previously created. This method is used to list and display all Qlik Applications currently saved in your host. When called on a Pytoqlik object in Desktop mode, returns a pandas DataFrame containing the application name, it's path and file size. When called on a Qlik SaaS object, returns a pandas DataFrame containing the application name, it's AppID and file size.

### Known Issues:
Qlik Cloud version of listApps() return a somewhat random selection of apps, and also, not a complete rundown of your tenant. This might be due to permission issues and a connectivity issue. We are still investigating this. We remind you that PyToQlik is still under active development, and as such, issues are to be expected.

### Usage:
```python
listApps(return_json=False)
```

### Argument breakdown:
| **ARGUMENT**  | **DATA TYPE** | **DESCRIPTION**  | **DEFAULT** |
|---------------|---------------|------------------|-------------|
|**return_json**|    boolean    | Whether or not calling this function returns the JSON file the API provides|False|

### Example 1:
```python
import pytoqlik
p2q = pytoqlik.Pytoqlik()

p2q.listApps()
```

### Example 2 - Cloud:
```python
import pytoqlik

key =  'eyJhbGciOiJFUzM4NCIsImtpZCI6IjczZWUwNDgzLTc1NGYtNDc3Yy1hZTQyLTBiMTQyMjNiYzA1YyIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiSlg3bWE2eTRrd0syUHhrQXgzajJKalpMWUZJa2ZibjMiLCJqdGkiOiI3M2VlMDQ4My03NTRmLTQ3N2MtYWU0Mi0wYjE0MjIzYmMwNWMiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoieklfR3paeWJqTi1tRUlQVnZxd2ZGUm5jU25DMzhJMTMifQ.W18i31VqtS3WORXfIAouSDAEAuiaLIDy0CvZ-R1t3gv3Hy7B1f9_eyZUyxDefZSnM2Y8t6ZSMWOEjGY0Y9fMWpxxUOc3mgVpJY676Koy24OZUZ-ABx149HKnpbES57m3' 
tenant =  'https://my-tenant.us.qlikcloud.com/' 
ID =  '5078a285-39f8-4bd1-8b1b-351d6cef77ea' 

p2q = pytoqlik.Pytoqlik(api_key=key, tenant=url, appId=ID)

p2q.listApps()
```

------------------------------------------------------------------------------------------
# fetchData()
fetchData() is a method called on a Pytoqlik object previously created. This method is similar to the toPy() method in the sense that it extracts data from the application. In contrast to toPy, you don't have to pass an object to fetchData(). You instead pass it some dimension, give it a label, and then you pass a list of measures, and finally a list of measure labels. This method returns you the data filtered using Qlik's Associative Engine inside a *pandas* DataFrame.

### Usage:
```python
fetchData(dim, dimLabel, measures=[], measureLabels=[], verbose=False)
```

### Argument breakdown:
| **ARGUMENT**  | **DATA TYPE** | **DESCRIPTION**  | **DEFAULT** |
|---------------|---------------|------------------|-------------|
|**dim**|string| A string containing the script variable used as a dimension inside an object|**REQUIRED**|
|**dimLabel**|string|A string containing the name of the dimension selected. Used to name the DataFrame dimension header|**REQUIRED**|
|**measures**|list of strings|You must pass a list object containing the strings of the measures you want to grab the data from|**EMPTY LIST**|
|**measureLabels**|list of strings|A list object containing the strings naming your measures. Used in naming the DataFrame headers|**EMPTY LIST**|
|**verbose**|    boolean    | Whether or not calling this function returns verbose data|False|

### Disclaimer
This function currently sorts by a single dimension, since multiple dimensions are created inside Qlik as different HyperCubes. To sort this, you might want to call fetchData for all dimensions and concatenate/work with the resulting DataFrames.

Also, since once again, Cloud applications are referenced directly on a Pytoqlik() object, you must call fetchData on a Pytoqlik() object, while Desktop applications you must first open the application using openApp(), then call fetchData on that object, as shown in the examples below.

### Example 1:
```python
import pytoqlik
p2q = pytoqlik.Pytoqlik()

app = p2q.openApp('MyApp', embedded=False)

# "MyApp" has seaborn "flights" data in it
app.fetchData('year', 
              'YEAR', 
              measures=['sum(passengers)', 'avg(passengers)'],
              measureLabels=['YEAR_TOTAL','YEAR_AVG'])
# Should return a DataFrame with 3 columns: one is YEAR, one is YEAR_TOTAL containing Qlik data that equals that of "=sum(passengers)" and the last one is YEAR_AVG contaning data equivalent to "=avg(passengers)"
```

### Example 2 - Cloud:
```python
import pytoqlik

key =  'eyJhbGciOiJFUzM4NCIsImtpZCI6IjczZWUwNDgzLTc1NGYtNDc3Yy1hZTQyLTBiMTQyMjNiYzA1YyIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiSlg3bWE2eTRrd0syUHhrQXgzajJKalpMWUZJa2ZibjMiLCJqdGkiOiI3M2VlMDQ4My03NTRmLTQ3N2MtYWU0Mi0wYjE0MjIzYmMwNWMiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoieklfR3paeWJqTi1tRUlQVnZxd2ZGUm5jU25DMzhJMTMifQ.W18i31VqtS3WORXfIAouSDAEAuiaLIDy0CvZ-R1t3gv3Hy7B1f9_eyZUyxDefZSnM2Y8t6ZSMWOEjGY0Y9fMWpxxUOc3mgVpJY676Koy24OZUZ-ABx149HKnpbES57m3' 
tenant =  'https://my-tenant.us.qlikcloud.com/' 
ID =  '5078a285-39f8-4bd1-8b1b-351d6cef77ea' 

p2q = pytoqlik.Pytoqlik(api_key=key, tenant=url, appId=ID)
# App has seaborn "flights" data in it
p2q.fetchData('year', 
              'YEAR', 
              measures=['sum(passengers)', 'avg(passengers)'],
              measureLabels=['YEAR_TOTAL','YEAR_AVG'])
# Should return a DataFrame with 3 columns: one is YEAR, one is YEAR_TOTAL containing Qlik data that equals that of "=sum(passengers)" and the last one is YEAR_AVG contaning data equivalent to "=avg(passengers)"
```




