Step 1: Step function will listen to S3 event notification.

You can configure the Step Functions workflow to start when an S3 event occurs.
The trigger can be an S3 bucket event, such as an object creation or modification event.
Step 2: Lambda function checks if the required files are present or not.

Define a state in the Step Functions workflow to invoke this Lambda function.
Use a Choice state to check the result of the Lambda invocation. If the required files are present, proceed to the next step. Otherwise, handle the condition accordingly (e.g., send an error notification, terminate the workflow, or retry the check).
Step 3: Lambda function checks if a Glue job is running for the same file or not.

Define a state in the Step Functions workflow to invoke this Lambda function.
Use a Choice state to check the result of the Lambda invocation. If a Glue job is running, proceed to Step 4. If no Glue job is running, proceed to Step 5.
Step 4: Wait for the Glue job to complete.

Use a Wait state to wait for a specific period or until a Glue job completes.
After the wait period, transition to the next step.
Step 5: Start the Glue job.

Define a state in the Step Functions workflow to trigger the Glue job using the AWS Glue StartJobRun API.
Wait for the Glue job to complete by using the Wait state and providing a timeout if necessary.
If the Glue job completes successfully, proceed to Step 6. Otherwise, handle the failure condition (e.g., send an error notification, terminate the workflow, or retry the Glue job).
Step 6: Check the Glue job status.

Define a state in the Step Functions workflow to invoke a Lambda function that checks the status of the Glue job.
Use a Choice state to check the status. If the job is successful, proceed to Step 7. If it failed or has an error, handle the condition accordingly.
Step 7: Publish an SQS message.

Define a state in the Step Functions workflow to invoke a Lambda function that publishes an SQS message to the downstream system.
If the Lambda invocation is successful, the workflow is complete. Otherwise, handle the failure condition accordingly.
Step 8: Handle failure and update the workflow status in the database.

In case of any failure in the workflow (e.g., in Steps 2-7), define error handling paths to send alerts or notifications to users.
Update the database with the workflow status (success or failure) and any relevant details.


========== terraform===========

# Define the Step Functions state machine
resource "aws_sfn_state_machine" "example" {
    name     = "example-step-function"
role_arn = aws_iam_role.step_function_role.arn
definition = <<EOF
{
    "Comment": "Example Step Functions workflow",
    "StartAt": "CheckFiles",
    "States": {
        "CheckFiles": {
            "Comment": "Invoke Lambda function to check if required files are present",
            "Type": "Task",
            "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:checkFilesLambda",
            "End": true,
            "Retry": [
                {
                    "ErrorEquals": ["States.ALL"],
                    "IntervalSeconds": 5,
                    "MaxAttempts": 3,
                    "BackoffRate": 2
                }
            ]
        },
        "ChoiceState": {
            "Comment": "Evaluate the result of the check and decide next step",
            "Type": "Choice",
            "Choices": [
                {
                    "Variable": "$.checkFilesResult",
                    "BooleanEquals": true,
                    "Next": "CheckGlueJob"
                }
            ],
            "Default": "FailureState"
        },
        "CheckGlueJob": {
            "Comment": "Invoke Lambda function to check if Glue job is running",
            "Type": "Task",
            "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:checkGlueJobLambda",
            "End": true,
            "Retry": [
                {
                    "ErrorEquals": ["States.ALL"],
                    "IntervalSeconds": 5,
                    "MaxAttempts": 3,
                    "BackoffRate": 2
                }
            ]
        },
        "WaitForGlueJob": {
            "Comment": "Wait for a specified duration for Glue job to complete",
            "Type": "Wait",
            "Seconds": 60,
            "Next": "StartGlueJob"
        },
        "StartGlueJob": {
            "Comment": "Invoke Lambda function to start the Glue job",
            "Type": "Task",
            "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:startGlueJobLambda",
            "End": true,
            "Retry": [
                {
                    "ErrorEquals": ["States.ALL"],
                    "IntervalSeconds": 5,
                    "MaxAttempts": 3,
                    "BackoffRate": 2
                }
            ]
        },
        "CheckGlueJobStatus": {
            "Comment": "Invoke Lambda function to check the status of the Glue job",
            "Type": "Task",
            "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:checkGlueJobStatusLambda",
            "End": true,
            "Retry": [
                {
                    "ErrorEquals": ["States.ALL"],
                    "IntervalSeconds": 5,
                    "MaxAttempts": 3,
                    "BackoffRate": 2
                }
            ]
        },
        "PublishSQSMessage": {
            "Comment": "Invoke Lambda function to publish SQS message",
            "Type": "Task",
            "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:publishSQSLambda",
            "End": true,
            "Retry": [
                {
                    "ErrorEquals": ["States.ALL"],
                    "IntervalSeconds": 5,
                    "MaxAttempts": 3,
                    "BackoffRate": 2
                }
            ]
        },
        "FailureState": {
            "Comment": "Handle failure condition",
            "Type": "Fail",
            "Cause": "Workflow failed",
            "Error": "WorkflowError"
        }
    }
}
EOF
}

# IAM role for Step Functions
resource "aws_iam_role" "step_function_role" {
    name = "example-step-function-role"
assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "states.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}

# IAM policy for Step Functions role
resource "aws_iam_policy_attachment" "step_function_policy_attachment" {
    name       = "example-step-function-policy-attachment"
roles      = [aws_iam_role.step_function_role.name]
policy_arn = "arn:aws:iam::aws:policy/service-role/AWSStepFunctionsFullAccess"
}


