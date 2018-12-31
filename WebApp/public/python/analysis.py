# Data load
# ',' was replace by '.'
base_df = sqlContext.read.format("com.databricks.spark.csv").options(header=True, inferSchema=True, delimiter=";").load("/FileStore/tables/base_teste-c46eb.csv")
print ("Quantidade de registros da base: {0}".format(base_df.count()))

# Print Schema in a tree format
base_df.cache()
base_df.printSchema()

#Seting the necessary fields as float type
base_new = base_df.select(base_df['*'], base_df.Value_vibracao.cast('float').alias("vibracao_new"))
base_new = base_new.select(base_new['*'], base_new.Average.cast('float').alias("average_new"))
base_new = base_new.select(base_new['*'], base_new.Value_speed.cast('float').alias("speed_new"))

# Print Schema in a tree format
base_new.cache()
base_new.printSchema()

#Cleaning the old fields
base_clean = base_new.drop('Value_vibracao').drop('Average').drop('Value_speed')
base_clean.printSchema()
base_clean.show()

#Perform descriptive analytics
base_clean.describe().toPandas().transpose()

# indicadores estatisticos para entender melhor a base de dadosbase_df.
from pyspark.sql.functions import mean, stddev
base_clean.select([stddev('vibracao_new')/mean('vibracao_new')]).show()
base_clean.select([stddev('speed_new')/mean('speed_new')]).show()

# correlation between independent variables and target variable
#import six
#for i in base_clean.columns:
 #   if not( isinstance(base_clean.select(i).take(1)[0][0], six.string_types)):
  #      print( "Correlation to vibracao for ", i, base_clean.stat.corr('vibracao_new',i))

from pyspark.ml.feature import VectorAssembler
vectorAssembler = VectorAssembler(inputCols = ['average_new','speed_new'], outputCol = 'features')
base_df = vectorAssembler.transform(base_clean)
base_df = base_df.select(['features', 'vibracao_new'])
base_df.show()

# Spliting the data between training and test

splits = base_df.randomSplit([0.9, 0.1])
train_df = splits[0]
test_df = splits[1]

# Linear Regression
from pyspark.ml.regression import LinearRegression
lr = LinearRegression(featuresCol = 'features', labelCol='vibracao_new', maxIter=10, regParam=0.3, elasticNetParam=0.8)
lr_model = lr.fit(train_df)
print("Coefficients: " + str(lr_model.coefficients))
print("Intercept: " + str(lr_model.intercept))

# Error metrics
trainingSummary = lr_model.summary
print("r2: %f" % trainingSummary.r2)

lr_predictions = lr_model.transform(test_df)
lr_predictions.select("prediction","vibracao_new","features").show(5)
from pyspark.ml.evaluation import RegressionEvaluator
lr_evaluator = RegressionEvaluator(predictionCol="prediction", \
                 labelCol="vibracao_new",metricName="r2")
print("R Squared (R2) on test data = %g" % lr_evaluator.evaluate(lr_predictions))

predictions = lr_model.transform(test_df)
predictions.select("prediction","vibracao_new","features").orderBy(predictions.prediction.desc()).show()