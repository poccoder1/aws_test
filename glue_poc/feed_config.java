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


=================

        import org.junit.jupiter.api.BeforeEach;
        import org.junit.jupiter.api.Test;
        import org.mockito.InjectMocks;
        import org.mockito.Mock;
        import org.mockito.MockitoAnnotations;
        import org.springframework.core.io.Resource;
        import org.springframework.core.io.ResourceLoader;

        import java.io.ByteArrayInputStream;
        import java.io.IOException;
        import java.nio.charset.StandardCharsets;

        import static org.junit.jupiter.api.Assertions.assertEquals;
        import static org.mockito.Mockito.when;

public class CSVFileMappingConfigurationTest {

    @InjectMocks
    private CSVFileMappingConfiguration configuration;

    @Mock
    private ResourceLoader resourceLoader;

    @Mock
    private Resource resource;

    @BeforeEach
    public void setup() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testLoadFileMappings() throws IOException {
        // Define the content of the feed.config file
        String configFileContent = "file1=com.example.PojoClass1\nfile2=com.example.PojoClass2\n";

        // Create a ByteArrayInputStream to simulate the resource
        ByteArrayInputStream inputStream = new ByteArrayInputStream(configFileContent.getBytes(StandardCharsets.UTF_8));

        // Mock the resourceLoader to return the ByteArrayInputStream when loading the resource
        when(resourceLoader.getResource("classpath:/feed.config")).thenReturn(resource);
        when(resource.getInputStream()).thenReturn(inputStream);

        // Load file mappings
        configuration.loadFileMappings();

        // Verify that mappings are loaded correctly
        assertEquals("com.example.PojoClass1", configuration.getPojoClassNameForFile("file1"));
        assertEquals("com.example.PojoClass2", configuration.getPojoClassNameForFile("file2"));
    }

    @Test
    public void testGetPojoClassNameForFile_NotFound() {
        // Test when the file mapping is not found
        assertEquals(null, configuration.getPojoClassNameForFile("nonExistentFile"));
    }
}

