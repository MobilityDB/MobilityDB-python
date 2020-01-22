#!/bin/bash

if [ "$#" != "1" ]; then 
	echo "Usage: $0 <install-path>"
	exit 1
fi

installpath=$1

cd `dirname $0`

mkdir -p $installpath

make html latexpdf epub
cp -vr build/html/* $installpath/
cp -v build/latex/*.pdf $installpath/
cp -v build/epub/*.epub $installpath/

