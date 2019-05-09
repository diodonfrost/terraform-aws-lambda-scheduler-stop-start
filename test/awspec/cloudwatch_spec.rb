# aws spec testing lambda event cloudwatch

require 'awspec'
require 'aws-sdk'
require 'rhcl'

cloudwatch_name = ['trigger-lambda-scheduler-start-aws',
                   'trigger-lambda-scheduler-stop-aws']

cloudwatch_name.each do |name|
  describe cloudwatch_event(name) do
    it { should exist }
    it { should be_enable }
  end
end
