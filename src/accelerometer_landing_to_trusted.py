import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
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
AWSGlueDataCatalog_node1737998467831 = glueContext.create_dynamic_frame.from_catalog(database="stedi-analytics", table_name="accelerometer_landing", transformation_ctx="AWSGlueDataCatalog_node1737998467831")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1737998502994 = glueContext.create_dynamic_frame.from_catalog(database="stedi-analytics", table_name="customer_trusted", transformation_ctx="AWSGlueDataCatalog_node1737998502994")

# Script generated for node Join
Join_node1737998486081 = Join.apply(frame1=AWSGlueDataCatalog_node1737998467831, frame2=AWSGlueDataCatalog_node1737998502994, keys1=["user"], keys2=["email"], transformation_ctx="Join_node1737998486081")

# Script generated for node SQL Query
SqlQuery4801 = '''
SELECT * 
FROM myDataSource AS d
WHERE d.timestamp >= d.shareWithResearchAsOfDate;
'''
SQLQuery_node1737999886529 = sparkSqlQuery(glueContext, query = SqlQuery4801, mapping = {"myDataSource":Join_node1737998486081}, transformation_ctx = "SQLQuery_node1737999886529")

# Script generated for node Select Fields
SelectFields_node1737998621138 = SelectFields.apply(frame=SQLQuery_node1737999886529, paths=["y", "x", "z", "timestamp", "user"], transformation_ctx="SelectFields_node1737998621138")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SelectFields_node1737998621138, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1737997752340", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1737998720974 = glueContext.getSink(path="s3://stedi-data-lake-gb/accelerometer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1737998720974")
AmazonS3_node1737998720974.setCatalogInfo(catalogDatabase="stedi-analytics",catalogTableName="accelerometer_trusted")
AmazonS3_node1737998720974.setFormat("json")
AmazonS3_node1737998720974.writeFrame(SelectFields_node1737998621138)
job.commit()