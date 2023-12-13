import java.util.Map;

public interface ValidatorService {
    void validate(Map<String, Object> validatorConfig, Dataset<Row> inputDataset);
}


import org.apache.spark.sql.Dataset;
        import org.apache.spark.sql.Row;
        import org.apache.spark.sql.functions;
        import org.springframework.stereotype.Service;

        import java.util.Map;

@Service
@Qualifier("LENGTH_VALIDATOR")
public class LengthValidatorServiceImpl implements ValidatorService {

    @Override
    public void validate(Map<String, Object> validatorConfig, Dataset<Row> inputDataset) {
        for (Map.Entry<String, Object> entry : validatorConfig.entrySet()) {
            String columnName = entry.getKey();
            int maxLength = (Integer) entry.getValue();

            inputDataset = inputDataset.withColumn("length_validation", functions.when(functions.length(columnName).$greater(maxLength), "invalid").otherwise("valid"));
        }

        inputDataset.show(); // Displaying the result, you can modify as per your requirements
    }
}
