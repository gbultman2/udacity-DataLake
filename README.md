# Deliverables: 

Notes: 

1. I believe the rubric is incorrect for count of step_trainer_trusted: 14460 rows when following the stand out suggestions.  There are fewer rows in customer_curated.  So, it stands to reason that if there are fewer customers, there will be fewer rows in the step trainer trusted when we have to join on customer_curated.  I have 13,920.
2. I used SQL statements rather than inner join nodes for `machine_learning_curated` and `step_trainer_landing_to_trusted` glue jobs.  

## Python Scripts

- [customer_landing_to_trusted.py](/src/customer_landing_to_trusted.py)
- [customer_trusted_to_curated.py](/src/customer_trusted_to_curated.py)
- [accelerometer_landing_to_trusted.py](/src/accelerometer_landing_to_trusted.py)
- [step_trainer_trusted.py](/src/step_trainer_landing_to_trusted.py)
- [machine_learning_curated.py](/src/machine_learning_curated.py)

## Landing Zone
  
### SQL DDL scripts
- [customer_landing.sql](/sql/customer_landing.sql)
- [accelerometer_landing.sql](/sql/accelerometer_landing.sql)
- [step_trainer_landing.sql](/sql/step_trainer_landing.sql)

### Screenshots
- Row count for `customer_landing` Expected value = 956 ![Count of customer_landing](/img/customer_landing_row_count.png)

- Customer Landing Table Contains rows with blank in `shareWithResearchAsOfDate`
  ![blank_sharewithresearchasofdate](/img/customer_landing_blank_sharewithresearchasofdate.png)

- Row count for `accelerometer_landing` Expected value = 81273
  ![accelerometer landing row count](/img/accelerometer_landing_row_count.png)

- Row count for `step_trainer_landing` Expected value = 28680
  ![step trainer landing row count](/img/step_trainer_landing_row_count.png)

## Trusted Zone

### Screenshots
- Row count for `customer_trusted` Expected value = 482
  ![customer trusted row count](/img/customer_trusted_row_count.png)
- No rows where `shareWithResearchAsOfDate` is blank
  ![sharewithresearchasofdate 0 rows](/img/customer_trusted_blank_sharewithresearchasofdate.png
- Row count for `accelerometer_trusted` Expected Value = 32025
  ![accelerometer trusted row count](/img/accelerometer_trusted_row_count.png)
- Row count for `step_trainer_trusted` Expected value < 14460
  ![step trainer trusted row count](/img/step_trainer_trusted_row_count.png)

## Curated Zone
- Row count for `customer_curated` Expected Value = 464
  ![customer curated row count](/img/customer_curated_row_count.png)
- Row count for `machine_learning_curated` Expected value = 34437
  ![machine learning curated row count](/img/machine_learning_row_count.png)
