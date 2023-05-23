spring.kafka.bootstrap-servers=<kafka bootstrap servers>
spring.kafka.consumer.group-id=<kafka consumer group id>
spring.kafka.consumer.auto-offset-reset=earliest


@Component
public class FileDownloadStatusManager {
    private Map<String, FileState> fileStatusMap = new ConcurrentHashMap<>();

    public boolean isFileDownloaded(String fileName) {
        return fileStatusMap.getOrDefault(fileName, false);
    }

    public void setFileDownloaded(String fileName, FileState downloaded) {
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
        resetData fileDetails
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


    List<FileDetails>  fileList = fromDb;
    private Map<String, FileState> fileStatusMap = new ConcurrentHashMap<>();
    // state: Downloading, Download_complete

    @Scheduled(cron = SCHEDULER_INTERVAL_MS) // Runs every 10 min
    public void scheduleFile() {

        for(FileDetails file: fileDetails){

            if(days_to_Run, Start_time, end_time, fileStatusMap.get("file")){
                        kafkaPublish(file,fileStatusMap)
            }
         }
    }

    public void kafkaPublish(){
        try{

            kakfkaTemplate.send(file)
            fileStatusMap.put(fileName, Downloading)
        }catch(Exc){
            fileStatusMap.remove(fileName);
        }
    }

}


