# Amazon EMR on EKS Custom Image CLI
## Introduction
[Amazon EMR](https://aws.amazon.com/emr/) on [Amazon EKS](https://aws.amazon.com/eks/) provides support for
Custom Images, a capability that enables you to customize the Docker container images used for running
Apache Spark applications on [Amazon EMR on EKS](https://aws.amazon.com/emr/features/eks/).
Custom images enables you to install and configure packages specific to your workload that are not available
in the public distribution of EMR’s Spark runtime into a single immutable container. An immutable container
promotes portability and simplifies dependency management for each workload and enables you to integrate
developing applications for EMR on EKS with your own continuous integration (CI) pipeline.

To test the compatibility of the modifications made to your EMR base image, we are providing a utility to validate 
the image’s file structure. The utility will examine basic required arguments and ensure that the modifications work as 
expected and prevent job failures due to common misconfigurations. This tool can be integrated into your Continuous 
Integration (CI) pipeline when you are building your image. For more information about customizing the EMR on EKS base 
image, see our [documentation](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/docker-custom-images.html).


## For Developers
Developers who wish to develop on or contribute to the source code, please refer to [Contribution Guide](CONTRIBUTING.md) and [Development Guide](DEVELOPMENT_GUIDE.md).

## Getting Started

### Prerequisite
Before running this tool, please make sure you have Docker CLI installed.

#### Install Docker CLI (Optional).

This tool utilizes [Docker CLI](https://docs.docker.com/get-docker/) to help validate custom images.
Please make sure you have Docker CLI installed prior to using the tool.

### Installation

Please follow the Installation Guide [here](installer/assets/INSTALLATION_GUIDE.md).

### Usage

#### Validate Custom Image

Use command:
```
emr-on-eks-custom-image validate-image -i <image_name> -r <release_name> [-t <image_type>]
```

-i specifies the local image URI that needs to be validated, this can be the image URI or any name/tag you defined for your image.

-r specifies the exact release version of the EMR base image used to generate the customized image. For example, if the custom image was developed using EMR base image with release version 5.32.0, then the parameter should specify emr-5.32.0.

-t specifies the image type. If this is a spark image, just input spark. The default value is `spark` and the current version only supports spark runtime images.

After successfully running the tool, the log info will show test results. If the image doesn't meet necessary configuration requirements, you will see error messages that inform the missing part.

#### Basic Test

The [basic test](custom_image_cli/validation_tool/validation_tests/check_manifest.py) ensures the image contains expected configuration. The following parameters are verified in this test:

* `UserName`
* `WorkingDir`
* `EntryPoint`

#### Environment Test

The [environment test](custom_image_cli/validation_tool/validation_tests/check_envs.py) ensures the required environment variables are set to the expected paths.

Examples:
* `SPARK_HOME=/usr/lib/spark`
* `JAVA_HOME=/etc/alternatives/jre`

#### File Structure Test

The [file structure test](custom_image_cli/validation_tool/validation_tests/check_files.py) ensures the required files exist in expected locations. For different
types of images, the required dependencies are different. You should make sure those files are in the correct
location.

#### Local Job Run Test

The [local job run test](custom_image_cli/validation_tool/validation_tests/check_local_job_run.py) ensures that the custom image is valid and can pass basic job run. We will run a sample local spark job with following configuration:

```
docker run -it --rm <image-uri> spark-submit 
--deploy-mode client 
--master local 
--class org.apache.spark.examples.SparkPi local:///usr/lib/spark/examples/jars/spark-examples.jar
```

### Output Results
Examples:
```
Amazon EMR on EKS Custom Image CLI
Version: x.xx
... Checking if docker cli is installed
... Checking Image Manifest
[INFO] Image ID: c0749c685b2a3cf50ff18c41510324585748a225bc4804a46d96a947db03a53e
[INFO] Created On: 2021-05-17T20:50:07.986662904Z
[INFO] Default User Set to hadoop:hadoop : PASS
[INFO] Working Directory Set to /home/hadoop : PASS
[INFO] Entrypoint Set to /usr/bin/entrypoint.sh : PASS
[INFO] SPARK_HOME is set with value: /usr/lib/spark : PASS
[INFO] JAVA_HOME is set with value: /etc/alternatives/jre : PASS
[INFO] File Structure Test for spark-jars in /usr/lib/spark/jars: PASS
[INFO] File Structure Test for hadoop-files in /usr/lib/hadoop: PASS
[INFO] File Structure Test for hadoop-jars in /usr/lib/hadoop/lib: PASS
[INFO] File Structure Test for bin-files in /usr/bin: PASS
... Start Running Sample Spark Job
[INFO] Sample Spark Job Test with local:///usr/lib/spark/examples/jars/spark-examples.jar : PASS
-----------------------------------------------------------------
Overall Custom Image Validation Succeeded.
-----------------------------------------------------------------
```

Error Message:

```
Amazon EMR on EKS Custom Image CLI
Version: x.xx
... Checking if docker cli is installed
... Checking Image Manifest
[INFO] Image ID: xxxx
[INFO] Created On: 2021-04-20T22:12:05.523378Z
[INFO] Default User Set to hadoop:hadoop : PASS
[INFO] Working Directory Set to /home/hadoop : PASS
[INFO] Entrypoint Set to /usr/bin/entrypoint.sh : PASS
[INFO] SPARK_HOME is set with value: /usr/lib/spark : PASS
[INFO] JAVA_HOME is set with value: /etc/alternatives/jre : PASS
[ERROR] mockito-all MUST be in /usr/lib/hadoop/lib : FAIL
[ERROR] servlet-api MUST be in /usr/lib/hadoop/lib : FAIL
[ERROR] spotbugs-annotations MUST be in /usr/lib/hadoop/lib : FAIL
[ERROR] stax-api MUST be in /usr/lib/hadoop/lib : FAIL
[ERROR] xmlenc MUST be in /usr/lib/hadoop/lib : FAIL
[INFO] File structure test for bin-files in /usr/bin: PASS
... Start Running Sample Spark Job
[ERROR] Sample Spark Job Test with local:///usr/lib/spark/examples/jars/spark-examples.jar : FAIL
-----------------------------------------------------------------
Custom Image Validation Failed. Please see individual test results above for detailed information.
-----------------------------------------------------------------
```

## Support

This tool supports the following releases:
Supported Versions in Repo:

|          Releases          | Amazon EMR on EKS release versions | Container image tags |
|:--------------------------:|:----------------------------------:|:--------------------:|
| Amazon EMR 6.15.0 releases |         emr-6.15.0-latest          |  emr-6.15.0:latest   |
| Amazon EMR 6.14.0 releases |         emr-6.14.0-latest          |  emr-6.14.0:latest   |
| Amazon EMR 6.13.0 releases |         emr-6.13.0-latest          |  emr-6.13.0:latest   |
| Amazon EMR 6.12.0 releases |         emr-6.12.0-latest          |  emr-6.12.0:latest   |
| Amazon EMR 6.11.0 releases |         emr-6.11.0-latest          |  emr-6.11.0:latest   |
| Amazon EMR 6.10.0 releases |         emr-6.10.0-latest          |  emr-6.10.0:latest   |
| Amazon EMR 6.9.0 releases  |          emr-6.9.0-latest          |   emr-6.9.0:latest   |
| Amazon EMR 6.8.0 releases  |          emr-6.8.0-latest          |   emr-6.8.0:latest   |
| Amazon EMR 6.7.0 releases  |          emr-6.7.0-latest          |   emr-6.7.0:latest   |
| Amazon EMR 6.6.0 releases  |          emr-6.6.0-latest          |   emr-6.6.0:latest   |
|                            |         emr-6.6.0-20220411         |  emr-6.6.0:20220411  |
| Amazon EMR 6.5.0 releases  |          emr-6.5.0-latest          |   emr-6.5.0:latest   |
|                            |         emr-6.5.0-20211119         |  emr-6.5.0:20211119  |
| Amazon EMR 6.4.0 releases  |          emr-6.4.0-latest          |   emr-6.4.0:latest   |
|                            |         emr-6.4.0-20210830         |  emr-6.4.0:20210830  |
| Amazon EMR 6.3.0 releases  |          emr-6.3.0-latest          |   emr-6.3.0:latest   |
|                            |         emr-6.3.0-20210429         |  emr-6.3.0:20210429  |
| Amazon EMR 6.2.0 releases  |          emr-6.2.0-latest          |  emr-6.2.0-20210129  |
|                            |         emr-6.2.0-20210129         |  emr-6.2.0-20210129  |
|                            |         emr-6.2.0-20201218         |  emr-6.2.0-20201218  |
|                            |         emr-6.2.0-20201201         |  emr-6.2.0-20201201  |
| Amazon EMR 5.35.0 releases |         emr-5.35.0-latest          |  emr-5.35.0:latest   |
|                            |        emr-5.35.0-20220307         | emr-5.35.0:20220307  |
| Amazon EMR 5.34.0 releases |         emr-5.34.0-latest          |  emr-5.34.0:latest   |
|                            |        emr-5.34.0-20211208         | emr-5.34.0:20211208  |
| Amazon EMR 5.33.0 releases |         emr-5.33.0-latest          | emr-5.33.0-20210323  |
|                            |        emr-5.33.0-20210323         | emr-5.33.0-20210323  |
| Amazon EMR 5.32.0 releases |         emr-5.32.0-latest          | emr-5.32.0-20210129  |
|                            |        emr-5.32.0-20210129         | emr-5.32.0-20210129  |
|                            |        emr-5.32.0-20201218         | emr-5.32.0-20201218  |
|                            |        emr-5.32.0-20201201         | emr-5.32.0-20201201  |

Supported Versions in [Releases](https://github.com/awslabs/amazon-emr-on-eks-custom-image-cli/releases) for Mac/Linux/Windows:

|          Releases          | Amazon EMR on EKS release versions | Container image tags |
|:--------------------------:|:----------------------------------:|:--------------------:|
| Amazon EMR 6.15.0 releases |         emr-6.15.0-latest          |  emr-6.15.0:latest   |
| Amazon EMR 6.14.0 releases |         emr-6.14.0-latest          |  emr-6.14.0:latest   |
| Amazon EMR 6.13.0 releases |         emr-6.13.0-latest          |  emr-6.13.0:latest   |
| Amazon EMR 6.12.0 releases |         emr-6.12.0-latest          |  emr-6.12.0:latest   |
| Amazon EMR 6.11.0 releases |         emr-6.11.0-latest          |  emr-6.11.0:latest   |
| Amazon EMR 6.10.0 releases |         emr-6.10.0-latest          |  emr-6.10.0:latest   |
| Amazon EMR 6.9.0 releases  |          emr-6.9.0-latest          |   emr-6.9.0:latest   |
| Amazon EMR 6.8.0 releases  |          emr-6.8.0-latest          |   emr-6.8.0:latest   |
| Amazon EMR 6.7.0 releases  |          emr-6.7.0-latest          |   emr-6.7.0:latest   |
| Amazon EMR 6.6.0 releases  |          emr-6.6.0-latest          |   emr-6.6.0:latest   |
|                            |         emr-6.6.0-20220411         |  emr-6.6.0:20220411  |
| Amazon EMR 6.5.0 releases  |          emr-6.5.0-latest          |   emr-6.5.0:latest   |
|                            |         emr-6.5.0-20211119         |  emr-6.5.0:20211119  |
| Amazon EMR 6.4.0 releases  |          emr-6.4.0-latest          |   emr-6.4.0:latest   |
|                            |         emr-6.4.0-20210830         |  emr-6.4.0:20210830  |
| Amazon EMR 6.3.0 releases  |          emr-6.3.0-latest          |   emr-6.3.0:latest   |
|                            |         emr-6.3.0-20210429         |  emr-6.3.0:20210429  |
| Amazon EMR 6.2.0 releases  |          emr-6.2.0-latest          |  emr-6.2.0-20210129  |
|                            |         emr-6.2.0-20210129         |  emr-6.2.0-20210129  |
|                            |         emr-6.2.0-20201218         |  emr-6.2.0-20201218  |
|                            |         emr-6.2.0-20201201         |  emr-6.2.0-20201201  |
| Amazon EMR 5.35.0 releases |         emr-5.35.0-latest          |  emr-5.35.0:latest   |
|                            |        emr-5.35.0-20220307         | emr-5.35.0:20220307  |
| Amazon EMR 5.34.0 releases |         emr-5.34.0-latest          |  emr-5.34.0:latest   |
|                            |        emr-5.34.0-20211208         | emr-5.34.0:20211208  |
| Amazon EMR 5.33.0 releases |         emr-5.33.0-latest          | emr-5.33.0-20210323  |
|                            |        emr-5.33.0-20210323         | emr-5.33.0-20210323  |
| Amazon EMR 5.32.0 releases |         emr-5.32.0-latest          | emr-5.32.0-20210129  |
|                            |        emr-5.32.0-20210129         | emr-5.32.0-20210129  |
|                            |        emr-5.32.0-20201218         | emr-5.32.0-20201218  |
|                            |        emr-5.32.0-20201201         | emr-5.32.0-20201201  |

You can find more release information [Here](https://docs.aws.amazon.com/emr/latest/EMR-on-EKS-DevelopmentGuide/docker-custom-images-tag.html).

## Security

If you discover a potential security issue in this project, or think you may have discovered a security issue, we request you to notify AWS Security via our vulnerability [reporting page](http://aws.amazon.com/security/vulnerability-reporting/). Please do not create a public GitHub issue.

