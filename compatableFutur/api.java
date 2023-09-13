@RestController
public class AccountController {

    @Autowired
    private AccountProcessingService accountProcessingService;

    @GetMapping("/process-accounts")
    public ResponseEntity<List<List<Object>>> processAccounts(@RequestParam List<String> accountIds) {

        return ResponseEntity.ok(getAccountDetails(accountIds));
    }
}


========

        import org.springframework.scheduling.annotation.Async;
        import org.springframework.stereotype.Service;

@Service
public class AccountServiceImpl implements AccountService {

    public  List<List<Object>> getAccountDetails(List<String> accountIds){

        List<CompletableFuture<List<Object>>> futures = accountProcessingService.processAllAccounts(accountIds);

        CompletableFuture<Void> allOf = CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]));

        CompletableFuture<List<Object>> combinedFuture = allOf.thenApply(v -> {
            return futures.stream()
                    .map(CompletableFuture::join)
                    .collect(Collectors.toList());
        });

        List<List<Object>> results = combinedFuture.join();
        return results;
    }

    @Async
    @Override
    public CompletableFuture<List<Customer>> processAccount(String accountId) {
        // Simulate a database call to fetch a list of customers for the account
        List<Customer> customers = someDatabaseCall(accountId); // Implement this method

        // Wrap the list of customers in a completed CompletableFuture
        return CompletableFuture.completedFuture(customers);
    }

    // Implement this method to perform the actual database call
    private List<Customer> someDatabaseCall(String accountId) {
        // Your database retrieval logic here
    }
}



==========

        import org.junit.jupiter.api.BeforeEach;
        import org.junit.jupiter.api.Test;
        import org.mockito.Mockito;
        import org.springframework.boot.test.context.SpringBootTest;
        import org.springframework.boot.test.mock.mockito.MockBean;
        import org.springframework.scheduling.annotation.Async;

        import java.util.ArrayList;
        import java.util.Arrays;
        import java.util.List;
        import java.util.concurrent.CompletableFuture;

        import static org.junit.jupiter.api.Assertions.assertEquals;
        import static org.mockito.Mockito.when;

@SpringBootTest
public class AccountServiceImplTest {

    @MockBean
    private AccountService accountService;

    private AccountProcessingService accountProcessingService;

    @BeforeEach
    public void setUp() {
        accountProcessingService = new AccountProcessingService(accountService);
    }

    @Test
    public void testProcessAllAccounts() {
        // Arrange
        List<String> accountIds = Arrays.asList("1", "2", "3");

        // Create a list of CompletableFuture results to simulate
        List<CompletableFuture<List<Customer>>> futureResults = new ArrayList<>();
        futureResults.add(CompletableFuture.completedFuture(Arrays.asList(new Customer("John"), new Customer("Alice"))));
        futureResults.add(CompletableFuture.completedFuture(Arrays.asList(new Customer("Bob"), new Customer("Eve"))));
        futureResults.add(CompletableFuture.completedFuture(Arrays.asList(new Customer("Charlie"))));

        when(accountService.processAccount(Mockito.anyString())).thenAnswer(invocation -> {
            String accountId = invocation.getArgument(0);
            int index = Integer.parseInt(accountId) - 1;
            return futureResults.get(index);
        });

        // Act
        List<List<Object>> result = accountProcessingService.processAllAccounts(accountIds);

        // Assert
        assertEquals(3, result.size());
        assertEquals(2, result.get(0).size());
        assertEquals(2, result.get(1).size());
        assertEquals(1, result.get(2).size());
    }

    @Async
    @Test
    public void testProcessAccount() {
        // Arrange
        String accountId = "1";
        List<Customer> customers = Arrays.asList(new Customer("John"), new Customer("Alice"));

        when(accountService.processAccount(accountId)).thenReturn(CompletableFuture.completedFuture(customers));

        // Act
        CompletableFuture<List<Customer>> resultFuture = accountService.processAccount(accountId);

        // Assert
        List<Customer> result = resultFuture.join();
        assertEquals(2, result.size());
        assertEquals("John", result.get(0).getName());
        assertEquals("Alice", result.get(1).getName());
    }

    @Async
    @Test
    public void testProcessAccountWithEmptyResult() {
        // Arrange
        String accountId = "4"; // Simulate an account with no customers

        when(accountService.processAccount(accountId)).thenReturn(CompletableFuture.completedFuture(new ArrayList<>()));

        // Act
        CompletableFuture<List<Customer>> resultFuture = accountService.processAccount(accountId);

        // Assert
        List<Customer> result = resultFuture.join();
        assertEquals(0, result.size());
    }
}



==================

        import java.lang.reflect.Field;
        import java.util.*;
        import java.util.concurrent.CompletableFuture;
        import java.util.stream.Collectors;

public class AccountProcessor {
    public Map<String, Map<String, Object>> processAccounts(List<CompletableFuture<List<Account>>> futures) {
        // Wait for all CompletableFuture objects to complete and collect their results
        List<List<Account>> accountLists = futures.stream()
                .map(CompletableFuture::join)
                .collect(Collectors.toList());

        // Create the result map
        Map<String, Map<String, Object>> resultMap = new HashMap<>();

        // Iterate through the list of Account objects and organize data into the map
        for (List<Account> accounts : accountLists) {
            for (Account account : accounts) {
                String accountId = account.getAccountId();

                // Create or update the outer map with accountId
                resultMap.computeIfAbsent(accountId, k -> new HashMap<>());

                // Get all the fields of the Account class using reflection
                Field[] fields = Account.class.getDeclaredFields();

                // Iterate through the fields and add them to the inner map with their values
                for (Field field : fields) {
                    field.setAccessible(true);
                    try {
                        Object value = field.get(account);
                        resultMap.get(accountId).put(field.getName(), value);
                    } catch (IllegalAccessException e) {
                        e.printStackTrace(); // Handle the exception as needed
                    }
                }
            }
        }

        return resultMap;
    }
}
