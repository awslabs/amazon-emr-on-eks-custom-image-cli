### Installation Guide

####Install on Linux and Mac

For Mac users, please unblock the exec file first before installation.

Use command: 
```
sudo xattr -d com.apple.quarantine dist/emr-on-eks-custom-image
```
to remove quarantine attribute from the file.

Or press ctrl + right click on the exec file to allow open it.

1. Install Amazon EMR on EKS Custom Image CLI
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

####Install on Windows

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