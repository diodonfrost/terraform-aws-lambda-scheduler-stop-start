package test

import (
	L "./lib"
	"fmt"
	"testing"
	"time"

	"github.com/gruntwork-io/terratest/modules/aws"
	"github.com/gruntwork-io/terratest/modules/random"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

// Test Terraform ec2 scheduler module
func TestTerraformAwsSpotScheduler(t *testing.T) {
	t.Parallel()

	// Pick aws region Ireland
	awsRegion := "eu-west-1"

	// Give this Spot Instance a unique ID for a name tag so we can distinguish it from any other EC2 Instance running
	terratestTag := fmt.Sprintf("terratest-tag-%s", random.UniqueId())

	terraformOptions := &terraform.Options{
		// The path to where our Terraform code is located
		TerraformDir: "../../examples/spot-schedule",

		// Variables to pass to our Terraform code using -var options
		Vars: map[string]interface{}{
			"random_tag": terratestTag,
		},

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

	// Get all ec2 spot IDs with the tag "topstop:true" and the state running
	filtersSpotToTerminateRunning := map[string][]string{
		"instance-state-name": {"running"},
		"tag:tostop":          {"true"},
		"tag:terratest_tag":   {terratestTag},
		"instance-lifecycle":  {"spot"},
	}
	SpotIDsToStopRunning := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersSpotToTerminateRunning)

	// Get all ec2 spot IDs with the tag "topstop:false" and the state running
	filtersSpotsNoTerminateRunning := map[string][]string{
		"instance-state-name": {"running"},
		"tag:tostop":          {"false"},
		"tag:terratest_tag":   {terratestTag},
		"instance-lifecycle":  {"spot"},
	}
	SpotIDsNoTerminateRunning := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersSpotsNoTerminateRunning)

	// Invoke lambda function to terminate all spot instances with the tag:value `tostop:true`
	L.RunAwslambda(awsRegion, lambdaStopName)

	// Wait for scheduler exectuion
	time.Sleep(160 * time.Second)

	// Get all spot instances IDs with the tag "topstop:true" and the state terminate
	filtersSpotToStopTerminate := map[string][]string{
		"instance-state-name": {"terminated"},
		"tag:tostop":          {"true"},
		"tag:terratest_tag":   {terratestTag},
		"instance-lifecycle":  {"spot"},
	}
	SpotIDsToStopTerminate := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersSpotToStopTerminate)

	// Get all ec2 instances IDs with the tag "topstop:false" and the state running
	filtersSpotNoStopTerminate := map[string][]string{
		"instance-state-name": {"running"},
		"tag:tostop":          {"false"},
		"tag:terratest_tag":   {terratestTag},
		"instance-lifecycle":  {"spot"},
	}
	SpotIDsNoTerminate := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersSpotNoStopTerminate)

	// Verify the instances trigger by scheduler terminate-spot with tag "topstop:true" should be terminated
	assert.Equal(t, SpotIDsToStopRunning, SpotIDsToStopTerminate)

	// Verify the instances trigger by scheduler terminate-spot with tag "topstop:false" should be running
	assert.Equal(t, SpotIDsNoTerminateRunning, SpotIDsNoTerminate)
}
