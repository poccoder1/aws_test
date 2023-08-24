file1=com.example.PojoClass1
        file2=com.example.PojoClass2
        file3=com.example.PojoClass3



==========

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.Resource;
import org.springframework.core.io.ResourceLoader;

import javax.annotation.PostConstruct;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;

@Configuration
public class CSVFileMappingConfiguration {

    private final ResourceLoader resourceLoader;

    @Value("${feed.config.file:classpath:/feed.config}")
    private Resource feedConfigResource;

    private Map<String, String> fileNameToPojoClassMapping = new HashMap<>();

    public CSVFileMappingConfiguration(ResourceLoader resourceLoader) {
        this.resourceLoader = resourceLoader;
    }

    @PostConstruct
    public void loadFileMappings() throws IOException {
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(feedConfigResource.getInputStream()))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split("=");
                if (parts.length == 2) {
                    fileNameToPojoClassMapping.put(parts[0], parts[1]);
                }
            }
        }
    }

    public String getPojoClassNameForFile(String fileName) {
        return fileNameToPojoClassMapping.get(fileName);
    }
}


===========
        import org.springframework.beans.factory.annotation.Autowired;
        import org.springframework.web.bind.annotation.GetMapping;
        import org.springframework.web.bind.annotation.RequestParam;
        import org.springframework.web.bind.annotation.RestController;

        import java.io.IOException;
        import java.util.List;

@RestController
public class CSVController {

    @Autowired
    private CSVService csvService;

    @Autowired
    private CSVFileMappingConfiguration fileMappingConfiguration;

    @GetMapping("/map-csv")
    public List<?> mapCSVToObject(@RequestParam String csvFilePath) throws IOException {
        // Get the mapping for the provided CSV file name
        String pojoClassName = fileMappingConfiguration.getPojoClassNameForFile(csvFilePath);

        if (pojoClassName == null) {
            throw new IllegalArgumentException("No mapping found for CSV file: " + csvFilePath);
        }

        try {
            Class<?> clazz = Class.forName(pojoClassName);
            return csvService.mapCSVToObject(csvFilePath, clazz);
        } catch (ClassNotFoundException e) {
            throw new IllegalArgumentException("Invalid POJO class name: " + pojoClassName);
        }
    }
}
