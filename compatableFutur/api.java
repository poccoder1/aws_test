// Maven Dependencies

<!-- Spark Dependencies -->
<dependency>
<groupId>org.apache.spark</groupId>
<artifactId>spark-core_2.12</artifactId>
<version>3.1.2</version>
</dependency>
<dependency>
<groupId>org.apache.spark</groupId>
<artifactId>spark-sql_2.12</artifactId>
<version>3.1.2</version>
</dependency>

<!-- Add other dependencies based on the file types you want to support (e.g., CSV, XML, PDF) -->
<!-- For CSV -->
<dependency>
<groupId>com.databricks</groupId>
<artifactId>spark-csv_2.12</artifactId>
<version>1.5.0</version>
</dependency>

<!-- For XML -->
<dependency>
<groupId>com.databricks</groupId>
<artifactId>spark-xml_2.12</artifactId>
<version>0.13.0</version>
</dependency>

//  application proper

        // application-local.properties
        spring.spark.master=local
        spring.spark.app.name=SparkFileReaderLocal

// use spark session object in class
import org.apache.spark.sql.SparkSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
@Autowired
private SparkSession sparkSession;
/////