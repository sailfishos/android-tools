#
# spec file for package android-tools
#
# Copyright (c) 2023 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# To submit bugfixes or comments please read:
# https://docs.sailfishos.org/Develop/Collaborate

# Obsolete old android-tools-hadk which provides:
# - fastboot
# bootimg:
# - split_bootimg
# - mkbootimg
%define obsole_android_tools_hadk_ver 5.1.1_r38 
%undefine __cmake_in_source_build

Name:           android-tools
Version:        35.0.1
Release:        0
Summary:        Android platform tools
License:        Apache-2.0 AND MIT
URL:            https://developer.android.com/studio/releases/platform-tools
Source0:        %{name}-%{version}.tar.xz
Patch0000:      0001-Allow-to-use-patch-instead-of-git-to-apply-patches.patch
Patch0001:      0002-Don-t-use-absolute-dir-for-mkbootimg-symlink.patch
Patch0002:      0003-Move-static-libraries-to-separate-cmakelists-files-a.patch
Patch0003:      0004-Disable-unwanted-programs.patch
Patch0004:      0005-Make-it-possible-to-disable-COMPLETIONS.patch
BuildRequires:  cmake >= 3.12
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(gtest)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libpcre2-8)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(protobuf-lite)
BuildRequires:  pkgconfig(libcrypto)
# NOTE: We don't need udev rules for permissions as we don't run udev inside sdk
# Requires:       android-udev-rules 
Suggests:       %{name}-mkbootimg = %{version}
Suggests:       %{name}-partition = %{version}
Provides:       android-tools-hadk
Obsoletes:      android-tools-hadk < %{obsole_android_tools_hadk_ver}

%description
Android SDK Platform-Tools is a component for the Android SDK.
It includes tools that interface with the Android platform.

%package mkbootimg
Summary:        Android boot.img manipulation tools
Requires:       %{name} = %{version}
Provides:       android-tools-hadk-bootimg <= %{obsole_android_tools_hadk_ver}
Obsoletes:      android-tools-hadk-bootimg < %{obsole_android_tools_hadk_ver}
BuildArch:      noarch

%description mkbootimg
This package contains the Android boot.img manipulation tools.

%package partition
Summary:        Android dynamic partition tools
Requires:       %{name} = %{version}

%description partition
This package contains the Android dynamic partition tools.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

# fix env-script-interpreter
sed -e '1s|^#!.*|#!/usr/bin/python3|' -i vendor/avb/avbtool.py \
vendor/mkbootimg/{mk,repack_,unpack_}bootimg.py \
vendor/mkbootimg/gki/generate_gki_certificate.py \
vendor/libufdt/utils/src/mkdtboimg.py

%build

%cmake \
-DBUILD_SHARED_LIBS=OFF		\
-DCOMPLETIONS=OFF \
%{nil}
%cmake_build

%install
%cmake_install

# fix non-executable-script
chmod 0755 %{buildroot}%{_datadir}/%{name}/mkbootimg/gki/generate_gki_certificate.py

%check
# call some tools to test python3 compatibility
export PATH=%{buildroot}%{_bindir}:$PATH
export PYTHONDONTWRITEBYTECODE=1
avbtool version
mkbootimg --help

%files
%license LICENSE
%doc README.md
%{_bindir}/append2simg
%{_bindir}/avbtool
%{_bindir}/e2fsdroid
%{_bindir}/ext2simg
%{_bindir}/fastboot
%{_bindir}/img2simg
%{_bindir}/make_f2fs
%{_bindir}/sload_f2fs
%{_bindir}/mke2fs.android
%{_bindir}/simg2img

%files mkbootimg
%license LICENSE
%{_bindir}/{mk,repack_,unpack_}bootimg
%{_bindir}/mkdtboimg
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/mkbootimg

%files partition
%license LICENSE
%doc vendor/extras/partition_tools/README.md
%{_bindir}/lp{add,dump,flash,make,unpack}
