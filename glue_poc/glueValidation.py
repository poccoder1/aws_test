 convert dynamic frame to data frame
df = dyf.toDF()

# capture output of df.show() using StringIO
output = StringIO()
df.show(10, False, True, False, False, False, truncate=False, file=output)
output_string = output.getvalue()

# log the captured output using logger.info()
logger.info("Printing DataFrame:\n" + output_string)