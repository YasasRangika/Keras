# Welcome to Automating-APIM-Migration-Testing Tool
![enter image description here](https://lh3.googleusercontent.com/jzdVP5eLXSpqJtMzeQxglw-34LLe6p3tUwrDBWd33sRqJu5TGJRtzz8t6bfOkthJQjYcGW2ZLi0p=s300)


## **Prerequisites**
-   Clone or download [this](https://github.com/YasasRangika/apim-automating-migration-testing) GitHub repository.
    


> If you have not installed Python 3 or above version please follow this [https://www.python.org/downloads/](https://www.python.org/downloads/) to install.

    

  

-   Choose your database type that you are going to test the API manager product with it.
    
-   It is requested to create three databases in that database type that you have selected;
    

		amdb: Databases for API Manager tables
    
		regdb: Database for registry management tables
    
		userdb: Database for user management tables
    

	-   In Oracle database no need to have these kinds of three databases
    

  

-   All the database names that you have provided when creating databases must be added to the properties file that is mentioned in the following 'working with properties file' section.
    

  

	-   Please use one all privileged user for creating above databases. Use of multiple users are not currently supported for this tool
    

  

-   Download the two API Manager versions that you want to test the migration.

## **Testing Tool**

![enter image description here](https://lh3.googleusercontent.com/NI4AYDlIpXpNAZ0g5IPl2ltiCe4ImZZmI9udKlLJkW09ZqObqLQ5lB3ykXMSdS8vOnbIgJ-w2itJ)

This migration Test Automation tool is a python program (Python 3) that includes several components. To run this complete program there is shell script for Linux-based platforms and bat file for Windows-based platforms.

There is a property file named as properties.py inside the Python directory in the root directory of testing tool. All the system required information is extracted from this file. As this is the most important part of this tool, the whole next section will discuss how to feed data into it.

## **Working with Properties File**

    <Testing_tool_HOME_PATH>/Python/properties.py
![enter image description here](https://lh3.googleusercontent.com/sN-w_lVjW8JekgoYFGlV9y53qxWmMhAbTpSAfUJUq1THmnSE6QNEM0F9M3bigRQDlQbsIDebtVVu)

This is a python file. So before feeding data to this file, you need to know how to follow basic Python syntaxes and rules given below.

 -   Do not hit any spaces or tabs before any line in the file
    
 -   Do not change any given key name
    
 -   There is a file filled with dummy data, and do not forget to parse string values inside the double inverted commas
    
 -   Commenting is done by ‘#’ sign in python.

**Give New Values and Commenting/Uncommenting default values in Properties File**

	   -   OLD_VERSION/TO_OLD_PATH: Chosen old/new version
	  
	   -   TO_OLD_PATH/TO_NEW_PATH: Path to the download location of the zip file
       
	   -   APIM_HOME_PATH: Choose a location to unzip files (This will be the home path for every version)
       
	   -   DB_TYPE: Uncomment given database type according to your test (Only one database type is allowed at once)
       
	   -   USER_NAME, PWD, HOST, PORT: According to the given type of database, give these values accurately (PORT is integer value)
       
	   -   AM_DB, REG_DB, USER_DB: As mentioned in prerequisites provide database names you have given to those databases (Follow the lowercase uppercase letters correctly in database names)
       
	   -   SID: This is only for Oracle database
       
	   -   IS_VERSION: Identity server version which is required for given new version of API Manager product
       
	   -   JAVA_HOME: Java home path if it is not set as a path variable

## **Manually Adding Required Resources for The Testing Tool**

	    Do not remove any file that comes with the testing tool except adding new required files.

 - There are three directories named API-M_2.1.0, API-M_2.2.0, API-M_2.5.0 in <Testing_tool_HOME_PATH>/data directory. These directories include edited registry.xml file that is required to replace with the original file that came up among API Manager package for mounting registries.  
If the new version you are going to test is not in this list you need to manually add it to this kind of directory. For that follow [https://docs.wso2.com/display/AM210/Installing+and+Configuring+the+Databases](https://docs.wso2.com/display/AM210/Installing+and+Configuring+the+Databases)(see the AM version you want) steps in the section “To enable access to the registry database” to build registry.xml. When naming the directory please follow this pattern;
   
   > API-M_<APIM_VERSION>
  
 -   In most cases, user-mgt.xml is same as in all the versions. So the configured user-mgt.xml file is located under <Testing_tool_HOME_PATH>/data  directory for all cases. If any special situation comes in future to change user-mgt.xml with the version, then edit it with the registry.xml and change the code segment; 

    #user-mgt.xml file changing
    change_file("user-mgt.xml", '../data/user-mgt.xml', ←change the path to file'%s/wso2am-%s/repository/conf/user-mgt.xml' % (APIM_HOME_PATH, OLD_VERSION))

In `<Testing_tool_HOME_PATH>/Python/testingtool.py`  file

-   As mentioned in WSO2 API Manager migration documentation, download the reg-index.sql and tenantloader.jar files and place it in the `<Testing_tool_HOME_PATH>/data/re_indexing_registry` directory with renaming these two files as below;

> *sql file:* ‘**reg-index.sql**’ and jar file: ‘**tenantloader.jar**’

![enter image description here](https://lh3.googleusercontent.com/LpaiTWE6k7MCv2CRjrnocwm5VBYQfBLPmNDJMEYTpYeNy5HGQmZPzncrYX1Oc04Bno3p7FqpRmU_)

 - In `<Testing_tool_HOME_PATH>/data/Access_control_migration_client`  directory you should keep the required migration client mentioned in the WSO2 APIM migration documentation.

![enter image description here](https://lh3.googleusercontent.com/g9QI09mFdSrZuRkK1zsKNrE19bnyolSnFRtF0mhujjTxwlmWbe6FktvWXy8vUvE0vlwnXDLgBDW_)

Go through the given link in the documentation and download .jar file or .zip file and add it to `<Testing_tool_HOME_PATH>/data/Access_control_migration_client` directory.  
It is essential to do required changes in code level also as follows;

Go to the `<Testing_tool_HOME_PATH>/Python/ApiMangerConfigUtil/configuring_identity_components.py`  and find below code segment,

    def access_control_migration_client():
	    """Copy access control migration client and configure server"""
	    dir = '%s/wso2am-%s/migration-resources' % (APIM_HOME_PATH, NEW_VERSION)
	    if os.path.isdir(dir):
		    shutil.rmtree(dir)
	    
	    jar_dir = '%s/wso2am-%s/repository/components/dropins/org.wso2.carbon.is.migration-%s.jar' % (APIM_HOME_PATH, NEW_VERSION, IS_MIGRATE_VERSION)
	    os.remove(jar_dir)
	    if shutil.copy('../data/Access_control_migration_client/org.wso2.carbon.apimgt.access.control.migration.client-1.0-SNAPSHOT.jar'<←org.wso2.carbon.is.migration-5.6.0.jar to the name of new downloaded file name>, '%s/wso2am-%s/repository/components/dropins' % (APIM_HOME_PATH, NEW_VERSION)):
		    print("Successfully copied the apimgt.access.control.migration.client JAR.")
		    
	    subprocess.Popen(["gnome-terminal", "-e",
	    "%s/wso2am-%s/bin/wso2server.sh -DmigrateAccessControl=true" % (APIM_HOME_PATH, NEW_VERSION)])

 -    Identity component upgrading;
 
 Download and copy the required IS-migration resource as mentioned in documentation to `<Testing_tool_HOME_PATH>/data/Identity_component_upgrade` directory. For that follow the instructions given in migration documentation.


![enter image description here](https://lh3.googleusercontent.com/KOew2RC1jPkYLrjxJaCTte6S13LCdKqBnP9Lki91CwpOcSi5C6WTmEu3If1X7vmKfYQfzaehlAeU)
	
- Unzip the zip file and make sure the name of that directory is in format,
***

> ‘wso2is-x.x.0-migration’

***
   
   

 Change the IS_MIGRATE_VERSION value in properties.py file.

    #Relevant WSO2 IS version(ex:5.6.0)
    IS_CURRENT_VERSION = "5.3.0"
    IS_MIGRATE_VERSION = "5.7.0"
    
 - Check whether ‘**migration-resources**’ folder exist inside the unzipped directory.

    
-   If you can’t see ‘**org.wso2.carbon.is.migration-x.x.0.jar**’ in <wso2is-x.x.0-migration-HOME> directory, please check if it is available inside the folder named 'droppings' or another folder available in this location. If the jar files are available inside the droppings folder or within a similar folder then bring the jar files into the `<wso2is-x.x.0-migration-HOME>` path
    
-   After all these steps you should see the below files exists inside `<wso2is-x.x.0-migration-HOME>`;

> migration-resources 
> 
> org.wso2.carbon.is.migration-x.x.0.jar
> 
> snakeyaml-1.16.0.wso2v1.jar

 - Download apimgt-db-migration-scripts by the link provided in
   migration documentation


![enter image description here](https://lh3.googleusercontent.com/wJi4o4ZpP_HC8b45qTdGwdm7I4GlyJ6Vi7u_CXXQePRn0pELRyomM1iEfj5YHIHk__1M50ar8fHO)

Unzip content from the zip file to `<Testing_tool_HOME_PATH>/data/Identity_component_upgrade/migration_scripts` directory renaming it in the below format.
***

> ‘apimgt-db-migration-scripts-x.x.0toy.y.0’

***

![enter image description here](https://lh3.googleusercontent.com/JS-0m6lPyCf31wFBBUzhtin0LAkeYZEbsMpncS6ErJ_lTTdbsgcsSeLK9BOll5xhKoM9Qjeteqg1)


It is requested to download and copy gateway_artifact_migrator.sh script to the same above-mentioned directory by renaming as follows;

> ***‘apim_gateway_artifact_migrator.sh’*** 
> 
> *(remove all the version numbers)*

## **JMeter Test Scripts**
There are two ways to accomplish this step either using JMeter UI or editing JMeter script;

**Type 01 - Edit JMeter Script**

Go to the directory `<Testing_tool_HOME_PATH>/testing/scripts` and open below mentioned three scripts using text editor;

> DataPopulationInOldVersion.jmx
> 
> Integration_testing_in_new_APIM.jmx
> 
> Validation_in_new_APIM.jmx
> 

Then find this segment;

    <elementProp name="rest_api_version" elementType="Argument">
	    <stringProp name="Argument.name">rest_api_version</stringProp>
	    <stringProp name="Argument.value">v0.12</stringProp>
	    <stringProp name="Argument.metadata">=</stringProp>
       </elementProp>

Change the `<stringProp name="Argument.value">v0.12</stringProp>` version number according to the APIM version you are going to test. For assistance;

 - APIM 2.0.0 -> v0.10 
 - APIM 2.1.0 -> v0.11 
 - APIM 2.2.0 -> v0.12 
 - APIM 2.5.0 -> v0.13 
 - APIM 2.6.0 -> v0.14

Do this for all above mentioned three files.

**Type 02 - With JMeter UI**

This APIM Testing tool consists of JMeter testing tool. Find it from `<Testing_tool_HOME_PATH>/testing/bin` directory. To do any changes in JMeter script start JMeter by manually going to this location. Please go through [these steps](https://www.blazemeter.com/blog/how-get-started-jmeter-part-1-installation-test-plans/) to launch JMeter.

 -Existing test scripts are as follows;
 
 - **RolesAndUsersCreation.jmx:**
			 This script is to take care of admin SOAP APIs to create roles and users. Without any special reason, users will not want to open or change this script version to version.
			 
 - **DataPopulationInOldVersion.jmx:**

![](https://lh5.googleusercontent.com/aDs3iLrny78Iqv1sfWsR0wG6S5P0DrN7usuTk9Y2JK3hZZbHQnj4ml55_xBMrIxZVVKg3eD8wTMpsv7WXHAkEsC9sKSrX4If6xjUVcXwPFqRB7pYCMIfkK9Z-9k_pizmhwZk0p6h)
		
This test script is designed assuming the old version is API Manager 2.2.0. (You can find this variable list by clicking on the ‘Data Population in Old Version’ thread class name in sidepane).

You need to change the last variable ‘rest_api_version’ to the relevant rest api version number mentioned in [https://docs.wso2.com/display/AM260/RESTful+APIs](https://docs.wso2.com/display/AM260/RESTful+APIs).

 -    **Validation_in_new_APIM.jmx:**
		 This script is for validating APIs created in the previous version of API Manager.


![](https://lh5.googleusercontent.com/01N59ZEXqAMRmoEaw1OeTGXIbKJ_pWzdU7yDpPBGF9gfowsgraSYulqPntRXOTrgXUKwV7mBfgEfxuduJgbIIapFIMfKQiEQ4C6rCallWqj3RxclxQy557x7auAxudNQj_j_CVaw)


So as mentioned in the above step, need to change the version number

- **Integration_testing_in_new_APIM.jmx:**
	This script will generate and test new APIs in the new version of API Manager. Do the version number change as previous.

## **Running Testing Tool**

By following the above steps correctly, now you are ready to run the testing tool.
Using shell script for Linux based OS or bat file for Windows OS you can run the testing tool.

![](https://lh6.googleusercontent.com/SaXwfK8k5e1Upajq7B6tiIrir1yethP0Rx_OvYH8GiLCqVxFCmFmtC3VDBFLEGWFLmoJckh-LIlR8mee9tsShZvhOhQqU09scUKqOZXjtAicavUn-B5QTjpZa5eRBLipIwuH40iR)
