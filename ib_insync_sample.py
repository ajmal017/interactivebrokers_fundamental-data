# TODO: Fetch data with ib_insync, see https://github.com/erdewit/ib_insync

from ib_insync import IB, Forex, util
util.startLoop()  # uncomment this line when in a notebook

ib = IB()
ib.connect('127.0.0.1', 4001, clientId=2)

contract = Forex('EURUSD')
bars = ib.reqHistoricalData(
    contract, endDateTime='', durationStr='30 D',
    barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)

# convert to pandas dataframe:
df = util.df(bars)
print(df)

ib.disconnect()

from pyspark.sql import SparkSession
import os
# warehouseLocation = 'hdfs://localhost:9000/warehouse'
warehouseLocation = 'hdfs://localhost:8020/user/hive/warehouse'
os.environ["HADOOP_USER_NAME"] = "root"
spark = SparkSession.builder \
    .appName('appName') \
    .config('spark.driver.port', 8080) \
    .config("spark.sql.warehouse.dir", warehouseLocation) \
    .config('spark.driver.host', 'http://127.0.0.1:58896/api/v1/namespaces/default/services/spark:spark-master-6d4984666-s68v2:8080/proxy/#/') \
    .config('spark.sql.hive.thriftServer.singleSession', True) \
    .enableHiveSupport() \
    .getOrCreate()
spark
spark.sql("CREATE TABLE IF NOT EXISTS src (key INT, value STRING) USING hive")

spark.sql("LOAD DATA LOCAL INPATH 'sample.json' INTO TABLE src")
