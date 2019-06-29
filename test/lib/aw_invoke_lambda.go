package lib

import (
    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/lambda"

    "encoding/json"
    "fmt"
    "os"
)

type getItemsRequest struct {
    SortBy     string
    SortOrder  string
    ItemsToGet int
}

// Trigger specific aws lambda function
func RunAwslambda(awsRegion string, lambdaName string) {

    // Initialize connection to aws
    sess := session.Must(session.NewSessionWithOptions(session.Options{
        SharedConfigState: session.SharedConfigEnable,
    }))

    // Define aws region to use
    client := lambda.New(sess, &aws.Config{Region: aws.String(awsRegion)})

    // Configure lambda event
    request := getItemsRequest{"time", "descending", 10}
    payload, err := json.Marshal(request)
    if err != nil {
        fmt.Println("Error marshalling MyGetItemsFunction request")
        os.Exit(0)
    }

    // Run aws lambda function
    client.Invoke(&lambda.InvokeInput{FunctionName: aws.String(lambdaName), Payload: payload})
}
