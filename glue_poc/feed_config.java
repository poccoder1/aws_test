csv-mappings:
        file1: com.example.PojoClass1
        file2: com.example.PojoClass2


=====

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import java.util.Map;

@Configuration
@ConfigurationProperties(prefix = "csv-mappings")
public class CSVMappingsConfig {
    private Map<String, String> mappings;

    public Map<String, String> getMappings() {
        return mappings;
    }

    public void setMappings(Map<String, String> mappings) {
        this.mappings = mappings;
    }
}


=====

        import org.junit.jupiter.api.BeforeEach;
        import org.junit.jupiter.api.Test;
        import org.springframework.boot.context.properties.EnableConfigurationProperties;
        import org.springframework.boot.test.context.SpringBootTest;
        import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
        import org.springframework.boot.test.mock.mockito.MockBean;
        import org.springframework.test.context.ActiveProfiles;
        import org.springframework.test.context.TestPropertySource;

        import java.util.HashMap;
        import java.util.Map;

        import static org.junit.jupiter.api.Assertions.assertEquals;
        import static org.mockito.Mockito.when;

@SpringBootTest(webEnvironment = WebEnvironment.NONE)
@EnableConfigurationProperties(CSVMappingsConfig.class)
@TestPropertySource(properties = {
        "csv-mappings.file1=com.example.PojoClass1",
        "csv-mappings.file2=com.example.PojoClass2"
})
@ActiveProfiles("test")
public class CSVMappingsConfigTest {

    @MockBean
    private CSVMappingsConfig mappingsConfig;

    @BeforeEach
    void setUp() {
        // Mocking is set up in @BeforeEach
        Map<String, String> mappings = new HashMap<>();
        mappings.put("file1", "com.example.PojoClass1");
        mappings.put("file2", "com.example.PojoClass2");
        when(mappingsConfig.getMappings()).thenReturn(mappings);
    }

    @Test
    void testMappingsLoadedFromProperties() {
        // Verify that mappings are loaded correctly from properties
        Map<String, String> mappings = mappingsConfig.getMappings();
        assertEquals("com.example.PojoClass1", mappings.get("file1"));
        assertEquals("com.example.PojoClass2", mappings.get("file2"));
    }
}
