---
editor_options: 
  markdown: 
    wrap: sentence
---

Project: Udacity Data Lake - STEDI Human Balance Analytics

Project Introduction: STEDI Human Balance Analytics

In this project, you'll act as a data engineer for the STEDI team to build a data lakehouse solution for sensor data that trains a machine learning model.
Project Details

The STEDI Team has been hard at work developing a hardware STEDI Step Trainer that:

```         
trains the user to do a STEDI balance exercise;
and has sensors on the device that collect data to train a machine-learning algorithm to detect steps;
has a companion mobile app that collects customer data and interacts with the device sensors.
```

STEDI has heard from millions of early adopters who are willing to purchase the STEDI Step Trainers and use them.

Several customers have already received their Step Trainers, installed the mobile application, and begun using them together to test their balance.
The Step Trainer is just a motion sensor that records the distance of the object detected.
The app uses a mobile phone accelerometer to detect motion in the X, Y, and Z directions.

The STEDI team wants to use the motion sensor data to train a machine learning model to detect steps accurately in real-time.
Privacy will be a primary consideration in deciding what data can be used.

Some of the early adopters have agreed to share their data for research purposes.
Only these customers’ Step Trainer and accelerometer data should be used in the training data for the machine learning model.

Constraints: Only consenting users can have data published.
Ideally, the app would not collect this information if this were the case instead of filtering it afterward.

Data: STEDI has three JSON data sources(opens in a new tab) to use from the Step Trainer.
Check out the JSON data in the following folders in the Github repo:

```         
customer
step_trainer
accelerometer



Extract the zip file.

Navigate to the project/starter folder in the extracted output to find the JSON data files within three sub-folders. You should have
    956 rows in the customer_landing table,
    81273 rows in the accelerometer_landing table, and
    28680 rows in the step_trainer_landing table.
```

1.  Customer Records

This is the data from fulfillment and the STEDI website.

Data Download URL(opens in a new tab)

AWS S3 Bucket URI - s3://cd0030bucket/customers/

contains the following fields:

```         
serialnumber
sharewithpublicasofdate
birthday
registrationdate
sharewithresearchasofdate
customername
email
lastupdatedate
phone
sharewithfriendsasofdate
```

2.  Step Trainer Records

This is the data from the motion sensor.

Data Download URL(opens in a new tab)

AWS S3 Bucket URI - s3://cd0030bucket/step_trainer/

contains the following fields:

```         
sensorReadingTime
serialNumber
distanceFromObject
```

3.  Accelerometer Records

This is the data from the mobile app.

Data Download URL(opens in a new tab)

AWS S3 Bucket URI - s3://cd0030bucket/accelerometer/

contains the following fields:

```         
timeStamp
user
x
y
z
```

Lastly, you must review the project README(opens in a new tab) in the Github repo to understand the project structure.

Using AWS Glue, AWS S3, Python, and Spark, create or generate Python scripts to build a lakehouse solution in AWS that satisfies these requirements from the STEDI data scientists.

Refer to the flowchart below to better understand the workflow.
A flowchart displaying the workflow.

A flowchart displaying the workflow.
Requirements

To simulate the data coming from the various sources, you will need to create your own S3 directories for customer_landing, step_trainer_landing, and accelerometer_landing zones, and copy the data there as a starting point.

```         
You have decided you want to get a feel for the data you are dealing with in a semi-structured format, so you decide to create three Glue tables for the three landing zones. Share your customer_landing.sql, accelerometer_landing.sql, and step_trainer_landing.sql scripts in git.
Query those tables using Athena, and take a screenshot of each one showing the resulting data. Name the screenshots customer_landing(.png,.jpeg, etc.), accelerometer_landing(.png,.jpeg, etc.), step_trainer_landing (.png, .jpeg, etc.).
```

The Data Science team has done some preliminary data analysis and determined that the Accelerometer Records each match one of the Customer Records.
They would like you to create 2 AWS Glue Jobs that do the following:

```         
Sanitize the Customer data from the Website (Landing Zone) and only store the Customer Records who agreed to share their data for research purposes (Trusted Zone) - creating a Glue Table called customer_trusted.
Sanitize the Accelerometer data from the Mobile App (Landing Zone) - and only store Accelerometer Readings from customers who agreed to share their data for research purposes (Trusted Zone) - creating a Glue Table called accelerometer_trusted.
You need to verify your Glue job is successful and only contains Customer Records from people who agreed to share their data. Query your Glue customer_trusted table with Athena and take a screenshot of the data. Name the screenshot customer_trusted(.png,.jpeg, etc.).
```

Data Scientists have discovered a data quality issue with the Customer Data.
The serial number should be a unique identifier for the STEDI Step Trainer they purchased.
However, there was a defect in the fulfillment website, and it used the same 30 serial numbers over and over again for millions of customers!
Most customers have not received their Step Trainers yet, but those who have, are submitting Step Trainer data over the IoT network (Landing Zone).
The data from the Step Trainer Records has the correct serial numbers.

The problem is that because of this serial number bug in the fulfillment data (Landing Zone), we don’t know which customer the Step Trainer Records data belongs to.

The Data Science team would like you to write a Glue job that does the following:

```         
Sanitize the Customer data (Trusted Zone) and create a Glue Table (Curated Zone) that only includes customers who have accelerometer data and have agreed to share their data for research called customers_curated.
```

Finally, you need to create two Glue Studio jobs that do the following tasks:

```         
Read the Step Trainer IoT data stream (S3) and populate a Trusted Zone Glue Table called step_trainer_trusted that contains the Step Trainer Records data for customers who have accelerometer data and have agreed to share their data for research (customers_curated).
Create an aggregated table that has each of the Step Trainer Readings, and the associated accelerometer reading data for the same timestamp, but only for customers who have agreed to share their data, and make a glue table called machine_learning_curated.
```

Refer to the relationship diagram below to understand the desired state.
A diagram displaying the relationship between entities.

A diagram displaying the relationship between entities.
Check your work!

After each stage of your project, check if the row count in the produced table is correct.
You should have the following number of rows in each table:

```         
Landing
    Customer: 956
    Accelerometer: 81273
    Step Trainer: 28680
Trusted
    Customer: 482
    Accelerometer: 40981
    Step Trainer: 14460
Curated
    Customer: 482
    Machine Learning: 43681
```

Hint: Use Transform - SQL Query nodes whenever you can.
Other node types may give you unexpected results.

For example, rather than a Join node, you may use a SQL node that has two parents, then join them through a SQL query.

## Project Rubric

**Landing Zone**

+----------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Criteria                                                       | Submission Requirements                                                                                                                                                                                                    |
+================================================================+============================================================================================================================================================================================================================+
| Use Glue Studio to ingest data from an S3 bucket               | **customer_landing_to_trusted.py**, **accelerometer_landing_to_trusted.py**, and **step_trainer_trusted.py** Glue jobs have a node that connects to S3 bucket for customer, accelerometer, and step trainer landing zones. |
+----------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Manually create a Glue Table using Glue Console from JSON data | SQL DDL scripts customer_landing.sql, accelerometer_landing.sql, and step_trainer_landing.sql include all of the JSON fields in the data input files and are appropriately typed (not everything is a string).             |
+----------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Use Athena to query the Landing Zone.                          | Include screenshots showing various queries run on Athena, along with their results:                                                                                                                                       |
|                                                                |                                                                                                                                                                                                                            |
|                                                                | -   Count of customer_landing: 956 rows                                                                                                                                                                                    |
|                                                                | -   The customer_landing data contains multiple rows with a blank shareWithResearchAsOfDate.                                                                                                                               |
|                                                                | -   Count of accelerometer_landing: 81273 rows                                                                                                                                                                             |
|                                                                | -   Count of step_trainer_landing: 28680 rows                                                                                                                                                                        |
+----------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

**Trusted Zone**

+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| Criteria                                                                       | Submission Requirement                                                                                                                     |
+================================================================================+============================================================================================================================================+
| Configure Glue Studio to dynamically update a Glue Table schema from JSON data | Glue Job Python code shows that the option to dynamically infer and update schema is enabled.                                              |
|                                                                                |                                                                                                                                            |
|                                                                                | To do this, set the *Create a table in the Data Catalog and, on subsequent runs, update the schema and add new partitions* option to True. |
+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| Use Athena to query Trusted Glue Tables                                        | Include screenshots showing various queries run on Athena, along with their results:                                                       |
|                                                                                |                                                                                                                                            |
|                                                                                | -   Count of customer_trusted: 482 rows                                                                                                    |
|                                                                                |                                                                                                                                            |
|                                                                                |     -   The resulting customer_trusted data has no rows where shareWithResearchAsOfDate is blank.                                          |
|                                                                                |                                                                                                                                            |
|                                                                                | -   Count of accelerometer_trusted: 40981 rows                                                                                             |
|                                                                                |                                                                                                                                            |
|                                                                                | -   Count of step_trainer_trusted: 14460 rows                                                                                              |
|                                                                                |                                                                                                                                            |
|                                                                                | However, **if you are following the stand-out suggestions**, your row counts should be as follows:                                         |
|                                                                                |                                                                                                                                            |
|                                                                                | -   Count of customer_trusted: 482 rows                                                                                                    |
|                                                                                |                                                                                                                                            |
|                                                                                |     -   The resulting customer_trusted data has no rows where shareWithResearchAsOfDate is blank.                                          |
|                                                                                |                                                                                                                                            |
|                                                                                | -   Count of accelerometer_trusted: 32025 rows                                                                                             |
|                                                                                |                                                                                                                                            |
|                                                                                | -   Count of step_trainer_trusted: 14460 rows                                                                                              |
+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| Filter protected PII with Spark in Glue Jobs                                   | **customer_landing_to_trusted.py** has a node that drops rows that do not have data in the sharedWithResearchAsOfDate column.              |
|                                                                                |                                                                                                                                            |
|                                                                                | Hints:                                                                                                                                     |
|                                                                                |                                                                                                                                            |
|                                                                                | -   **Transform - SQL Query** node often gives more consistent outputs than other node types.                                              |
|                                                                                |                                                                                                                                            |
|                                                                                | -   Glue Jobs do not replace any file. Delete your S3 files and Athena table whenever you update your visual ETLs.                         |
+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------+
| Join Privacy tables with Glue Jobs                                             | **accelerometer_landing_to_trusted.py** has a node that                                                                                    |
|                                                                                | inner joins the customer_trusted data with the accelerometer_landing                                                                       |
|                                                                                | data by emails. The produced table should have only columns from the                                                                       |
|                                                                                | accelerometer table.                                                                                                                       |
+--------------------------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------+

+-----------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Criteria                                | Submission Requirements                                                                                                                                                                                          |
+=========================================+==================================================================================================================================================================================================================+
| Write a Glue Job to join trusted data   | **customer_trusted_to_curated.py** has a node that inner joins the `customer_trusted` data with the `accelerometer_trusted` data by emails. The produced table should have only columns from the customer table. |
+-----------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Write a Glue Job to create curated data | **step_trainer_trusted.py** has a node that inner joins the step_trainer_landing data with the customer_curated data by serial numbers                                                                           |
|                                         |                                                                                                                                                                                                                  |
|                                         | **machine_learning_curated.py**                                                                                                                                                                                  |
|                                         | has a node that inner joins the step_trainer_trusted data with the                                                                                                                                               |
|                                         | accelerometer_trusted data by sensor reading time and timestamps                                                                                                                                                 |
|                                         |                                                                                                                                                                                                                  |
|                                         | Hints:                                                                                                                                                                                                           |
|                                         |                                                                                                                                                                                                                  |
|                                         | -   **Data Source - S3 bucket** node sometimes extracted incomplete data. Use the **Data Source - Data Catalog** node when that's the case.                                                                      |
|                                         |                                                                                                                                                                                                                  |
|                                         | -   Use                                                                                                                                                                                                          |
|                                         |     the Data Preview feature with at least 500 rows to ensure the number of                                                                                                                                      |
|                                         |     customer-curated rows is correct. Click "Start data preview session",                                                                                                                                        |
|                                         |     then click the gear next to the "Filter" text box to update the number                                                                                                                                       |
|                                         |     of rows                                                                                                                                                                                                      |
|                                         |                                                                                                                                                                                                                  |
|                                         | -   As before, the **Transform - SQL Query** node often gives more consistent outputs than any other node type. Tip - replace the JOIN node with it.                                                             |
|                                         |                                                                                                                                                                                                                  |
|                                         | -   The `step_trainer_trusted` may take about 8 minutes to run.                                                                                                                                                  |
+-----------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Use Athena to query Curated Glue Tables | Include screenshots showing various queries run on Athena, along with their results:                                                                                                                             |
|                                         |                                                                                                                                                                                                                  |
|                                         | -   Count of customer_curated: 482 rows                                                                                                                                                                          |
|                                         |                                                                                                                                                                                                                  |
|                                         | -   Count of machine_learning_curated: 43681 rows                                                                                                                                                                |
|                                         |                                                                                                                                                                                                                  |
|                                         | However, **if you are following the stand-out suggestions**, your row counts should be as follows:                                                                                                               |
|                                         |                                                                                                                                                                                                                  |
|                                         | -   Count of customer_curated: 464 rows                                                                                                                                                                          |
|                                         |                                                                                                                                                                                                                  |
|                                         | -   Count of machine_learning_curated: 34437 rows                                                                                                                                                                |
|                                         |                                                                                                                                                                                                                  |
|                                         | Hint: If you get unexpected results, consider using the **Transform - SQL Query** node rather than Glue-provided nodes.                                                                                          |
+-----------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

### Suggestions to Make Your Project Stand Out

Consider these additions to your project to make it stand out!

1.  When creating
    the Glue Job to join data from the accelerometer readings and the
    customer table, filter out any readings that were prior to the research
    consent date.
    This will ensure consent was in place at the time that
    data was gathered.
    This helps in the case that in the future the
    customer revokes consent.
    We can be sure that the data we used for
    research was used when consent was in place for that particular data.

2.  Anonymize
    the final curated table so that it is not subject to GDPR or other
    privacy regulations, in case a customer requests deletion of PII, we
    will not be in violation by retaining PII data --remove email, and any
    other personally identifying information up front.
