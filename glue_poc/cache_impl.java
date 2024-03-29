import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class AccountService {

    @Autowired
    private ExternalApiService externalApiService;

    @Autowired
    private CacheManager cacheManager;

    @Cacheable("accountCache")
    public Map<String, Account> getAllAccounts() {
        return externalApiService.fetchAllAccounts();
    }

    public Account getAccountById(String accountId) {
        Map<String, Account> accountMap = getAllAccounts();
        Account account = accountMap.get(accountId);
        if (account == null) {
            // Account not found in cache, fetch it from the external API
            account = externalApiService.fetchAccountById(accountId);

            // Update the cache with the new account data
            cacheManager.getCache("accountCache").put(accountId, account);
        }
        return account;
    }

    // Optional: You can use this method to manually evict a specific account from the cache
    @CacheEvict(value = "accountCache", key = "#accountId")
    public void evictAccountFromCache(String accountId) {
    }
}



==============

        import org.springframework.stereotype.Service;
        import org.springframework.web.client.RestTemplate;
        import java.util.Map;

@Service
public class ExternalApiService {

    private final ExternalApi api;


    public completedFuture<List<ApiResponse> fetchAllAccounts() {
        ExternalApiRes res = api.getService();
        List<ApiResponse> response = res.call("test");

        return CompatableFuture.completedFuture(response);
    }
}


==========
        import org.springframework.beans.factory.annotation.Autowired;
        import org.springframework.cache.annotation.CacheEvict;
        import org.springframework.cache.annotation.Cacheable;
        import org.springframework.stereotype.Service;

        import java.util.Map;

@Service
public class AccountService {

    @Autowired
    private ExternalApiService externalApiService;

    @Autowired
    private CacheManager cacheManager;

    @Cacheable("accountCache")
    public Map<String, Account> getAllAccounts() {
        return externalApiService.fetchAllAccounts();
    }

    public Account getAccountById(String accountId) {
        Map<String, Account> accountMap = getAllAccounts();
        return accountMap.get(accountId);
    }

    // This method will force refresh of the cache by calling the external API
    public void refreshAccountCache() {
        Map<String, Account> refreshedAccounts = externalApiService.fetchAllAccounts();
        cacheManager.getCache("accountCache").clear(); // Clear the existing cache
        cacheManager.getCache("accountCache").putAll(refreshedAccounts); // Update cache with new data
    }

    // Optional: You can use this method to manually evict a specific account from the cache
    @CacheEvict(value = "accountCache", key = "#accountId")
    public void evictAccountFromCache(String accountId) {
    }
}


=========
        import org.springframework.beans.factory.annotation.Autowired;
        import org.springframework.scheduling.annotation.Scheduled;
        import org.springframework.stereotype.Component;

@Component
public class CacheRefreshScheduler {

    @Autowired
    private AccountService accountService;

    @Scheduled(cron = "0 0 0 * * ?") // Run every midnight
    public void refreshCache() {
        // Fetch new account data from the external API and update the cache
        accountService.refreshAccountCache();
    }
}


=======

        import org.junit.jupiter.api.Test;
        import org.mockito.Mockito;
        import org.springframework.beans.factory.annotation.Autowired;
        import org.springframework.boot.test.context.SpringBootTest;
        import org.springframework.boot.test.mock.mockito.MockBean;
        import org.springframework.test.context.TestPropertySource;

@SpringBootTest
@TestPropertySource(locations = "classpath:test.properties") // Use a test properties file if needed
public class CacheRefreshSchedulerTest {

    @Autowired
    private CacheRefreshScheduler cacheRefreshScheduler;

    @MockBean
    private AccountService accountService;

    @Test
    public void testRefreshCache() {
        // Mock the behavior of accountService.refreshAccountCache()
        Mockito.doNothing().when(accountService).refreshAccountCache();

        // Trigger the scheduler's refreshCache method
        cacheRefreshScheduler.refreshCache();

        // Verify that accountService.refreshAccountCache() was called once
        Mockito.verify(accountService, Mockito.times(1)).refreshAccountCache();
    }
}


=========

        import org.junit.jupiter.api.Test;
        import org.mockito.Mock;
        import org.mockito.Mockito;
        import org.springframework.beans.factory.annotation.Autowired;
        import org.springframework.boot.test.context.SpringBootTest;
        import org.springframework.cache.Cache;
        import org.springframework.cache.CacheManager;
        import org.springframework.boot.test.mock.mockito.MockBean;

        import java.util.HashMap;
        import java.util.Map;

@SpringBootTest
public class AccountServiceTest {

    @Autowired
    private AccountService accountService;

    @MockBean
    private ExternalApiService externalApiService;

    @Autowired
    private CacheManager cacheManager;

    @Test
    public void testGetAllAccountsCacheHit() {
        // Mock cache behavior
        Cache cache = cacheManager.getCache("accountCache");
        Map<String, Account> cachedAccounts = new HashMap<>();
        cachedAccounts.put("1", new Account("1", "Account 1"));
        cache.put("accountCache", cachedAccounts);

        // Call the service method
        Map<String, Account> accounts = accountService.getAllAccounts();

        // Verify that the cached data is returned
        Mockito.verify(externalApiService, Mockito.never()).fetchAllAccounts();
        // Add additional assertions as needed
    }

    @Test
    public void testGetAllAccountsCacheMiss() {
        // Mock the behavior of externalApiService
        Map<String, Account> freshAccounts = new HashMap<>();
        freshAccounts.put("1", new Account("1", "Account 1"));
        Mockito.when(externalApiService.fetchAllAccounts()).thenReturn(freshAccounts);

        // Call the service method
        Map<String, Account> accounts = accountService.getAllAccounts();

        // Verify that the externalApiService.fetchAllAccounts() was called once
        Mockito.verify(externalApiService, Mockito.times(1)).fetchAllAccounts();
        // Add additional assertions as needed
    }
}


=====
        import org.junit.jupiter.api.Test;
        import org.springframework.beans.factory.annotation.Autowired;
        import org.springframework.boot.test.context.SpringBootTest;
        import org.springframework.boot.web.client.RestTemplateBuilder;
        import org.springframework.boot.test.mock.mockito.MockBean;
        import org.springframework.web.client.RestTemplate;

        import java.util.HashMap;
        import java.util.Map;

        import static org.mockito.Mockito.*;

@SpringBootTest
public class ExternalApiServiceTest {

    @Autowired
    private ExternalApiService externalApiService;


    @Test
    public void testFetchAllAccounts() {
        // Mock the behavior of the RestTemplate (you can customize this based on your actual implementation)
        RestTemplate restTemplate = mock(RestTemplate.class);
        when(restTemplateBuilder.build()).thenReturn(restTemplate);

        // Mock the response from the external API
        Map<String, Account> expectedAccounts = new HashMap<>();
        expectedAccounts.put("1", new Account("1", "Account 1"));
        when(restTemplate.getForObject(anyString(), eq(Map.class))).thenReturn(expectedAccounts);

        // Call the service method
        Map<String, Account> accounts = externalApiService.fetchAllAccounts();

        // Verify that the expected data is returned
        // Add additional assertions as needed
    }

    // Similar tests for fetchAccountById can be added
}



==================test


        import org.junit.jupiter.api.BeforeEach;
        import org.junit.jupiter.api.Test;
        import org.mockito.InjectMocks;
        import org.mockito.Mock;
        import org.mockito.MockitoAnnotations;
        import org.springframework.scheduling.annotation.Scheduled;

        import static org.mockito.Mockito.*;

public class CacheRefreshSchedulerTest {

    @InjectMocks
    private CacheRefreshScheduler cacheRefreshScheduler;

    @Mock
    private AccountService accountService;

    @BeforeEach
    public void setUp() {
        // Initialize mockito mocks
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testRefreshCacheScheduled() {
        // Assuming that the @Scheduled cron expression runs at midnight

        // Mock the behavior of refreshAccountCache method
        doNothing().when(accountService).refreshAccountCache();

        // Manually invoke the scheduled method (since it's scheduled at midnight)
        cacheRefreshScheduler.refreshCache();

        // Verify that the refreshAccountCache method was called exactly once
        verify(accountService, times(1)).refreshAccountCache();
    }
}


============new test


        import org.junit.jupiter.api.BeforeEach;
        import org.junit.jupiter.api.Test;
        import org.mockito.InjectMocks;
        import org.mockito.Mock;
        import org.mockito.MockitoAnnotations;

        import java.util.Arrays;
        import java.util.List;
        import java.util.concurrent.CompletableFuture;

        import static org.junit.jupiter.api.Assertions.assertEquals;
        import static org.mockito.Mockito.*;

public class ExternalApiServiceTest {

    @InjectMocks
    private ExternalApiService externalApiService;

    @Mock
    private ExternalApi externalApi;

    @BeforeEach
    public void setUp() {
        // Initialize Mockito mocks
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testFetchAllAccounts() {
        // Prepare test data
        ExternalApiRes externalApiRes = new ExternalApiRes();
        List<ApiResponse> testData = Arrays.asList(new ApiResponse("1", "John"), new ApiResponse("2", "Doe"));

        // Mock external API behavior
        when(externalApi.getService()).thenReturn(externalApiRes);
        when(externalApiRes.call("test")).thenReturn(testData);

        // Call the method under test
        CompletableFuture<List<ApiResponse>> result = externalApiService.fetchAllAccounts();

        // Verify that the external API service was called
        verify(externalApi, times(1)).getService();
        verify(externalApiRes, times(1)).call("test");

        // Verify the result
        assertEquals(testData, result.join());
    }
}


=========cacheconfig=====

        import com.github.benmanes.caffeine.cache.Caffeine;
        import org.junit.jupiter.api.BeforeEach;
        import org.junit.jupiter.api.Test;
        import org.mockito.InjectMocks;
        import org.mockito.Mock;
        import org.mockito.MockitoAnnotations;
        import org.springframework.cache.CacheManager;
        import org.springframework.cache.caffeine.CaffeineCacheManager;

        import java.util.concurrent.TimeUnit;

        import static org.junit.jupiter.api.Assertions.assertEquals;
        import static org.mockito.Mockito.when;

public class CacheConfigTest {

    @InjectMocks
    private CacheConfig cacheConfig;

    @Mock
    private Caffeine<Object, Object> caffeine;

    @BeforeEach
    public void setUp() {
        // Initialize Mockito mocks
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testCacheManager() {
        // Create a CaffeineCacheManager
        CaffeineCacheManager expectedCacheManager = new CaffeineCacheManager();
        expectedCacheManager.setCaffeine(caffeine);

        // Mock the behavior of caffeineConfig to return the configured Caffeine object
        when(caffeine.expireAfterWrite(300, TimeUnit.SECONDS)).thenReturn(caffeine);
        when(caffeine.initialCapacity(10)).thenReturn(caffeine);

        // Call the method under test
        CacheManager result = cacheConfig.cacheManager(caffeine);

        // Verify that the result is the expected CaffeineCacheManager
        assertEquals(expectedCacheManager, result);
    }
}
