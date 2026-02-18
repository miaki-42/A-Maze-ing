#!/bin/bash

cd /tmp

apt download libxcb-keysyms1-dev libxcb-keysyms1
mkdir -p extracted_libs
dpkg -x libxcb-keysyms1-dev_*.deb ./extracted_libs && dpkg -x libxcb-keysyms1_*.deb ./extracted_libs
cp -r ./extracted_libs/usr/include/* $VIRTUAL_ENV/include/ && cp -P ./extracted_libs/usr/lib/x86_64-linux-gnu/libxcb-keysyms* $VIRTUAL_ENV/lib/

export C_INCLUDE_PATH="$VIRTUAL_ENV/include:$C_INCLUDE_PATH"
export LIBRARY_PATH="$VIRTUAL_ENV/lib:$LIBRARY_PATH"
export LD_LIBRARY_PATH="$VIRTUAL_ENV/lib:$LD_LIBRARY_PATH"
export PKG_CONFIG_PATH="$VIRTUAL_ENV/lib/pkgconfig:$PKG_CONFIG_PATH"

cd - && cd src/mlx_CLXV
./configure.sh CFLAGS="-I$VIRTUAL_ENV/include" LDFLAGS="-L$VIRTUAL_ENV/lib -Wl,-rpath,$VIRTUAL_ENV/lib"
cd ../..