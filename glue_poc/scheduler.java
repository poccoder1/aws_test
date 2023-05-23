spring.kafka.bootstrap-servers=<kafka bootstrap servers>
spring.kafka.consumer.group-id=<kafka consumer group id>
spring.kafka.consumer.auto-offset-reset=earliest


@Component
public class FileDownloadStatusManager {
    private Map<String, FileState> fileStatusMap = new ConcurrentHashMap<>();

    public boolean isFileDownloaded(String fileName) {
        return fileStatusMap.getOrDefault(fileName, false);
    }

    public void setFileDownloaded(String fileName, boolean downloaded) {
        fileStatusMap.put(fileName, downloaded);
    }

    public void resetStatus() {
        fileStatusMap.clear();
    }
}

// run from scheduler
    @Scheduled(cron = "0 0 0 * * ?") // Runs daily at midnight
    public void resetProperties() {
        fileDownloadStatusManager.resetStatus();
        // Reset any other properties or data structures as needed
    }


@Component
public class FileDownloadStatusUpdater {
    private FileDownloadStatusManager fileDownloadStatusManager;

    @Autowired
    public FileDownloadStatusUpdater(FileDownloadStatusManager fileDownloadStatusManager) {
        this.fileDownloadStatusManager = fileDownloadStatusManager;
    }

    @KafkaListener(topics = "file.download.topic", groupId = "file-download-group")
    public void updateFileDownloadStatus(String file, FileState fileState) {
        fileDownloadStatusManager.setFileDownloaded(file, fileState);
    }
}


import org.springframework.scheduling.annotation.Async;
        import org.springframework.scheduling.annotation.Scheduled;
        import org.springframework.stereotype.Component;
        import org.springframework.web.client.RestTemplate;

        import java.util.List;

@Component
public class FileDownloadScheduler {

    private static final long SCHEDULER_INTERVAL_MS = 10 * 60 * 1000; // 10 minutes
    private final FileRepository fileRepository;
    private final RestTemplate restTemplate;
    private final DownloadService downloadService;

    public FileDownloadScheduler(FileRepository fileRepository, RestTemplate restTemplate, DownloadService downloadService) {
        this.fileRepository = fileRepository;
        this.restTemplate = restTemplate;
        this.downloadService = downloadService;
    }

    @Async
    @Scheduled(fixedDelay = SCHEDULER_INTERVAL_MS)
    public void runScheduler() {
        // Get the files to download
        List<File> filesToDownload = fileRepository.getFilesToDownload();

        for (File file : filesToDownload) {
            // Check if the file is already being downloaded
            if (!downloadService.isDownloading(file.getId())) {
                // Call the download service asynchronously
                downloadService.downloadFileAsync(file.getId());
            }
        }
    }
}


