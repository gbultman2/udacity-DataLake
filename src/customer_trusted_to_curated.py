import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import functions as SqlFuncs

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1738000688501 = glueContext.create_dynamic_frame.from_catalog(database="stedi-analytics", table_name="customer_trusted", transformation_ctx="AWSGlueDataCatalog_node1738000688501")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1738000687540 = glueContext.create_dynamic_frame.from_catalog(database="stedi-analytics", table_name="accelerometer_trusted", transformation_ctx="AWSGlueDataCatalog_node1738000687540")

# Script generated for node Join
Join_node1738000716680 = Join.apply(frame1=AWSGlueDataCatalog_node1738000688501, frame2=AWSGlueDataCatalog_node1738000687540, keys1=["email"], keys2=["user"], transformation_ctx="Join_node1738000716680")

# Script generated for node Drop Fields
DropFields_node1738000755326 = DropFields.apply(frame=Join_node1738000716680, paths=["x", "y", "timestamp", "z", "user"], transformation_ctx="DropFields_node1738000755326")

# Script generated for node Drop Duplicates
DropDuplicates_node1738000794090 =  DynamicFrame.fromDF(DropFields_node1738000755326.toDF().dropDuplicates(), glueContext, "DropDuplicates_node1738000794090")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=DropDuplicates_node1738000794090, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1738000133843", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1738000806940 = glueContext.getSink(path="s3://stedi-data-lake-gb/customer/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1738000806940")
AmazonS3_node1738000806940.setCatalogInfo(catalogDatabase="stedi-analytics",catalogTableName="customer_curated")
AmazonS3_node1738000806940.setFormat("json")
AmazonS3_node1738000806940.writeFrame(DropDuplicates_node1738000794090)
job.commit()