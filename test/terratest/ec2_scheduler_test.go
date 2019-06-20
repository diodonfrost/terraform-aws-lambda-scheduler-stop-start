package test

import (
//	"fmt"
	"testing"

//  "github.com/aws/aws-sdk-go/aws"
//  "github.com/aws/aws-sdk-go/aws/session"
//  "github.com/aws/aws-sdk-go/service/lambda"

	"github.com/gruntwork-io/terratest/modules/aws"
//	"github.com/gruntwork-io/terratest/modules/random"
	"github.com/gruntwork-io/terratest/modules/terraform"
//	"github.com/stretchr/testify/assert"
)

// An example of how to test the Terraform module in examples/terraform-aws-example using Terratest.
func TestEc2Scheduler(t *testing.T) {
	t.Parallel()

	// Give this EC2 Instance a unique ID for a name tag so we can distinguish it from any other EC2 Instance running
	// in your AWS account
//	expectedName := fmt.Sprintf("terratest-aws-example-%s", random.UniqueId())

	// Pick a random AWS region to test in. This helps ensure your code works in all regions.
//	awsRegion := aws.GetRandomStableRegion(t, nil, nil)
  awsRegion := "eu-west-1"

	terraformOptions := &terraform.Options{
		// The path to where our Terraform code is located
		TerraformDir: "../../examples/ec2-schedule",

		// Variables to pass to our Terraform code using -var options
//		Vars: map[string]interface{}{
//			"instance_name": expectedName,
//		},

		// Environment variables to set when running Terraform
		EnvVars: map[string]string{
			"AWS_DEFAULT_REGION": awsRegion,
		},
	}

	// At the end of the test, run `terraform destroy` to clean up any resources that were created
	defer terraform.Destroy(t, terraformOptions)

	// This will run `terraform init` and `terraform apply` and fail the test if there are any errors
	terraform.InitAndApply(t, terraformOptions)

  // Get arn of the lambda start-scheduler
  lambdaARN := terraform.Output(t, terraformOptions, "scheduler_lambda_invoke_arn")

  // Tag lambda function
	aws.AddTagsToResource(t, awsRegion, lambdaARN, map[string]string{"testing": "testing-tag-value"})

  // Run lambda scheduler
//  sess := session.Must(session.NewSessionWithOptions(session.Options{
//    SharedConfigState: session.SharedConfigEnable,
//  }))
//  client := lambda.New(sess, &aws.Config{Region: awsRegion})
//  result, err := client.Invoke(&lambda.InvokeInput{FunctionName: lambdaName, Payload: payload})
//  if err != nil {
//      fmt.Println("Error calling MyGetItemsFunction")
//      os.Exit(0)
//  }
//
//	// Look up the tags for the given Instance ID
//	instanceTags := aws.GetTagsForEc2Instance(t, awsRegion, instanceID)
//
//	testingTag, containsTestingTag := instanceTags["testing"]
//	assert.True(t, containsTestingTag)
//	assert.Equal(t, "testing-tag-value", testingTag)
//
//	// Verify that our expected name tag is one of the tags
//	nameTag, containsNameTag := instanceTags["Name"]
//	assert.True(t, containsNameTag)
//	assert.Equal(t, expectedName, nameTag)
}
