# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## [3.1.3] - 2021-02-28
### Bug Fixes

* **variable:** rename scheduler tag variable name ([a2e0e2a](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/a2e0e2a95af3ee36e160123fc1decf1f9b88830e))

## [3.1.2] - 2021-02-26
### Reverts

* Revert "refactor(tag): renames scheduler tag" ([3800d9f](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/3800d9fcecbd1e8b7babe0b15cf7d58e96094a5b))

## [3.1.1] - 2021-02-25
### Bug Fixes

* **log:** allow lambda scheduler to write log ([8461925](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/8461925dd1842ebbe643bf33fbc1ae00630b75ba)) issue #15 thanks to @viyullas


### Features

* **iam:** add aws tags on iam role resource ([cdf4737](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/cdf473740b6eaa605de2ee535951c48741a97bff))

## [3.1.0] - 2020-12-31
### Features
* **cloudwatch:** add aws tags on cloudwatch resources ([6a579e2](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/6a579e2c59d42ab0b69664f517847e45ec20120d))

## [3.0.1] - 2020-12-04
### Bug Fixes
* **lambda:** add git version in the filename used by lambda ([4aa887e](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/4aa887e3f0a377ebc116f0922a655a86c9229844))
* **lambda:** removing source_code_hash param ([c813a0f](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/c813a0f6c40547ee78e54264da09f04281047976))

### Chore
* **gitignore:** ignore dependency lockfile ([41ba586](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/41ba586b87a94fac424890dc9d64dc1fdf492976))

### Refactor
* **python:** add utf-8 header encoding ([4aa887e](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/4aa887e3f0a377ebc116f0922a655a86c9229844))
* **terraform:** apply terraform fmt ([a51e4d6](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/a51e4d6c3cb1c57c17bec28a76612e9df598e698))

### Tests
* **pytest:** set python_path directly in pytest.ini ([a2bceb3](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/a2bceb38ff2257622fd713a02e692719284226e6))
* **sanity:** stop sanity script when error is found ([a22e396](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/a22e39612af1fe2244ad3a72f04ded59c084d947))
* **pytest:** update python packages requirements ([c9904ca](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/c9904ca2a9cff1273d301a7287f380c15b2b6aa4))

### CI
* **travis-ci:** removing travis-ci pipeline ([68a2827](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/68a2827d534fc71966ba58f6867ec0824de1bc35))
* **tflint:** update terraform version ([60eaa5a](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/60eaa5aa8a0379172483043cb3d7c4280655485e))
* **linting:** sparse github-action steps ([33b746a](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/33b746a5af451faa0ee5df497150692d88e20882))

## [3.0.0] - 2020-10-01
### BREAKING

* **spot-scheduler:** removing spot scheduler ([e52fdbcf](https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/commit/e52fdbcf6bfebbc1634f3c1b0cd20dd1547e9491))

## [2.10.0] - 2020-09-30
### Feature
- Python/Terraform: use ResourceGroupsTaggingAPI to filter aws resources
- Terraform: Allow bool type with scheduler variables

### Refactor
- Python: move waiter in dedicated class
- Python: changes inheritance by composition in the autoscaling scheduler class

### Style
- Python : use absolute imports in Python

### Build
- Python: Freeze Python packages version

## [2.9.1] - 2020-09-04
### Fix
- Fix Terraform ouput lambda_iam_role_name

### Changed
- Format python code with black 20.8b1

## [2.9.0] - 2020-07-28
### Added
- Terraform variable "tags" for tag lambda function
- github-action workflow

### Changed
- Freeze pylint version

### Deleted
- removing kitchen-ci file

## [2.8.0] - 2020-04-15
### Added
- Improve instance scheduler unit tests
- Cloudwatch integration tests

### Changed
- Restrict iam log group policy
- Do not schedule asg instances with ec2 instance scheduler

## [2.7.0] - 2020-03-31
### Changed
- Schedule Cloudwatch alarms with aws tags

## [2.6.0] - 2020-03-30
### Added
- Disable or Enable Cloudwatch alarms attached on scheduled resources
- Python 3.8 support

### Changed
- Rename ec2 scheduler class

## [2.5.3] - 2020-02-28
### Changed
- Do not run ec2 waiter when no instances found

## [2.5.2] - 2020-02-24
### Changed
- Waiting for instances in running state before resuming autoscaling group

## [2.5.1] - 2020-02-24
### Added
- github ISSUE_TEMPLATE

### Changed
- Start asg instances before autoscaling group

## [2.5.0] - 2020-02-17
### Added
- kms support

## [2.4.0] - 2020-02-12
### Added
- Use Python type hint

### Changed
- Refactoring Python import
- Move Python aws exception in dedicated function
- Increase waiting time during end-to-end tests

## [2.3.0] - 2019-11-26
### Added
- Multi aws regions support
- Python integration tests

## [2.2.1] - 2019-11-14
### Changed
- Refactoring Python unit tests

## [2.2.0] - 2019-11-10
### Added
- Python test units
- Aws region specification

## [2.1.5] - 2019-10-17
### Changed
- Improve rds error catching

## [2.1.4] - 2019-10-16
### Changed
- Fix autoscaling scheduler when autoscaling list are empty

## [2.1.3] - 2019-10-13
### Changed
- Use new python class style
- Optimize integration tests

## [2.1.2] - 2019-10-06
### Changed
- Optimize python code with yield

## [2.1.1] - 2019-09-29
### Changed
- Use poo style on python code

## [2.1.0] - 2019-09-12
### Added
- Custom IAM role

## [2.0.0] - 2019-09-12
### Changed
- Terraform 0.12 support
- Refactoring list resources function

## [1.9.0] - 2019-08-09
### Added
- Force utf-8 encoding

### Changed
- Refactoring whole Python code
- Set Flake8 max-complexity to 10 instead of 20
- Change waiting delay in integration tests

## [1.8.0] - 2019-08-03
### Added
- Test Python code with Tox
- Test Python code with travis-ci
- Test Terraform code with terraform fmt command

### Changed
- Flake8 codestyle convention
- Black formating
- Pylint refactoring

## [1.7.2] - 2019-07-10
### Changed
- Don't shutdown all instances when no autoscaling group is found

## [1.7.1] - 2019-06-30
### Added
- Tests for spot instance scheduler
- Parallel testing with Terratest

### Changed
- Update test directory structure

## [1.7.0] - 2019-06-30
### Added
- Spot instance support
- Terratest tests for ec2 shceduler
- Terratest tests for autoscaling scheduler

### Changed
-  Update README.md

### Removed
- Remove Gemfile

## [1.6.1] - 2019-06-21
### Added
- Ouputs in Terraform examples

### Changed
- Lambda outputs name

## [1.6.0] - 2019-06-20
### Added
- Enable Lambda Cloudwatch logs

### Changed
- Improve Python exception handler
- Improve Terraform rds example
- Linting Python main.py

## [1.5.0] - 2019-05-31
### Changed
- Power-off instances instead of terminating with autoscaling scheduler
- Use aws region eu-west-1 with Terraform examples

## [1.4.3] - 2019-05-09
### Changed
- Update awspec tests
- Update version in Gemfile

## [v1.4.2] - 2019-05-04
### Added
- Use travis-ci pipeline

## [v1.4.1] - 2019-04-05
### Changed
- Add boto3 paginator for autoscaling and rds function
- Improve Terraform examples

## [v1.4.0] - 2019-04-02
### Added
- Add more aws examples

### Changed
- Split python code into multiple file
- Refactoring python code
- Fix autoscaling deletion

## [v1.3.0] - 2019-02-23
### Added
- Add python log output for every resources stop and start

### Changed
- Fix tag filter for instances start and stop

## [v1.2.2] - 2019-02-19
### Added
- Improve comments

### Changed
- Lint code

## [v1.2.1] - 2019-02-10
### Changed
- When autoscaling shceduler is set to stop, terminate all instances in it

## [v1.2.0] - 2019-02-09
### Added
- kitchen-ci with awspec test
- Test fixture example

## [v1.1.0] - 2019-02-07
### Added
- Autoscaling support with scheduler

## [v1.0.0] - 2019-02-05
### Added
- ec2 instances support with scheduler
- rds instances support with scheduler
- rds clusters support with scheduler

[Unreleased]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/3.1.3...HEAD
[3.1.3]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/3.1.2...3.1.3
[3.1.2]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/3.1.1...3.1.2
[3.1.1]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/3.1.0...3.1.1
[3.1.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/3.0.1...3.1.0
[3.0.1]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/3.0.0...3.0.1
[3.0.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.10.0...3.0.0
[2.10.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.9.1...2.10.0
[2.9.1]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.9.0...2.9.1
[2.9.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.8.0...2.9.0
[2.8.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.7.0...2.8.0
[2.7.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.6.0...2.7.0
[2.6.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.5.3...2.6.0
[2.5.3]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.5.2...2.5.3
[2.5.2]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.5.1...2.5.2
[2.5.1]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.5.0...2.5.1
[2.5.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.4.0...2.5.0
[2.4.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.3.0...2.4.0
[2.3.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.2.1...2.3.0
[2.2.1]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.2.0...2.2.1
[2.2.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.1.5...2.2.0
[2.1.5]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.1.4...2.1.5
[2.1.4]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.1.3...2.1.4
[2.1.3]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.1.2...2.1.3
[2.1.2]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.1.1...2.1.2
[2.1.1]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.1.0...2.1.1
[2.1.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/2.0.0...2.1.0
[2.0.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/1.9.0...2.0.0
[1.9.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/1.8.0...1.9.0
[1.8.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/1.7.2...1.8.0
[1.7.2]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/1.7.1...1.7.2
[1.7.1]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/1.7.0...1.7.1
[1.7.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/1.6.1...1.7.0
[1.6.1]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/1.6.0...1.6.1
[1.6.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/1.5.0...1.6.0
[1.5.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/1.4.3...1.5.0
[1.4.3]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/v1.4.2...1.4.3
[v1.4.2]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/v1.4.1...v1.4.2
[v1.4.1]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/v1.4.0...v1.4.1
[v1.4.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/v1.3.0...v1.4.0
[v1.3.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/v1.2.2...v1.3.0
[v1.2.2]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/v1.2.1...v1.2.2
[v1.2.1]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/v1.2.0...v1.2.1
[v1.2.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/v1.1.0...v1.2.0
[v1.1.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/compare/v1.0.0...v1.1.0
[v1.0.0]: https://github.com/diodonfrost/terraform-aws-lambda-scheduler-stop-start/releases/tag/v1.0.0
