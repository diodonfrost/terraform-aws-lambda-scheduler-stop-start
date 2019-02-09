# aws spec testing iam lambda sheduler

require 'awspec'
require 'aws-sdk'
require 'rhcl'

role_names = ['start-ec2-scheduler-lambda',
              'stop-ec2-scheduler-lambda']

role_names.each do |name|
  describe iam_role(name) do
   it { should exist }
   its('attached_policies.count') { should eq 3 }
  end
end
