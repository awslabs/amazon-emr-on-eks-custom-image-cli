# Amazon EMR on EKS Custom Image CLI Development Guide

This guide will help you set up your development environment for testing and contributing to custom image validation tool.
If you found something is missing or inaccurate, update this guide and send a Pull Request.

## Get Source Code

Pull source code from Github repository.

## Environment Set Up
### Prerequisite
Before running this tool, please make sure you have Docker CLI installed.

### Install Docker CLI (Optional).

This tool utilizes [Docker CLI](https://docs.docker.com/docker-for-mac/install/) to help validate custom images.
Please make sure you have Docker CLI installed prior to using the tool.

### Create Virtual Environment
To avoid messing up with global python environment, create a virtual environment for this tool
under current folder:

```python3 -m venv <venv>```

*Note: You can change the path for you virtual env to whatever you want, but be careful of the slight difference of
the path in Mac and Windows.*

To activate/deactivate virtual environment, run following command:

* For Mac/Unix Users, run ```source <venv>/bin/activate```

* For Windows Users, run ```C:\> <venv>\Scripts\activate.bat```

To deactivate the venv, type in the shell: ``` deactivate ```.

### Install Required Dependencies.

To ensure that all the required dependencies are successfully installed, run:
```
pip3 install -r requirements.txt
```

### Set Python Path

To avoid relative import error, set the Python path to current package folder:

```export PYTHONPATH=$PATHONPATH:`pwd` ``` in linux/macOS

or

```set PYTHONPATH=<path to source code>``` in windows

## Validate Custom Image
In the root directory, you can directly use python3 command to run the validation tool.

Then run command:

```
python3 custom_image_cli validate-image -i <image_name> -r <release_name> [-t <image_type>]
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

## Unit Test

To run unit tests for this tool, you can use command `python3 -m unittest discover`.
