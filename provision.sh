#!/bin/bash
set -eu

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

apt update
apt install -y nasm build-essential gdb

echo 'set disassembly-flavor intel' > ~/.gdbinit
