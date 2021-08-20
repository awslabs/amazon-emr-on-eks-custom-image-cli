#!/bin/sh
binary_zip_filename=$1
python_version=$3

if [ "$python_version" = "" ]; then
    python_version="3.7.9";
fi


set -eu


echo "Making Folders"
mkdir -p .build_mac/src
mkdir -p .build_mac/output/amazon-emr-on-eks-custom-image-cli-src
mkdir -p .build_mac/output/pyinstaller-output
cd .build_mac

echo "Copying Source"
cp -r ../[!.]* ./src
cd src
rm -rf scripts
rm -f Makefile
rm -rf venv
rm -rf __pycache__
cd ..
cp -r ./src/* ./output/amazon-emr-on-eks-custom-image-cli-src

echo "Installing Python3"
curl "https://www.python.org/ftp/python/${python_version}/Python-${python_version}.tgz" --output python.tgz
tar -xzf python.tgz
cd Python-$python_version
./configure --enable-shared
make -j8
make install
cd ..

echo "Installing Python Libraries"
python3 -m venv venv
./venv/bin/pip3 install --upgrade pip
./venv/bin/pip3 install -r src/requirements.txt

echo "Installing PyInstaller"
./venv/bin/pip3 install -r src/pyinstaller-build.txt

echo "Building Binary"
cd src
echo "custom-image-validation-tool.spec content is:"
cat installer/pyinstaller/custom-image-validation-tool.spec
../venv/bin/python3 -m PyInstaller -F --clean installer/pyinstaller/custom-image-validation-tool.spec

mkdir -p pyinstaller-output
mkdir -p pyinstaller-output/dist
mv dist/* pyinstaller-output/dist
cp installer/assets/* pyinstaller-output
chmod 755 pyinstaller-output/installation

echo "install script content is:"
cat pyinstaller-output/installation
echo "Copying Binary"
cd ..
cp -r src/pyinstaller-output/* output/pyinstaller-output

echo "Packaging Binary"
cd output
cd pyinstaller-output
cd dist
cd ..
zip -r ../"$binary_zip_filename" ./*
cd ..
zip -r "$binary_zip_filename" amazon-emr-on-eks-custom-image-cli-src
