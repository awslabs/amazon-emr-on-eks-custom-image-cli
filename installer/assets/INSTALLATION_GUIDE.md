### Installation Guide

#### Install on Linux and Mac

1. Use Homebrew for Mac/Linux users:
```
brew tap aws/tap
brew install emr-on-eks-custom-image
```
For Linux users, another option is to install using installation script:

Download the latest [Linux Release](https://github.com/awslabs/amazon-emr-on-eks-custom-image-cli/releases/download/v1.00/amazon-emr-on-eks-custom-image-cli-linux-v1.00.zip)

```
sudo ./installation
```
2. Run the tool
```
emr-on-eks-custom-image --version
```

Once succeeded, you will see the output message:
```
Amazon EMR on EKS Custom Image CLI 
Version: X.XX
```

To Uninstall, follow:

For Homebrew, run
```
brew uninstall emr-on-eks-custom-image
```

For installation script

1. Find the symlink using which
```
which emr-on-eks-custom-image
```
The output should be where the binary located: `/usr/local/bin/emr-on-eks-custom-image`

2. Find the directory the symlink points to
```
ls -l /usr/local/bin/emr-on-eks-custom-image
```
The output should be the installation directory: `/usr/local/amazon-emr-on-eks-custom-image-cli`

3. Delete the symlink and installation directory
```
sudo rm /usr/local/bin/emr-on-eks-custom-image
sudo rm -rf /usr/local/amazon-emr-on-eks-custom-image-cli
```

#### Install on Windows

Download the latest [Windows Release](https://github.com/awslabs/amazon-emr-on-eks-custom-image-cli/releases/download/v1.00/amazon-emr-on-eks-custom-image-cli-windows-v1.00.msi)

1. Install Amazon EMR on EKS Custom Image CLI using MSI Installer.
2. Run the tool
```
emr-on-eks-custom-image --version
```

Once succeeded, you will see the output message:
```
Amazon EMR on EKS Custom Image CLI 
Version: X.XX
```

To Uninstall, follow:

1. From the Start menu, search for "Add or remove programs".

2. Select the entry named Amazon EMR on EKS Custom Image CLI and choose Uninstall to launch the uninstaller.
