import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class ETLService {

    private final ServiceLocator serviceLocator;

    @Autowired
    public ETLService(ServiceLocator serviceLocator) {
        this.serviceLocator = serviceLocator;
    }

    public void process(Config config, String name) {
        Dataset<Row> inputDataset = null;
        for (Step step : config.getConfig()) {
            if (step.getName().equals(name)) {
                processSteps(step.getSteps(), inputDataset);
                break;
            }
        }
    }

    private void processSteps(List<StepType> steps, Dataset<Row> inputDataset) {
        if (steps != null) {
            for (StepType stepType : steps) {
                switch (stepType.getType()) {
                    case EXTRACTOR:
                        inputDataset = extractData((Map<String, Object>) stepType.getStep());
                        break;
                    case VALIDATOR:
                        validateData((Map<String, Object>) stepType.getStep(), inputDataset);
                        break;
                    case ENRICHER:
                        enrichData((Map<String, Object>) stepType.getStep(), inputDataset);
                        break;
                    case PRODUCER:
                        produceData((Map<String, Object>) stepType.getStep(), inputDataset);
                        break;
                    case ARCHIVER:
                        archiveData((Map<String, Object>) stepType.getStep(), inputDataset);
                        break;
                    // Add more cases as needed for additional step types
                }
            }
        }
    }

    private Dataset<Row> extractData(Map<String, Object> extractorConfig) {
        String extractorType = (String) extractorConfig.keySet().iterator().next();
        ExtractorService extractorService = serviceLocator.getExtractorService(extractorType);
        return extractorService.extract(extractorConfig);
    }

    private void validateData(Map<String, Object> validatorConfig, Dataset<Row> inputDataset) {
        String validatorType = (String) validatorConfig.keySet().iterator().next();
        ValidatorService validatorService = serviceLocator.getValidatorService(validatorType);
        validatorService.validate(validatorConfig, inputDataset);
    }

    private void enrichData(Map<String, Object> enricherConfig, Dataset<Row> inputDataset) {
        String enricherType = (String) enricherConfig.keySet().iterator().next();
        EnricherService enricherService = serviceLocator.getEnricherService(enricherType);
        inputDataset = enricherService.enrich(enricherConfig, inputDataset);
    }

    private void produceData(Map<String, Object> producerConfig, Dataset<Row> inputDataset) {
        String producerType = (String) producerConfig.keySet().iterator().next();
        ProducerService producerService = serviceLocator.getProducerService(producerType);
        producerService.produce(producerConfig, inputDataset);
    }

    private void archiveData(Map<String, Object> archiverConfig, Dataset<Row> inputDataset) {
        String archiverType = (String) archiverConfig.keySet().iterator().next();
        ArchiverService archiverService = serviceLocator.getArchiverService(archiverType);
        archiverService.archive(archiverConfig, inputDataset);
    }
}
