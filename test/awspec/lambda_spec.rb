# aws spec testing lambda functions

require 'awspec'
require 'aws-sdk'
require 'rhcl'

lambda_names = ['start-ec2',
               'stop-ec2']

# Lambda function should be created
lambda_names.each do |name|
  describe lambda(name) do
    it { should exist }
    its(:timeout) { should be >= 600 }
    its(:runtime) { should eq 'python3.7' }
  end
end
