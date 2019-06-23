package test

import (
  "time"
  L "./lib"
	"testing"

  "github.com/gruntwork-io/terratest/modules/aws"
	"github.com/gruntwork-io/terratest/modules/terraform"
  "github.com/stretchr/testify/assert"
)

// Test Terraform ec2 scheduler module
func TestTerraformAwsExample(t *testing.T) {
    t.Parallel()

    // Pick aws region Ireland
	  awsRegion := "eu-west-1"

	  terraformOptions := &terraform.Options{
		    // The path to where our Terraform code is located
		    TerraformDir: "../../examples/ec2-schedule",

		    // Environment variables to set when running Terraform
		    EnvVars: map[string]string{
			      "AWS_DEFAULT_REGION": awsRegion,
		    },
    }

    // At the end of the test, run `terraform destroy` to clean up any resources that were created
	  defer terraform.Destroy(t, terraformOptions)

	  // This will run `terraform init` and `terraform apply` and fail the test if there are any errors
	  terraform.InitAndApply(t, terraformOptions)

	  // Run `terraform output` to get the value of an output variables
	  lambdaStopName := terraform.Output(t, terraformOptions, "lambda_stop_name")
    lambdaStartName := terraform.Output(t, terraformOptions, "lambda_start_name")

    // Get all ec2 instances IDs with the tag "topstop" and the state running
    filtersInstancesTagRunning := map[string][]string{
        "instance-state-name": {"running"},
        "tag:tostop": {"true"},
    }
    InstancesIDsTagRunning := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersInstancesTagRunning)

    // Invoke lambda function to stop all instances with the tag:value `tostop:true`
    L.RunAwslambda(awsRegion, lambdaStopName)

    // Wait for scheduler exectuion
    time.Sleep(60 * time.Second)

    // Get all ec2 instances IDs with the tag "topstop" and the state stopped
    filtersInstancesTagStopped := map[string][]string{
		    "instance-state-name": {"stopped"},
        "tag:tostop": {"true"},
    }
    InstancesIDsStopped := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersInstancesTagStopped)

    // Instances trigger by scheduler stop-ec2 should be stopped
    assert.Equal(t, InstancesIDsTagRunning, InstancesIDsStopped)

    // Invoke lambda function to start all instances with the tag:value `tostop:true`
    L.RunAwslambda(awsRegion, lambdaStartName)

    // Wait for scheduler exectuion
    time.Sleep(60 * time.Second)

    // Get all ec2 instances IDs with the tag "topstop" and the state running
    InstancesIDsTagStarted := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersInstancesTagRunning)

    // Verify the instances trigger by scheduler start-ec2 should be running
    assert.Equal(t, InstancesIDsStopped, InstancesIDsTagStarted)
}
