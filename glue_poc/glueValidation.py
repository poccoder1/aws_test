output = "\n".join([str(row) for row in df.limit(10).collect()])
