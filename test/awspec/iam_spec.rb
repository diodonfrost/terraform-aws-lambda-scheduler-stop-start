# aws spec testing iam lambda sheduler

require 'awspec'
require 'aws-sdk'
require 'rhcl'

role_names = ['start-aws-scheduler-lambda',
              'stop-aws-scheduler-lambda']

role_names.each do |name|
  describe iam_role(name) do
    it { should exist }
    it { should have_inline_policy }
  end
end
