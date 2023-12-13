import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Component
public class ServiceLocator {

    private final Map<String, ExtractorService> extractorServiceMap;
    private final Map<String, ValidatorService> validatorServiceMap;
    private final Map<String, EnricherService> enricherServiceMap;
    private final Map<String, ProducerService> producerServiceMap;
    private final Map<String, ArchiverService> archiverServiceMap;

    @Autowired
    public ServiceLocator(
            List<ExtractorService> extractorServices,
            List<ValidatorService> validatorServices,
            List<EnricherService> enricherServices,
            List<ProducerService> producerServices,
            List<ArchiverService> archiverServices
    ) {
        this.extractorServiceMap = new HashMap<>();
        this.validatorServiceMap = new HashMap<>();
        this.enricherServiceMap = new HashMap<>();
        this.producerServiceMap = new HashMap<>();
        this.archiverServiceMap = new HashMap<>();

        populateServiceMap(extractorServices, extractorServiceMap);
        populateServiceMap(validatorServices, validatorServiceMap);
        populateServiceMap(enricherServices, enricherServiceMap);
        populateServiceMap(producerServices, producerServiceMap);
        populateServiceMap(archiverServices, archiverServiceMap);
    }

    private <T> void populateServiceMap(List<T> services, Map<String, T> serviceMap) {
        for (T service : services) {
            String key = service.getClass().getAnnotation(Qualifier.class).value();
            serviceMap.put(key, service);
        }
    }

    public ExtractorService getExtractorService(String extractorType) {
        return extractorServiceMap.get(extractorType);
    }

    public ValidatorService getValidatorService(String validatorType) {
        return validatorServiceMap.get(validatorType);
    }

    public EnricherService getEnricherService(String enricherType) {
        return enricherServiceMap.get(enricherType);
    }

    public ProducerService getProducerService(String producerType) {
        return producerServiceMap.get(producerType);
    }

    public ArchiverService getArchiverService(String archiverType) {
        return archiverServiceMap.get(archiverType);
    }
}
