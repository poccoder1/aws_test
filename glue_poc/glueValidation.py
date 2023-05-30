dynamic_frame = glueContext.create_dynamic_frame.from_catalog(frame=input_df, database='your_database_name', table_name='your_table_name')

glueContext.write_dynamic_frame.from_catalog(frame=dynamic_frame, database='your_database_name', table_name='your_table_name')

job.commit()
