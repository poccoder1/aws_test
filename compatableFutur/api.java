@RestController
public class AccountController {

    @Autowired
    private AccountProcessingService accountProcessingService;

    @GetMapping("/process-accounts")
    public ResponseEntity<List<List<Object>>> processAccounts(@RequestParam List<String> accountIds) {
        List<CompletableFuture<List<Object>>> futures = accountProcessingService.processAllAccounts(accountIds);

        CompletableFuture<Void> allOf = CompletableFuture.allOf(futures.toArray(new CompletableFuture[0]));

        CompletableFuture<List<Object>> combinedFuture = allOf.thenApply(v -> {
            return futures.stream()
                    .map(CompletableFuture::join)
                    .collect(Collectors.toList());
        });

        List<List<Object>> results = combinedFuture.join();
        return ResponseEntity.ok(results);
    }
}


========

        import org.springframework.scheduling.annotation.Async;
        import org.springframework.stereotype.Service;

@Service
public class AccountServiceImpl implements AccountService {

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
