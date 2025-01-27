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
AWSGlueDataCatalog_node1738008052685 = glueContext.create_dynamic_frame.from_catalog(database="stedi-analytics", table_name="step_trainer_trusted", transformation_ctx="AWSGlueDataCatalog_node1738008052685")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1738008065214 = glueContext.create_dynamic_frame.from_catalog(database="stedi-analytics", table_name="accelerometer_trusted", transformation_ctx="AWSGlueDataCatalog_node1738008065214")

# Script generated for node SQL Query
SqlQuery4459 = '''
SELECT *
FROM at2
JOIN stt 
ON at2.timestamp = stt.sensorreadingtime;

'''
SQLQuery_node1738008080208 = sparkSqlQuery(glueContext, query = SqlQuery4459, mapping = {"at2":AWSGlueDataCatalog_node1738008065214, "stt":AWSGlueDataCatalog_node1738008052685}, transformation_ctx = "SQLQuery_node1738008080208")

# Script generated for node Select Fields
SelectFields_node1738008211024 = SelectFields.apply(frame=SQLQuery_node1738008080208, paths=["y", "x", "z", "timestamp", "user", "sensorreadingtime", "serialnumber", "distancefromobject"], transformation_ctx="SelectFields_node1738008211024")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SelectFields_node1738008211024, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1738007370961", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1738008225705 = glueContext.getSink(path="s3://stedi-data-lake-gb/machine_learning_curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1738008225705")
AmazonS3_node1738008225705.setCatalogInfo(catalogDatabase="stedi-analytics",catalogTableName="machine_learning_curated")
AmazonS3_node1738008225705.setFormat("json")
AmazonS3_node1738008225705.writeFrame(SelectFields_node1738008211024)
job.commit()