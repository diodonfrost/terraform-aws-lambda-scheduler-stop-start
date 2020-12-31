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
func TestTerraformAwsInstanceScheduler(t *testing.T) {
	t.Parallel()

	// Pick aws region Ireland
	awsRegion := "eu-west-1"

	// Give this Spot Instance a unique ID for a name tag so we can distinguish it from any other EC2 Instance running
	terratestTag := fmt.Sprintf("terratest-tag-%s", random.UniqueId())

	terraformOptions := &terraform.Options{
		// The path to where our Terraform code is located
		TerraformDir: "../../examples/instance-scheduler",

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
	lambdaStartName := terraform.Output(t, terraformOptions, "lambda_start_name")
	
	// Wait for terraform execution
	time.Sleep(10 * time.Second)

	// Get all ec2 instances IDs with the tag "topstop:true" and the state running
	filtersInstancesToStopRunning := map[string][]string{
		"instance-state-name": {"running"},
		"tag:tostop":          {"true"},
		"tag:terratest_tag":   {terratestTag},
	}
	InstancesIDsToStopRunning := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersInstancesToStopRunning)

	// Get all ec2 instances IDs with the tag "topstop:false" and the state running
	filtersInstancesNoStopRunning := map[string][]string{
		"instance-state-name": {"running"},
		"tag:tostop":          {"false"},
		"tag:terratest_tag":   {terratestTag},
	}
	InstancesIDsNoStopRunning := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersInstancesNoStopRunning)

	// Invoke lambda function to stop all instances with the tag:value `tostop:true`
	L.RunAwslambda(awsRegion, lambdaStopName)

	// Wait for scheduler exectuion
	time.Sleep(180 * time.Second)

	// Get all ec2 instances IDs with the tag "topstop:true" and the state stopped
	filtersInstancesToStopStopped := map[string][]string{
		"instance-state-name": {"stopped"},
		"tag:tostop":          {"true"},
		"tag:terratest_tag":   {terratestTag},
	}
	InstancesIDsToStopStopped := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersInstancesToStopStopped)

	// Get all ec2 instances IDs with the tag "topstop:false" and the state running
	filtersInstancesNoStopStopped := map[string][]string{
		"instance-state-name": {"running"},
		"tag:tostop":          {"false"},
		"tag:terratest_tag":   {terratestTag},
	}
	InstancesIDsNoStopStopped := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersInstancesNoStopStopped)

	// Verify the instances trigger by scheduler stop-ec2 with tag "topstop:true" should be stopped
	assert.Equal(t, InstancesIDsToStopRunning, InstancesIDsToStopStopped)

	// Verify the instances trigger by scheduler stop-ec2 with tag "topstop:false" should be running
	assert.Equal(t, InstancesIDsNoStopRunning, InstancesIDsNoStopStopped)

	// Invoke lambda function to start all instances with the tag:value `tostop:true`
	L.RunAwslambda(awsRegion, lambdaStartName)

	// Wait for scheduler exectuion
	time.Sleep(180 * time.Second)

	// Get all ec2 instances IDs with the tag "topstop:true" and the state running
	InstancesIDsToStopStarted := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersInstancesToStopRunning)

	// Get all ec2 instances IDs with the tag "topstop:false" and the state running
	InstancesIDsNoStopStarted := aws.GetEc2InstanceIdsByFilters(t, awsRegion, filtersInstancesNoStopRunning)

	// Verify the instances trigger by scheduler start-ec2 with tag "topstop:true" should be running
	assert.Equal(t, InstancesIDsToStopStopped, InstancesIDsToStopStarted)

	// Verify the instances trigger by scheduler start-ec2 with tag "topstop:false" should be running
	assert.Equal(t, InstancesIDsNoStopStopped, InstancesIDsNoStopStarted)
}
