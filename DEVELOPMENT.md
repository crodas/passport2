<!--
SPDX-FileCopyrightText: 2021 Foundation Devices, Inc. <hello@foundationdevices.com>

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Development

This document describes how to develop for Passport.  The instructions below describe how to setup the developent environment and build Passport on a system running **Ubuntu 20.04**.  This OS is used for official Passport builds, as well as in the Dockerfile descibed below which creates reproducible builds.

## Setup
In order to build the Passport firmware, you need to:

* Get the source code
* Install the dependencies
* Run the build or sign command

### Get the Source Code
The instructions below assume you are installing into your home folder at `~/passport2`.  You can choose
to install to a different folder, and just update command paths appropriately.

    cd ~/
    git clone git@github.com:Foundation-Devices/passport2.git

### Install Dependencies
Several tools are required for building Passport.

#### Cross-Compiler Toolchain
The cross compiler enables your PC to build code for the STM32H753 MCU used by Passport.  Use the following commands to install and build the cross compiler and MicroPython tools.

    sudo apt install gcc-arm-none-eabi
    cd ~/passport2
    make -C mpy-cross

#### Autotools
The makefiles used by MicroPython and Passport firmware use Autotools.  Install Autotools and related packages with the following command:

    sudo apt install autotools-dev automake libusb-1.0.0-dev libtool python3-virtualenv libsdl2-dev pkg-config curl

#### OpenOCD - On-Chip Debugger
OpenOCD is used to connect to the STLink V2 debug probe.  Note that this is only required for developers with a special Developer version of the Passport board.  If all you want to do is build the firmware and install it with a Developer Pubkey over microSD, then you do not need to install OpenOCD.

    cd ~/
    git clone https://github.com/ntfreak/openocd.git
    cd ~/openocd/
    ./bootstrap
    ./configure --enable-stlink
    make
    sudo make install


## Building Passport Firmware
Passport comes with a a set of `Justfile` command scripts.  Using these commands requires that you first install the `just` command runner by following the instructions here:

    https://github.com/casey/just#installation
    
Note that Python `Pillow` must be updated to `8.4.0` for all commands to work properly using the following command:

    pip install Pillow==8.4.0

To build firmware for Passport, you can run the `just` commands in `ports/stm32/Justfile`.  You'll typically want to be in the `ports/stm32` folder to run these commands.

To build and sign the firmware with a Developer Pubkey, use one of the following commands:

    just sign 2.0.4 color
    just sign 2.0.4 mono

If you just want to build without signing, use one of the following commands:

    just build color
    just build mono

There are other `just` command as well, but most are only useful to developers who have the Developer board with a connection to an STLink V2 debug probe.

#### Building the Simulator
First, make sure you are in the simulator folder:

    cd simulator

Then run one of the simulator `just` commands:

    just sim color
    just sim mono


#### Code Signing
In order to load the files onto the device, they need to first be signed either by two separate keys (for Foundation's official updates), or by a Developer Pubkey if you are signing your own custom builds.  Since you are probably not a developer at Foundation, we'll just describe the process for the Developer Pubkey below.

Foundation developed a tool called `cosign`, which we use internally to double-sign official firmware, and which you can use to sign with a Developer Pubkey.

First, you need to build the `cosign` tool and copy it somewhere in your `PATH`:

    sudo apt install libssl-dev
    cd ports/stm32/boards/Passport/tools/cosign
    make
    cp x86/release/cosign ~/.local/bin   # You can run `echo $PATH` to see the list of possible places you can put this file

Next you need to sign the firmware and give it a version number.  Once signed, `cosign` will output a filename of the format `v2.0.3-passport.bin`, but with the version number
replaced with whatever you specified.  Note that you need to tell `cosign` whether you are signing for a `mono` (Founder's Edition) Passport or a `color` (Batch 2 onward) Passport.

    cosign -f build-Passport/firmware-COLOR.bin -k mykeys/user-pub.pem -t color -v 2.0.3

or

    cosign -f build-Passport/firmware-MONO.bin -k mykeys/user-pub.pem -t mono -v 2.0.3

Note that the `Justfile` in `ports/stm32` contains a `just sign` command that you can use just by placing your private key in `~/bin/keys/user.pem`.  Alternatively, you can
customize the location by setting `cosign_keypath` at the top of the `Justfile`.

    just sign 2.0.3 color

You can also print the contents of the firmware header with the following command:

    cosign -f build-Passport/firmware-signed-signed.bin -p -t color

The signed firmware can be put onto a microSD card and installed on Passport.  You just need to upload the corresponding Developer Pubkey first.

***TBD: Insert link to article on installing Developer Pubkey***

#### Building the Bootloader
To build the bootloader for a reproducibility check, go to the repo root folder:

    cd ~/passport2

Then run one of the following commands to build the corresponding bootloader:

    just build color
    just build mono
