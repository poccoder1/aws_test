import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;

import java.util.Map;

public interface ExtractorService {
    Dataset<Row> extract(Map<String, Object> extractorConfig);
}


import org.apache.spark.sql.Dataset;
        import org.apache.spark.sql.Row;
        import org.apache.spark.sql.SparkSession;
        import org.springframework.stereotype.Service;

        import java.util.Map;

@Service
@Qualifier("CSV_EXTRACTOR")
public class CsvExtractorServiceImpl implements ExtractorService {

    @Override
    public Dataset<Row> extract(Map<String, Object> extractorConfig) {
        SparkSession spark = SparkSession.builder().getOrCreate();

        String sourcePath = (String) extractorConfig.get("sourcePath");
        boolean ignoreFirstRow = (Boolean) extractorConfig.get("ignoreFirstRow");
        String delimiter = (String) extractorConfig.get("delimiter");
        Map<String, String> schema = (Map<String, String>) extractorConfig.get("schema");

        Dataset<Row> csvDataset = spark.read()
                .option("header", String.valueOf(ignoreFirstRow))
                .option("delimiter", delimiter)
                .csv(sourcePath);

        for (Map.Entry<String, String> entry : schema.entrySet()) {
            csvDataset = csvDataset.withColumn(entry.getKey(), functions.col(entry.getKey()).cast(entry.getValue()));
        }

        return csvDataset;
    }
}
