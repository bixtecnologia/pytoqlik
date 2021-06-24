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
![Key setup](https://lh3.googleusercontent.com/HXIyxUDWi0vcmbzPC4FSpEzUcMwpU6VXNdTqoY_cItx4GuzkKb0h6HD_LjYVhoo4OvpifrclDw6KJaF6gujnM6ohyVUPtKdFHnS8mkg9qspIM0FAfHpkqz2Gesax7ENppSKHEkQnV60fLvCalHh8E4yWUC94TL2mNNmqqYmq4cDAAfhENY_0v6B7207V5W-coHq-re_2lWR55Xgr8xbwhhLMvxQaAwTcAL3BA2jRSSgKhaSmc_VquoxZFlSfhyNwSD7tFkXYMimW9JeY6Mw9jTzp6qiPCXplF6gH97a7A2nSeiS7mP7GHPmUoum8yiSjUnDK65P-Gn8jJ7ISPCbmq_bE0lWyU74Ink0AdAD4LF4mjFORXqOc37EpvsMzdqXH7djCY6_V1Skna9pn7YmPNC_0W5BwtyHU2tK3Tku7wJfv4Mwo1Sa-XTs2WYv_VmO7SV6R_n-xihpWj0dl06Tckm_QveC91UyGHp2bl1pkKOGRmlY5WWPNZ3RQb_1yBfvPvv03PQvIUb00VOxhuqOFmgdTJOsdixhfwX9RjArvs8kxVlRCeOZ3zncqhBJ_ls-E4jA0rp3HMKQGq5_Tex2vizxLHX4axcgnVnsgXHOsu6EXym0DHMIwx8Vb-OpZarOLXMBJKDie31bnZwnoCKoGmbPriUJjkBLXkIt_-cpTZ8YtzSx2ZjGKAiOpxydOILn4g9N89MhmrzTKx2GOq8p_0jU=w1907-h478-no?authuser=1)

Upon generating, the API Key is displayed one time only, so copy the string and don't lose it. Although you can always delete lost Keys and generate new ones if it ever expires or you accidentally lose it.

![Api key](https://lh3.googleusercontent.com/zgMyID37jZnr_DkXKCd2riuQIB1mp208b9VRVjvMgwITaDSC4etZFdBEM2y9R_8NR8Hse4yzSIHEi14Uo9eTg2OSz_bqqooR9n_N-6TEYjfsd-BWvK2GSIIYhuuwbfcz2Iv9W5DEyJt7Az0nd9_2AWRqK_lGJgPfAWTcrFDHeDu7Fv6OjwPktM4FtNVRiW4LNfSji7N8IPlz2oSZD7IDpawUIZ2V-ceLA3HFPCOKs9Fo-YyV1SnojkYdJY1sqAzsWXs53mKExcs_muBbM-EOgrX99e50oUH8zWu51sRL8ccT_5xLSHVcvoD9r2WTXNMzDWKXSlJw3_ouF27acm28SCiWL2cvnvhidK4E0pLkRzxAD-iEHEaTspEXyl3XPKGKwPtGUXcYeB-7HOi7ywlCPtBXVtxvZW0wSfuw4eeUmeN6c2Pi8tKjajdMetj4WtMcONOHFVSXODDcxffoXYeceTdqsOsTUdQUIvJurZRdH2peLqAePFA7MHQktxGKL1DNdNeQQPW6rmTobb5H-EeGgVKxQiB6f3Dj2y8r9oICUrqWroe9Hkj6UE3REfKWpTceIy13ChiNli2j5HloLnQdJoiK54e6K3ql2qxQlpKCjfKWpFktE0VfYvmj5UtP5oCl09F-CWw0ToPlhzx-HJQ2njqcHchvGCV9LKBasaQzYqK0Z5zZUh6YhmgDSq4pgifuTKwtquJ3BrrU6-ocZPY02Qk=w554-h537-no?authuser=1)

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
![Successful connection](https://lh3.googleusercontent.com/CqyKEEP22cUKhWiqvZVDxKFM9OAIb_uW6VGw6e8GWXuKYebwahq54O50oA4bdZhVHemGCXll_CRh7LNxMpoWMeQ44FLpM73yxwvHE6gC0IGYsAMMkRaUm9G81UInakz154nEEZBs64FIiLQCEXynTc1Xjv5Rz5_nu57cdlKPsNl3Z-moDNQUTEej8FHe2b-3YC1nVmNZ9v-E-KpJfGX4KgJFfad9I4Am3uPZppW6YFZkcBpzxT6l7VHnfdjI4mJ9HbfmxTLhQqcJx0OCft8eBOCG-NMpQ4M1QndH7fzZIwO3tf6DeXjTqTHdCTuMGuJmwkXqMOiwZJLo206VSfBTbJmDG0xSyrggbybyK5V4U98nJyCWL2Fy0lJcL_DIq7ATjybubGQ7KH1UxZm5nH3q-HqTdj_54kWmUOz1x84x4IvyyNKz7lBB2Gy4zWOo4mnKIc4wMmTFtsfTAlvSCiJtG-TyyN_FBJ9lOc3A1Z2JaQDWiVKsawK3zRARDWPG8kSkCTrRUeGSbTW2u-Nwtc81TrRNaiItC58Eq0Uj9dQpKffLdkrWgz1GZzyU2Kkhm9zBqcfkvJE-pZf9MsFbw8zYqz6otjorPqxDQ_CXFa2f93toQbZGHYtXTJzgf1yUgw1MIF4TjICyJPMbu2evA_e33pjOgHm-sch4901e5oOQDH3p8pIHdwD9MnR9FPLYxXnGaSfcCPgQgTZ0lsqQVooQodE=w801-h151-no?authuser=1)

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
![pandas raw data](https://lh3.googleusercontent.com/JUFkBYnDdBi9T8OhW79else4az8dNnh0NPbHrXFecSHvSlnUYI75gGg0LwMTVSMOQYc2AMYK92zoi_-jw2QKyks57re2Kh9dz8XzDSdllAD2MpS6_wM807ymqpNuouHM5Fj_JXzabc4L55uSC9gbC92B9xU3acsLU6fFCO_XM67bHmhRCjVzr3x_IL0slvWLamR1vc71yDlndUCrMdiROx-h5iRVqu4mlf2YcPfu-1E4pZuHon0rc2U-Gle2bD7fQK6N7kwdBwHrvjOCcjYbksScvOfvO5O9nFvdIY7fyCPstP1-Yw-iBmFDbg5sSHMa_uTM0Ct43QRE3JmEsMTQL4VsuWcOc4jndykxL6mCPEWKRuxPla11v4_rp-1rqg2CWiHiYaVoIfTuUpdrstTUVqXcJnN-4XHYSt6lBFapzQjz218lNbtfrvLmD1DSjx4ccqFeNYGA3NNMV-Byle8byu4Z4QtQsbR14xFYXgyQmUlpMY_RXcZrBvv5vePFqkM8R3FfAjjrBCVpuTeelQB0KBMc5dIjwby-vqnBRvTA9KYoOmztFo1OPd0u6Q9m_Ah4IX4eqqX9gQkM-m20l0Iorfn8dROlDX46xpQ-ql_-NNeiPM0d2wIPh5c1ZeE6ZlTW6qYHfRCRahDwZ94dtW-NIpu1AkqMZnSdB-Y4dBUTgC0lIBMvEu1h0j_NZ68vIr3gFpmjqQmQMn8J3bSbiGu8U3Q=w337-h465-no?authuser=1)
Let's get this information to our application using **toQlik()**. The fourth cell is:
```python
p2q.toQlik(data)
```
Note that we called **toQlik()** in our connection object, since that object already has all the information about authentication, which tenant and which app it should modify. However, this method currently replaces all the data inside the **Data load editor** of the application. So, there running this cell should prompt us with a warning telling us exactly that, and awaits a Y/N confirmation. This behavior can be toggled on and off by passing the optional argument *warning=False* when calling **toQlik()**. If we either do that or just answer with a "y", the data should be imported into the application and we can start building visualizations with it! Let's check on the Data load editor page:

![Data Load Editor](https://lh3.googleusercontent.com/kXCutvU_IwF-88KD08ZDzEMb2qYYngM7qQi4j4zsztD9H4DZkAQmBmwwyudKONq-fCp-3jd92lkMV_lzf4hhtRQ07c4vVi5gOaPt_ye7MDhr4rxdD7l6-_C7uCsyPbsHCQ9jTIHKMY96Rrg61Hyw3WVgjghOjZXsmMOwbmepXsGDV6DX2a6RsmpxO_l4zPffI_U7u3OZAD-PeIMi2Fnotg57cU5oWYlc89JH3LaODpBHixeM51hUR7KGkepDBKbqEAzkHgU9_sgpw13vLNU6GjMJaI8sVTpwyUl3JDSktcvuMmDrelcy86RD6T6DsFS32WnXzIVHa3uXVBqbOARewKluCrGUey03tZVpcfEuI1QKsUhpztWJ25fMLn29ZkG-D2pC_LyFF1AfZ-gfZ1ZblOY4eFdluAFZc36CZ2UKMQvArDCMpEDWFD9HfuL8IXT6NyxlCfm3gqYSXSVOhBwMdjK73drnPtkM8eiNCRqPAHUfKuTZUp5msfTpy0wGWkTQ9XBtpHnnnsDdGvevisIp6I4URv9ip64jMFI8hSiat8pJFy6UNcp4RfnFR6isyq9WmC0lBYaFnwy-aJaawA1yEOPd8_3TXaW3FCxKMj9fRo8xdBIhLlJ0We5GcT9glDdKSDXImCnO3YCOQSpfzmG_s6-Qu6EZqOYQBV9-MmnAd5yVZ7bBBplCk4QyS0ICiEvBSt4fMQYX7rrT6CKwkJWySm0=w675-h438-no?authuser=1)
Looks like our data got passed as a .csv file, separated by semicolons (;), and headers were fetched for us already. If you check the documentation, there are also some other customizable settings like changing the separator character, or the decimal separator, and you can also pass multiple DataFrame objects in a single call of **toQlik()** (they will all be concatenated automatically).

## Some manual work: creating an example chart
So we now have an application with data in it. Let's go ahead and create a visualization and proceed to explore some other functionalities in PyToQlik. For this tutorial, we will create a pie chart in Qlik Sense, and then extract the data in it. 

Let's open our application in the browser normally and build the pie chart displaying the total number of passengers per year. Our dimension is "*year*", and as a measure we will add "*Sum(passengers)*", like shown below:
![Pie chart creation](https://lh3.googleusercontent.com/ch331HDP6feViP0XJztoQuHAZyqSxWvhgr5rggCgosl_9ChHHkGZulYLOyZJWod7aaDPVHcrGa8a-Jl-Mo7I4d_CBSG365ip7A-sAMTI-2loXAzNarzSf1zoSm2CEbYP-Tsx8rR4gu7tXO_Be6WuAwSrGuuu25b_8V_ENAvVYPtFa38Z7WjGnSEkcupmf8PJSTOiDaWcly_2zMW_aqOZ6bkNxhJpxRG0N7xtmxrlmqBNZv7QwCf0EpZer5N4J6OflOjNY5jqwCy_Osgt1Wg6ynwknePkwutNbEJNIMxIpavMwB140nXY4qappvstlhV8jers2hEThuJGA4EB5OWhw8iNFgDw7syfvANkNFxGNbgz0NsVHnYcVZQ4Ku6cVdGoUA6vHjvlDT4SBZTB1oJn_kausZdVe35HnwQ0P57uu8hx-0P1zlPr4dq6VatUUNMzkP-aEpH7bTXKdryqfT8eWpUMmQTSZ5NBL4KH2_VMSgcb2LMNWGKjAgCJck3DcmOC9dUDOy-yi9m9cfKrtzpUNFVeThenwdB_07MrgDHTA4x3VNQFq9wKVscUJICMw-Cb0rY4fw9oRuE1sJ6tXFiRyYZYUqc2czFajHsZh6r2gOVYjANbuZ-x74hjihjlM2Ns0Aeccy5BmEXPT3OyLHGN5k2fEP0L1kbNNqNpYBdBFTup1sE4IgtFi0ZHPX3fW8D3wYEJ9Jc_RNfn35KI3ejIYCE=w715-h465-no?authuser=1)
Let's also change the measure and dimension labels so our data is a little prettier. We are changing the pie chart's limitation value to 20 so there's not an "Others" dimension with the rest of the data condensed into it. The completed pie chart looks like the one in the image below.

![Completed pie chart](https://lh3.googleusercontent.com/H6crrHGdeCSFyj22NNhfx82T_uzoJEBm0uXoYLxn5AmqSfodEZR6CsOUG6_-hveV7vKChgqzzuEvvbI6S8vdBkyCE5pZ6EpuKwSE24p65adrRwBkJteN5LXPVedlWDQVce4rzuJ8zY0Ewqil-zEG9eUe4qkPD2vzOxoC6DOO44xNaUN3GSc9E0bw5YWuBYNWCy0tzis8bGBi7Ni7rxDOJn9_33sLTEHDcmU63310GV8zh-xNyrmISM0Gfylf6KUGPiZEvJtsgsRs2IhiOoLj923O6IzuXoQtzwTK007CZ_L8WL1bbjd2EYgZr_j4U7yNRJbchTy8OSA0qzL8D1PD_awEtnDx_M3wPphIB49DdoWa1_WctmTaEXbggB6KpFV-AbJgAbOqKopX4d-i4F5JuTIoezTD2NkGw7qfiPw0BL_rBzTKci8wdAE70NDR-ih4OaYLeRre4zW83lDyvuGvpbnaBcVPJCSn1Ci2An4tlHVSMvI3kLxzPqHb-m-VY3cCigMFIibMlpJYODRVfPpv6nXZlrgwkKl-tgU8S28_kLzBmjv5G0gd1frsz4S3gCohVbZKTlpaCB-Xuq41C6WwQcJoHIo2PA3Hnu3JxrwXRfboMv6NFba_pJ7gtk5sfb0yO1qQhqbBYxD4A88tPHPcu4ejgbGWzvg_DeihWQ1-LoDOlnhIIL6MtuI-e2kaes8W18y0rBEKUXBSM0V0glrBVcQ=w959-h462-no?authuser=1)

*Please note that this is just an example, and data can be extracted the same way as will be shown shortly from all  other Qlik objects that may contain dimension and measure information, such as bar charts, KPIs, scatter plots, gauges, etc...* 

## Extracting data from an object
In order to retrieve the information contained in an object, we will use the **toPy()** method. This method takes in a single parameter called **objId** (not to be mistaken by the *appId*), and returns a pandas DataFrame with all measures sorted by dimension. In order to accomplish this, we then need to find the object's ID value.

To do this, all we need is to leave the **"Edit sheet**" mode on our application in the browser, right click on the object (in this case, the pie chart), then go to **Share > Embed**. In small letters, under the preview section there will be displayed the object's **Object ID**, just like shown in the image below:

![Object ID acquisition](https://lh3.googleusercontent.com/rHbDl_kTxixWdPi-4SaL0awpFLh-gZwxWoHrvgwaMX5qp7DMqjj7NX5W29ZySPKoLf29DbnIP77_B1iXbX3-b32Uf_xe8LmfK8gMkbqwRr-ym2tcjbylWwseSDpMS62WJohTmibFs7eEBr6knHLj68hIAF7ETcUGuTEDYRjj3TlmdoMOuXo0COsJYET3c7LVJobA6QCGUzLQdNRMzZkGeNluE6tg1Rw2XfZ6-3pO-joCFeEqV-NeYR4qA7WBqSvWlt3aysky5mr1gfAel11x1-StsIz0i1dumd_iYiT2TWoDHNnvUxunI01TgC0eQs50WnFWy9ob7Yj2bs9EzCX1X3LVQKPFGp1A3XL4oe1vVZBxVT6k8SZLGu0655NUeC6sJYy9nhtOXpCa1HMnEdh-8eFLlvmBSJgOa1SlFFF71XWffoh4WSUqUoicS0dljqox6Z5ZNFVHknQe5FN2JG7OnB_DEs2uFNdalrihiHATF4YydsrLUDZTAaCUSmmNf_gncW1hnLnzsS9NaqTyIsuFmI5Lqyo9hGaaLUPK1ckwKYKW_MFPSDWkqQkbHnmUtspwP_UYf2RQ4u7uTmwZlNhtN4o84EnwYi7GqryGRa-8ynuavu4bdXW5zgt_W0T4deu0VFiSCxcfNkiHvpRR0fqiVCWXmSmgGq3tjsudz-9gQTIlX0jXtS5iNqRgdHZFrfaun7FSrEwm7lJ2DvsSJ2WLa4I=w1250-h603-no?authuser=1)

Finally, with the Object ID in hands, all it takes is a single call to **toPy()** to get what we want. All we have to do is pass it a string containing the Object ID of the object we want to take the data from. Therefore, in this case, the fifth and last cell in our Notebook consists of:
```python
p2q.toPy('qCZbkW')
```
Which returns, for the data we provided, a DataFrame containing every year, and the sum of passengers in that year:
![resulting data](https://lh3.googleusercontent.com/EZoRPEPTGBcn78DmyhpPp9rETkL-w0IwtI4XxC5258LrPtykbmU9PnrPTmEXA1Mri71wECTxuoqjkVcXb8SD6IIZ1GcNeRdMOMMEnR-UI1Bv1y35kq_go42mTDoRo0nVjAx8HJe80F6atVBI1vw43PPYtaQqcG-hZno1cbR4iio0pJoy4uQdZJCtU2GYWCA9HSsPZnOX4X8KRWDvIiIWulSFQNyn65FX7IOfAAYJ2bfPguaTD35NyxkJeO1Pp1TyH631rTcQcrCYqfWYTZKw9D6MdPdlpPixqMK3lqg7qB5cBo_nFsZM7GnrV-S0T_wXTZnVDaYrLXmbMIc2mmRJjDZcGEoRzLpFx9qaa-uZC1g_CpYMorIkVWuZ1coCsIjiPvaUn-LoEA0e8iVLdPmCEDsxkBmw-B6Ju6PNdBYVzM2FqudNRwW2dX4LCDGicHKgWrM4belmrRdaVJv7t1G8QIxLW2e2-KHX99iyV8M_69ZfyJESfN8u9nNq0JJif5yItRLD2hvR2nWdJ9S3FZ4pip5bw8ve1afcyqJMyi-Fz6gd3eE-bKlxPX2yDbUJUl1F0ck_KmfafehWg8TjQSswGF2DUCBtMDoYFp6A85T2YWvvkefi-k64TUWzPiBbvMhGH-fq4LDj06LgqGOrLT5XFjOywS4vqb4e26aIqj5sYl26TfTlxNR5DTznVycvfjEfrs3ZGoYd12w6TAgKjvbHCek=w311-h465-no?authuser=1)

We can always assign this DataFrame to a variable to save it, and then perform as many operations as we want with it. If you are a data scientist in Python, *pandas* is most likely your best friend, and the possibilities and analysis you can now perform is much, much higher. You can extract and input all kinds of data in machine learning algorithms, you can format and reformat structures, save them in a variable and input them back into the application by using **toQlik()** once again, you can perform regressions, trend predictions, etc... all using other Python libraries.

Note that the data we got is not what we originally inputted with **toQlik()**, but instead is literally what is displayed in our pie chart. The headers of the DataFrame are the labels we set in Qlik, and the measures are the expression we set for them, that is in this case, *Sum(passengers)*.

And also note, any changes you make to the object are saved automatically since we are in the Cloud. The object ID of an object does not change if you change the parameters of the object, and as such, every time you cast **toPy()**, the most current data is extracted. This means you can always edit your object whenever you need, rerun **toPy('objId')** and you will have an up-to-date DataFrame object at your disposal.


# Closing thoughts
PyToQlik is still under active development, and many more functions are expected to be released. But most importantly, we plan to add robustness to the code, as in, make it more streamlined, less prone to bugs and connectivity issues, especially for the Qlik Cloud SaaS version.

We also have the .ipynb file used to create this tutorial available [here](https://drive.google.com/file/d/1vk5AZ3pg4oHG4bgfYkF4AhdKq5XDiAws/view?usp=sharing).

If this tutorial was helpful for you in any way, please consider sharing it and also the library. The larger the community gets, the better and more focused we can collectively develop.





