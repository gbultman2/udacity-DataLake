The purpose of this readme is to provide a look at how I approached this project and to have it graded by Udacity.

Step 1.  Suss out the requirements and develop a plan. 

I like to follow the mantra "code last."  Code and any tools used should just be an artifact of the design process. Since the requirements are pretty stringent in this project, I'll follow them as listed even though improvements can be made.  I will list any recommendations in a later section.  

**Requirements Analysis**

We're given the data for the accelerometer and the mobile application in the project.  

Looks like we need to just copy local files for the data into the s3 bucket into a landing zone then create other folders in S3 with glue jobs.  I've outlined the required S3 bucket path structure and glue table names, in parentheses, below:

Customer
	| Landing (customer_landing)
	| Trusted (customer_trusted)
	| Curated (customers_curated)
Accelerometer
	| Landing (accelerometer_landing)
	| Trusted (accelerometer_trusted)
Step Trainer
	| Landing (step_trainer_landing)
	| Trusted (step_trainer_trusted)
	| Curated (machine_learning_curated)
	
In the landing zones, we'll just need to copy project data over to the S3 buckets.   The trusted are as follows:

- Customer - only the customer records of those who agreed to share data
- Accelerometer - Only readings from customers who agreed to share their data
- Step Trainer - only data from customers who agreed to share their data

The specifications for this project require that there be a certain number of records in each zone.  Therefore, we won't do any type of quality checks on the incoming data.  In a real world application, we would profile the information based on the metadata provided.

Data scientists discovered a data quality issue with customer data.  The serial number in the customer table is reused.  There was a defect in the fulfillment website.  The data in step trainer records is correct though. I'm not really sure why the data scientists are accessing the raw data if we're to create curated data for them. Nonetheless we need to fix the issue in the data lake.  The website needs fixed as well, but that is a task for others.  Data profiling would have identified this issue before getting downstream.  

The specifications for the project also require us to use glue jobs to move the data from the landing to the trusted zones.  So we need to use AWS Glue to accomplish that task.

Examining the data:

We need to know how to join the tables to create the trusted zones.  Here are the Relationships: 

Customers.serialnumber = step_trainer.serialNumber
Customers.email = accelerometer.user
step_trainer.sensorReadingTime = accelerometer.timeStamp

customers.sharewithresearchasofdate is the property we need to use to create the trusted records.  The requirements don't explicitly state whether we need to use records only after this date.  We'll be conservative and only use data on or after this date.  Note: This is a recommendation to make your project stand out.  It seems like a best practice.

Plan

1.  Create an AWS S3 bucket for the data lake and create a role so that Glue can access the bucket. 
2.  Move the landing zone data from the project folders to the S3 bucket.
3.  Create a glue table for each of the landing zone objects and save the sql create statements.
	a. customer_landing (customer_landing.sql)
	b. accelerometer_landing (accelerometer_landing.sql)
	c. step_trainer_landing (step_trainer_landing.sql)
4.  Query the tables using Athena
	a. customer_landing
		i. table row count (956)
		ii. show rows with blank shareWithResearchAsOfDate
	b. accelerometer_landing
		- table row count (81273)
	c. step_trainer_landing
		- table row count (28680)
5.  Sanitize the data with glue jobs and create trusted zone glue tables.  This must be done using Glue Studio and it must dynamically update a glue table schema from the JSON data. (To do this, set the Create a table in the Data Catalog and, on subsequent runs, update the schema and add new partitions option to True.)
		a. customer_landing_to_trusted.py
			- must have a node that drops rows that don't have data in the sharedWithResearchAsOfDate column
		b. accelerometer_landing_to_trusted.py
			- must have a node that inner joins customer_trusted with acclerometer_landing by email. Produced table must only have accelerometer data
		c. step_trainer_trusted.py (inconsistent naming is in the requirements)
			- must have a node that inner joins the step_trainer_landing data with customer_curated data by serial numbers
			(this step may take about 8 minutes to run)  -- note you'll have to run this step later but it's here to show consistency
6.  Query the trusted tables using Athena and provide screenshots.
	a. customer_trusted
		i. table row count (482)
		ii. row count where shareWithResearchAsOfDate is blank (0)
	b. accelerometer_trusted
		- table row count (32205)
	c. step_trainer_trusted
		- table row count (14460)
7.  Curate the data with glue jobs and create curated zone glue tables. 
	a. customer_trusted_to_curated.py
		i. must have a node that inner joins customer_trusted with accelerometer_trusted by email
		ii. table must only have columns from the customer table
	b. machine_learning_curated.py (inconsistent naming is in the requirements)
		- must have a node that inner joins step_trainer_trusted data with the customer_curated data by timestamp
8. Query the curated tables using Athena and provide screenshots
	a. customer_curated 
		- table row count (464)
	b. machine_learning_curated
		- table row count (43681)
		
Execution: 

Based on the plan, we don't really need to do much AWS infrastructure setup.  So we won't use infrastructure as code for this project. 

1.  Create the S3 bucket and role for glue
	a. bucket name - stedi-data-lake-gb
	b. glue role - glue-s3-full-access
        i. give the glue assume role AmazonS3FullAccess and AWSGlueServiceRole
        ii. in a real environment we'd assume least privlige however udacity restricts how we see things in the aws console and we can't analyze these `You don't have permission to access-analyzer:ListPolicyGenerations`.
2. Upload data to the landing zone. The project has us using the cloudshell console to do this task, but I'm just going to do it through the S3 UI.
	- I have the project on my local machine so, I uploaded everything from there.  Everything will be in my git repo as well.
	- This produced a structure as follows: 
		customer
			| landing
		accelerometer
			| landing
		step_trainer
			| landing
3. Create a glue table for the landing zones in the glue UI. Note: we don't have metadata on any of this so we'll make a best guess at the datatypes by inspecting sample files.
	a. create the `stedi-analytics` database in Glue
	b. create the table for `customer_landing` with path s3://stedi-data-lake-gb/customer/landing/
		i. customerName string
		ii. email - string
		iii. phone - bigint (initial called for string?)
		iv. birthDay - date (initial called for string?)
		v. serialNumber string
		vi. registrationDate - bigint
		vii. lastUpdateDate - bigint
		viii. shhareWithResearchAsOfDate - bigint
		ix. shareWithPublicAsOfDate - bigint
		x. shareWithFriendsAsOfDate - bigint
	c. create the table for `accelerometer_landing` with path s3://stedi-data-lake-gb/accelerometer/landing/
		i. user - string
		ii. timestamp - bigint
		iii. x - float
		iv. y - float
		v. z - float
	d. create glue table for `step_trainer_landing` with path s3://stedi-data-lake-gb/step_trainer/landing/
		i. sensorreadingtime - bigint
		ii. serialnumber - string
		iii. distancefromobject - int
4. Query Data in Athena
	a. Set up a landing zone for queries in S3: s3://stedi-data-lake-gb/query-result/
	b. Run the table ddl for each table created and save the sql code to files for the git repo. 
	    i. SHOW CREATE TABLE `customer_landing`;
	    ii. SHOW CREATE TABLE `accelerometer_landing`;
	    iii. SHOW CREATE TABLE `step_trainer_landing`;
    c. Query the row counts from each table and provide screen shots
        i. img/
        ii. img/
        iii. img/
    d. Query the customer and show that there are blanks in the sharedwithpublic field
        - img/
5. Sanitize the tables and output them to the trusted zone using Glue Studio
    a.   customer_trusted 
        - customer_landing_to_trusted.py
    b. accelerometer_trusted
        - accelerometer_landing_to_trusted.py
    c. step_trainer_trusted
        - step_trainer_landing_to_trusted.py
6. Query the tables using Athena
    a. customer_trusted
        i. row count img/
        ii. no customers with missing research dates /img
    b. accelerometer_trusted
        - row count
    c. step_trainer_trusted
        - row count
7. Curated Zone 
    a. customer_curated
        - customer_trusted_to_curated.py
    b. machine_learning_curated
        
        
		
	
	
	
Expected row counts
    customer
        - landing 956
        - trusted 482
        - curated 464
    accelerometer
        - landing 81273
        - trusted 32025
        - curated 
    step_trainer
        -landing 28680
        -trusted 14460 - 13920?
    ml curated 34437
