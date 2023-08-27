import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.cache.caffeine.CaffeineCacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import com.github.benmanes.caffeine.cache.Caffeine;
import java.util.concurrent.TimeUnit;

@Configuration
@EnableCaching
public class CacheConfig {

    @Bean
    public CacheManager cacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager();
        cacheManager.setCaffeine(Caffeine.newBuilder()
                .expireAfterWrite(Long.MAX_VALUE, TimeUnit.NANOSECONDS) // Set to a very large value
                .maximumSize(1) // Store a single entry for the HashMap
                .maximumWeight(300 * 1024 * 1024) // Max size in bytes (300MB)
                .build());
        return cacheManager;
    }
}


========

        import org.slf4j.Logger;
        import org.slf4j.LoggerFactory;
        import org.springframework.beans.factory.annotation.Autowired;
        import org.springframework.cache.Cache;
        import org.springframework.cache.CacheManager;
        import org.springframework.stereotype.Service;
        import org.springframework.web.client.HttpClientErrorException;
        import org.springframework.web.client.RestTemplate;

        import java.util.HashMap;
        import java.util.List;
        import java.util.Map;

@Service
public class CustomerService {

    private static final Logger log = LoggerFactory.getLogger(CustomerService.class);

    private final CacheManager cacheManager;
    private final RestTemplate restTemplate;

    @Autowired
    public CustomerService(CacheManager cacheManager, RestTemplate restTemplate) {
        this.cacheManager = cacheManager;
        this.restTemplate = restTemplate;
    }

    public Map<Long, Customer> getCustomersByIds(List<Long> customerIds) {
        Map<Long, Customer> customersMap = new HashMap<>();

        for (Long customerId : customerIds) {
            Customer customer = getCustomerById(customerId);
            if (customer != null) {
                customersMap.put(customerId, customer);
            }
        }

        return customersMap;
    }

    public Customer getCustomerById(Long customerId) {
        Cache cache = cacheManager.getCache("customers");
        if (cache != null) {
            Cache.ValueWrapper valueWrapper = cache.get("customerMap");
            if (valueWrapper != null) {
                Map<Long, Customer> cachedCustomerMap = (Map<Long, Customer>) valueWrapper.get();
                if (cachedCustomerMap != null) {
                    if (cachedCustomerMap.containsKey(customerId)) {
                        Customer customer = cachedCustomerMap.get(customerId);
                        log.info("Customer with ID {} found in cache.", customerId);
                        return customer;
                    }
                }
            }
        }

        Customer customer = fetchCustomerDataFromAPI(customerId);
        if (customer != null) {
            updateCustomerInCache(customerId, customer);
        }

        return customer;
    }

    private Customer fetchCustomerDataFromAPI(Long customerId) {
        try {
            // Replace the URL with your actual API endpoint for fetching customer data
            String apiUrl = "https://your-api.com/customers/" + customerId;
            Customer customer = restTemplate.getForObject(apiUrl, Customer.class);
            log.info("Fetched customer data for ID {} from external API.", customerId);
            return customer;
        } catch (HttpClientErrorException.NotFound notFoundException) {
            log.error("Customer with ID {} not found in the external API.", customerId);
            return null;
        } catch (Exception e) {
            log.error("Failed to fetch customer data from the external API for ID {}.", customerId, e);
            return null;
        }
    }

    private void updateCustomerInCache(Long customerId, Customer customer) {
        Cache cache = cacheManager.getCache("customers");
        if (cache != null) {
            Cache.ValueWrapper valueWrapper = cache.get("customerMap");
            if (valueWrapper != null) {
                Map<Long, Customer> cachedCustomerMap = (Map<Long, Customer>) valueWrapper.get();
                if (cachedCustomerMap != null) {
                    cachedCustomerMap.put(customerId, customer);
                    cache.put("customerMap", cachedCustomerMap);
                } else {
                    // If the cache is empty, create a new map with the customer and store it in the cache
                    Map<Long, Customer> newCustomerMap = new HashMap<>();
                    newCustomerMap.put(customerId, customer);
                    cache.put("customerMap", newCustomerMap);
                }
            } else {
                // If the cache value is not found, create a new map with the customer and store it in the cache
                Map<Long, Customer> newCustomerMap = new HashMap<>();
                newCustomerMap.put(customerId, customer);
                cache.put("customerMap", newCustomerMap);
            }
        }
    }

}


