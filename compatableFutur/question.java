I need to create python web application along with spark job for ETl processing.
        Below are the use case.
        consider i have 100 input files with different extensions.
        I am planning to create configuration json for each input file.
        Below is sample json format.

        {
        "config": [
        {
        "name": "test_file_operation",
        "extractor":{
        "CSV":{
        "sourcePath": "/home/data/test.csv",
        "extractorType": "CSV_EXTRACTOR",
        "ignoreFirstRow": true,
        "delimeter": ",",
        "schema":{
        "col1": "String",
        "col2": "String",
        "col3": "String",
        "col4": "String",
        "col5": "String",
        "col6": "String"
        }
        }

        },
        "validator":{
        "LENGTH":{
        "LESS_THAN":[{
        "col1": 10
        },
        {
        "col2": 13
        },
        {
        "col3": 63
        },
        {
        "col4": 43
        },
        {
        "col5": 33
        },
        {
        "col6": 23
        }
        ],
        "EQUAL":[{

        "col2": 13
        },
        {
        "col3": 63
        },
        {
        "col4": 43
        }]
        },
        "LENGTH_type":{
        "col1":"text",
        "col2":"text",
        "col3":"text",
        "col4":"text"
        }
        }
        },
        {
        "enricher": {
        "DATA_MAN":{
        "sql": "select * from temp"
        }
        }
        },
        {
        "appender": {
        "DATA_MAN":{
        "sql": "select * from temp"
        }
        }
        }
        ,
        {
        "enricher": {
        "BUSINESS_DATE":{
        "sql": "select * from temp"
        }
        }
        }
        ,
        {
        "producer": {
        "DB":{
        "sql": "select * from temp"
        }
        }
        },
        {
        "archiver": {
        "DATA_MAN":{
        "sql": "select * from temp"
        }
        }
        }
        ]
        }

        similer json will be for each input file.

        I need to create python class for this json and load all json into class object.
        Also need to create on rest controller which will take name as parameter (here name is nothing but json "name" properties like  "test_file_operation". based on the rest input program should get respective object and perform sequential operation mentioned in json.
        in json file has mention: extractor, validator, enricher, producer, archiver are nothing but different services.
        extractor:  Consider i have different types of files like TXT,CSV, xls, pdf, xlsx, xml
        based on    "extractorType": "CSV_EXTRACTOR", it should call respective extrator  type method of service.
        so what ever mentioned in json file it should call respective service class method. also use spark for etl purpose.
        enricher:  enricher service also have different method like DATA_MAN, BUSINESS_DATE. then it should call that method.
        producer:  producer service also have different method like DB, file. based on json parameter it should call that method.
        Here use spark for data read, processing and load purpose. so we can able to query on spark df.
give full example with complete python project configuration, requirment.txt file and all the code.

=================================== split file workflow case===========
@Service
public class WorkflowService {

    private static final Logger logger = LoggerFactory.getLogger(WorkflowService.class);

    @Autowired
    private WorkflowRepository workflowRepository;

    @Autowired
    private RestTemplate restTemplate;

    public void startWorkflow(FileProcessRequest request) {
        List<WorkflowStep> steps = workflowRepository.findWorkflowByFileType(request.getFileType());

        logger.info("Starting workflow for file_type: {}, batch_id: {}, business_date: {}, file_name: {}",
                request.getFileType(), request.getBatchId(), request.getBusinessDate(), request.getFileName());

        for (WorkflowStep step : steps) {
            try {
                String generatedFileName = null;
                String newFileType = null;

                // Handle GFF processing and renaming logic
                if (step.getServiceName().equals("GFF")) {
                    GFFResponse gffResponse = callGFFService(request, step.getUrlPath());

                    // Track the renamed file for further workflow processing
                    if (gffResponse.isFileRenamed()) {
                        generatedFileName = gffResponse.getRenamedFileName();
                        newFileType = gffResponse.getNewFileType();
                    }
                }
                // Handle GFP processing logic, which may generate an output file
                else if (step.getServiceName().equals("GFP")) {
                    GFPResponse gfpResponse = callGFPService(request, step.getUrlPath());

                    if (gfpResponse.isFileGenerated()) {
                        generatedFileName = gfpResponse.getGeneratedFileName();
                        newFileType = gfpResponse.getNewFileType(); // e.g., MPT_output_CSV
                        logger.info("New output file {} with file_type {} generated by GFP", generatedFileName, newFileType);
                    }
                } else {
                    callService(step.getServiceName(), request, step.getUrlPath());
                }

                // Start new workflow for the renamed or generated file
                if (generatedFileName != null && newFileType != null) {
                    FileProcessRequest newRequest = new FileProcessRequest();
                    newRequest.setBatchId(request.getBatchId());
                    newRequest.setFileType(newFileType); // e.g., MPT_CSV_INPUT or MPT_output_CSV
                    newRequest.setFileName(generatedFileName);  // e.g., MTP_output.csv
                    newRequest.setBusinessDate(request.getBusinessDate());
                    newRequest.setOriginalFileName(request.getOriginalFileName());

                    // Start a new workflow for the generated or renamed file
                    startWorkflow(newRequest);
                }

                // Proceed with the next step in the workflow
                logger.info("Completed step_order {} for service: {}, batch_id: {}, file_name: {}",
                        step.getStepOrder(), step.getServiceName(), request.getBatchId(), request.getFileName());

            } catch (Exception e) {
                logger.error("Error occurred while executing step_order {} for service {} in batch_id {}: {}",
                        step.getStepOrder(), step.getServiceName(), request.getBatchId(), e.getMessage());
                updateBatchStatus(request.getBatchId(), request.getFileType(), "Failed", step.getStepOrder(), request.getBusinessDate());
                throw new RuntimeException("Workflow execution failed at step_order: " + step.getStepOrder(), e);
            }
        }

        logger.info("Completed workflow for file_type: {}, batch_id: {}, business_date: {}, file_name: {}",
                request.getFileType(), request.getBatchId(), request.getBusinessDate(), request.getFileName());
    }

    /**
     * Call GFP service and handle output file generation.
     */
    private GFPResponse callGFPService(FileProcessRequest request, String urlPath) {
        String serviceUrl = getServiceUrl("GFP", urlPath);

        logger.info("Calling GFP service: {}, url: {}, for batch_id: {}, file_type: {}, business_date: {}, file_name: {}",
                serviceUrl, request.getBatchId(), request.getFileType(), request.getBusinessDate(), request.getFileName());

        ResponseEntity<GFPResponse> response = restTemplate.postForEntity(serviceUrl, request, GFPResponse.class);

        if (response.getStatusCode().is2xxSuccessful()) {
            GFPResponse gfpResponse = response.getBody();
            if (gfpResponse != null) {
                return gfpResponse;
            }
        } else {
            logger.error("Failed to complete step for GFP service, batch_id: {}, file_type: {}, business_date: {}, file_name: {}. Status: {}",
                    request.getBatchId(), request.getFileType(), request.getBusinessDate(), request.getFileName(), response.getStatusCode());
            throw new RuntimeException("GFP service call failed with status: " + response.getStatusCode());
        }

        return null;
    }

    // Other methods remain the same (callGFFService, callService, etc.)
}


====
        CREATE TABLE file_process_status (
        id BIGINT PRIMARY KEY AUTO_INCREMENT,
        batch_id BIGINT NOT NULL,
        file_type VARCHAR(50) NOT NULL,
        file_name VARCHAR(255) NOT NULL,
        original_file_name VARCHAR(255) NOT NULL, -- Keeps track of original file
        linked_file_id BIGINT, -- Links to parent file if generated from another file
        status VARCHAR(20) NOT NULL,
        step_order INT NOT NULL,
        service_name VARCHAR(50) NOT NULL,
        business_date DATE NOT NULL,
        version INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

        FOREIGN KEY (linked_file_id) REFERENCES file_process_status(id)
        );


