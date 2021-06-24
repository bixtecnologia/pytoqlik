# PyToQlik basics
Hello! This tutorial is a short introduction to some functionalities the PyToQlik library offers. We will be exploring both the Qlik Cloud SaaS version and Desktop version, since they connect and handle some methods slightly differently to accomodate their respective APIs. However, this tutorial in particular focuses on the Cloud SaaS version.


# Table of Contents
- [Installation](#installation)
- [Qlik Cloud SaaS Tutorial](#qlik-cloud-saas-tutorial)
	- [Importing what we will need](#importing-what-we-will-need)
	- [Generating an API Key](#generating-an-api-key)
	- [Creating the connection to a Qlik application](#creating-the-connection-to-a-qlik-application)
	- [Inputting data into the application](#inputting-data-into-the-application)
	- [Some manual work: creating an example chart](#some-manual-work-creating-an-example-chart)
	- [Extrating data from an object](#extracting-data-from-an-object)
- [Closing thoughts](#closing-thoughts)



# Installation
First things first, we download and install the library using pip:
```
pip install pytoqlik
```
We are now ready to start using PyToQlik to extract and modify data in your applications. It is also strongly recommended that you use [Jupyter Notebooks](https://jupyter.org/) as your IDE, since they support **IFrame object embedding**, a core feature of PyToQlik. You can also preferrably use a cloud service that provides such functionality, something like [Google Colaboratory](https://research.google.com/colaboratory/). 
*Tip: to install libraries in Google Colaboratory, just put a "!" character before "pip install \<lib_name\>" and run the cell. The interpreter understands that command as a "run in cmd prompt".*

# Qlik Cloud SaaS Tutorial
For this tutorial, we will be using the forementioned Google Colaboratory to import some data into a previously created Qlik application. We will then attempt to extract part of the data that is contained in a pie chart object visualization, put it into a pandas DataFrame structure, and finally perform some operations on top of the extracted information as part of a data science experiment. Let's get to it:

## Importing what we will need

First, we open a Jupyter Notebook and begin by importing the libraries we will use throughout the tutorial. Our first cell consists of:
```python
import pytoqlik
import seaborn        # Seaborn provides us with some sample datasets
import pandas as pd   # We will need pandas to manipulate the extracted DataFrame
```

## Generating an API Key
*Some of the steps will require you to manually work on either your tenant or your application because the Qlik QIX API, which PyToQlik uses to communicate with your cloud applications, is somewhat limited in what it can do. The next step is logging into your tenant and creating what is called an API Key. To make this tutorial shorter we supressed some of the steps, but you can refer to Qlik's API Key tutorial [here](https://qlik.dev/tutorials/generate-your-first-api-key)*.

Assuming you followed their step-by-step, that your tenant has already enabled API Keys, and also that you already have the **developer** role in your tenant, as per shown on the link above, we will proceed here by showing you how to create an API Key and input it to PyToQlik.

Go to your **profile settings** window, and under **Management** go to the **API Keys** section. If you have the **developer** role, a **generate new key** button will appear on the top-right corner. Clicking it will open a a window that allows you to input a Key description and an expiration period, as shown below:
![Key setup](https://github.com/BeautyFades/pytoqlik/blob/BeautyFades-sprint-wk3/docs/images/generateKey.png)

Upon generating, the API Key is displayed one time only, so copy the string and don't lose it. Although you can always delete lost Keys and generate new ones if it ever expires or you accidentally lose it.

![Api key](https://github.com/BeautyFades/pytoqlik/blob/BeautyFades-sprint-wk3/docs/images/key.png)

## Creating the connection to a Qlik application

With the Key in hands, we are one step closer to connecting to our tenant. There's a total of three strings the library needs to be able to connect to your apps: the **API Key**, **your tenant's URL** and the referred **appId**:

 1. The **API Key** we already got.
 2. The **tenant URL** is the address used to get into your tenant. It usually has a formatting like https://my-tenant.region.qlikcloud.com/. You can copy it directly from your browser. An example of a valid URL would be: https://pytoqlik-bestlib.us.qlikcloud.com/.
 3. The **appId** is once again, part of a browser address. Since the QIX API connects directly to applications, we need to inform its ID manually. To get this identifier, all we need is to open the application we want to connect to in the browser and look at the address. **appId** usually has the format xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx. An example of a complete URL is: https://pytoqlik-bestlib.us.qlikcloud.com/sense/app/5078a285-39f8-4bd1-8b1b-351d6cef77ea/overview, which is the overview page for the application, and the ID in this case is "5078a285-39f8-4bd1-8b1b-351d6cef77ea" (everything that is after "/sense/app/" and before "/overview").

With these three, we can write the second cell in our Jupyter Notebook as follows:
```python
key='eyJhbGciOiJFUzM4NCIsImtpZCI6IjczZWUwNDgzLTc1NGYtNDc3Yy1hZTQyLTBiMTQyMjNiYzA1YyIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiSlg3bWE2eTRrd0syUHhrQXgzajJKalpMWUZJa2ZibjMiLCJqdGkiOiI3M2VlMDQ4My03NTRmLTQ3N2MtYWU0Mi0wYjE0MjIzYmMwNWMiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoieklfR3paeWJqTi1tRUlQVnZxd2ZGUm5jU25DMzhJMTMifQ.W18i31VqtS3WORXfIAouSDAEAuiaLIDy0CvZ-R1t3gv3Hy7B1f9_eyZUyxDefZSnM2Y8t6ZSMWOEjGY0Y9fMWpxxUOc3mgVpJY676Koy24OZUZ-ABx149HKnpbES57m3'
url='https://pytoqlik-bestlib.us.qlikcloud.com/'
ID='5078a285-39f8-4bd1-8b1b-351d6cef77ea'

p2q = pytoqlik.Pytoqlik(api_key=key, tenant=url, appId=appId)
```
**key**, **url** and **ID** are all strings containing the API Key, the tenant's URL and the application ID as we got it in the browser.
To effectively create the connection, we are going to instatiate a Pytoqlik() object. Let's call it **p2q** and pass the optional arguments *api_key* to be the key we generated, *tenant* should be the URL to the tenant, and *appId* should be the ID we copied from the application's overview page, just like shown above.

As soon as we run this second cell, we should get a message saying the object has been pointed to a URL which uses a WebSocket Server and return the API Key used. Upon successful connection, a message displaying either **SESSION_CREATED** or **SESSION_ATTACHED** shall be shown. A new session is *created* when the user who owns the API Key used is not currently logged into the tenant, and it is *attached* when sharing a session. Both connections function effectively the same.
![Successful connection](https://github.com/BeautyFades/pytoqlik/blob/BeautyFades-sprint-wk3/docs/images/code.png)

**Congratulations**, we are ready to call methods on top of our application!

### Connection troubleshooting
If the cell returns a "*Handshake status 401 Unauthorized*" error, it means that your API Key and tenant do not match, and that authentication has failed. Causes are probably a **typo in the tenant's URL**, or a **typo/expired API Key**.

If a "*Handshake status 404 Not Found*" error appears, it most likely means the **appId** you inputted is wrong/mistyped, since the WebSocket connection couldn't find the server the API connects to.

## Inputting data into the application
Alright, we finally got our **p2q** object pointing to the application, and to which we call our library's methods. In this experiment, let's get some sample data from the *seaborn* library and import it to the application. In order to set the data in an application, PyToQlik has a **toQlik()** method that **sets its script to match a pandas DataFrame data**. Let's see what kind of data *seaborn* can provide us. Our third cell consists of:
```python
data = seaborn.load_dataset('flights')
data
```
This returns a pandas DataFrame containing 144 rows and 3 columns of sample data. We have flight information containing flight year, month and the number of passengers. 

![pandas raw data](https://github.com/BeautyFades/pytoqlik/blob/BeautyFades-sprint-wk3/docs/images/datapreview.png)

Let's get this information to our application using **toQlik()**. The fourth cell is:
```python
p2q.toQlik(data)
```
Note that we called **toQlik()** in our connection object, since that object already has all the information about authentication, which tenant and which app it should modify. However, this method currently replaces all the data inside the **Data load editor** of the application. So, there running this cell should prompt us with a warning telling us exactly that, and awaits a Y/N confirmation. This behavior can be toggled on and off by passing the optional argument *warning=False* when calling **toQlik()**. If we either do that or just answer with a "y", the data should be imported into the application and we can start building visualizations with it! Let's check on the Data load editor page:

![Data Load Editor](https://github.com/BeautyFades/pytoqlik/blob/BeautyFades-sprint-wk3/docs/images/importeddata.png)

Looks like our data got passed as a .csv file, separated by semicolons (;), and headers were fetched for us already. If you check the documentation, there are also some other customizable settings like changing the separator character, or the decimal separator, and you can also pass multiple DataFrame objects in a single call of **toQlik()** (they will all be loaded one after the other automatically).

## Some manual work: creating an example chart
So we now have an application with data in it. Let's go ahead and create a visualization and proceed to explore some other functionalities in PyToQlik. For this tutorial, we will create a pie chart in Qlik Sense, and then extract the data in it. 

Let's open our application in the browser normally and build the pie chart displaying the total number of passengers per year. Our dimension is "*year*", and as a measure we will add "*Sum(passengers)*", like shown below:
![Pie chart creation](https://github.com/BeautyFades/pytoqlik/blob/BeautyFades-sprint-wk3/docs/images/creatingpiechart.png)

Let's also change the measure and dimension labels so our data is a little prettier. We are changing the pie chart's limitation value to 20 so there's not an "Others" dimension with the rest of the data condensed into it. The completed pie chart looks like the one in the image below.

![Completed pie chart](https://github.com/BeautyFades/pytoqlik/blob/BeautyFades-sprint-wk3/docs/images/piechart.png)

*Please note that this is just an example, and data can be extracted the same way as will be shown shortly from all  other Qlik objects that may contain dimension and measure information, such as bar charts, KPIs, scatter plots, gauges, etc...* 

## Extracting data from an object
In order to retrieve the information contained in an object, we will use the **toPy()** method. This method takes in a single parameter called **objId** (not to be mistaken by the *appId*), and returns a pandas DataFrame with all measures sorted by dimension. In order to accomplish this, we then need to find the object's ID value.

To do this, all we need is to leave the **"Edit sheet**" mode on our application in the browser, right click on the object (in this case, the pie chart), then go to **Share > Embed**. In small letters, under the preview section there will be displayed the object's **Object ID**, just like shown in the image below:

![Object ID acquisition](https://github.com/BeautyFades/pytoqlik/blob/BeautyFades-sprint-wk3/docs/images/objid.png)

Finally, with the Object ID in hands, all it takes is a single call to **toPy()** to get what we want. All we have to do is pass it a string containing the Object ID of the object we want to take the data from. Therefore, in this case, the fifth and last cell in our Notebook consists of:
```python
p2q.toPy('qCZbkW')
```
Which returns, for the data we provided, a DataFrame containing every year, and the sum of passengers in that year:

![resulting data](https://github.com/BeautyFades/pytoqlik/blob/BeautyFades-sprint-wk3/docs/images/outputdata.png)

We can always assign this DataFrame to a variable to save it, and then perform as many operations as we want with it. If you are a data scientist in Python, *pandas* is most likely your best friend, and the possibilities and analysis you can now perform is much, much higher. You can extract and input all kinds of data in machine learning algorithms, you can format and reformat structures, save them in a variable and input them back into the application by using **toQlik()** once again, you can perform regressions, trend predictions, etc... all using other Python libraries.

Note that the data we got is not what we originally inputted with **toQlik()**, but instead is literally what is displayed in our pie chart. The headers of the DataFrame are the labels we set in Qlik, and the measures are the expression we set for them, that is in this case, *Sum(passengers)*.

And also note, any changes you make to the object are saved automatically since we are in the Cloud. The object ID of an object does not change if you change the parameters of the object, and as such, every time you cast **toPy()**, the most current data is extracted. This means you can always edit your object whenever you need, rerun **toPy('objId')** and you will have an up-to-date DataFrame object at your disposal.


# Closing thoughts
PyToQlik is still under active development, and many more functions are expected to be released. But most importantly, we plan to add robustness to the code, as in, make it more streamlined, less prone to bugs and connectivity issues, especially for the Qlik Cloud SaaS version.

We also have the .ipynb file used to create this tutorial available [here](https://drive.google.com/file/d/1vk5AZ3pg4oHG4bgfYkF4AhdKq5XDiAws/view?usp=sharing).

If this tutorial was helpful for you in any way, please consider sharing it and also the library. The larger the community gets, the better and more focused we can collectively develop.





