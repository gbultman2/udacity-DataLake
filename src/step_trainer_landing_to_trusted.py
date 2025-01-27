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
AWSGlueDataCatalog_node1738001259806 = glueContext.create_dynamic_frame.from_catalog(database="stedi-analytics", table_name="step_trainer_landing", transformation_ctx="AWSGlueDataCatalog_node1738001259806")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1738001276407 = glueContext.create_dynamic_frame.from_catalog(database="stedi-analytics", table_name="customer_curated", transformation_ctx="AWSGlueDataCatalog_node1738001276407")

# Script generated for node SQL Query
SqlQuery854 = '''
SELECT sensorreadingtime
    , serialnumber
    , distancefromobject
FROM stl
WHERE serialnumber IN (SELECT serialnumber FROM cc);
'''
SQLQuery_node1738004664162 = sparkSqlQuery(glueContext, query = SqlQuery854, mapping = {"stl":AWSGlueDataCatalog_node1738001259806, "cc":AWSGlueDataCatalog_node1738001276407}, transformation_ctx = "SQLQuery_node1738004664162")

# Script generated for node Select Fields
SelectFields_node1738006271852 = SelectFields.apply(frame=SQLQuery_node1738004664162, paths=["sensorreadingtime", "serialnumber", "distancefromobject"], transformation_ctx="SelectFields_node1738006271852")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=SelectFields_node1738006271852, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1738007370961", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1738007403059 = glueContext.getSink(path="s3://stedi-data-lake-gb/step_trainer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1738007403059")
AmazonS3_node1738007403059.setCatalogInfo(catalogDatabase="stedi-analytics",catalogTableName="step_trainer_trusted")
AmazonS3_node1738007403059.setFormat("json")
AmazonS3_node1738007403059.writeFrame(SelectFields_node1738006271852)
job.commit()