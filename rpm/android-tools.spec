Name:		android-tools
Version:	8.0.0
Release:	1%{?dist}
Summary:	Some tools from android

Group:		Tools
License:	Apache2, BSD, or MIT
URL:		https://android.googlesource.com/
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(openssl)

%description
android-tools

The upstream tarball is based of upstream Android git repo:
  git clone https://android.googlesource.com/platform/system/core

with unneeded files removed.

%prep
%setup -q

%build
cp Makefile core/libsparse
make %{?_smp_mflags} -C core/libsparse

%install
rm -rf $RPM_BUILD_ROOT
cd core/libsparse
%make_install

%files
%defattr(-,root,root,-)
%{_bindir}/*

