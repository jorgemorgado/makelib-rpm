Summary: Framework to build RPM packages.
Name:    makelib
Epoch:   1
Version: 3.4
Release: 1%{?dist}.yourtag
License: GPLv2+
Group:   Applications/Utils
URL:     https://github.com/jorgemorgado/makelib-rpm

Source0: Makefile
Source1: release
Source2: makelib.sudo

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: coreutils, gcc, gcc-c++, m4, make, automake, rpm-build, grep, util-linux, sed

%package release
Summary: Release packages to a Yum repository.
Requires: sudo

%description
This software provides a framework to build RPM packages.

%description release
This package implements the release function for makelib 'release' target.

%prep
# noop

%build
# noop

%install
%{__rm} -rf %{buildroot}
%{__install} -m644 -D %{SOURCE0} %{buildroot}/usr/local/makelib/Makefile
%{__install} -m755 -D %{SOURCE1} %{buildroot}/usr/local/makelib/release
%{__install} -m440 -D %{SOURCE2} %{buildroot}/etc/sudoers.d/makelib

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/local/makelib
/usr/local/makelib/Makefile

%files release
%defattr(-,root,root)
/usr/local/makelib/release
/etc/sudoers.d/makelib

%changelog
* Mon Nov 27 2017 Fabien Hochstrasser - 1:3.4-1
- Release to the same platform as the one where this script is running
- Fix version parsing
- Add more dependencies

* Tue Mar 20 2012 Jorge Morgado <jorge@morgado.ch> - 1:2.0-1
- Implement 'release' target.
- Add sub-package makelib-release which includes only the release function.

* Tue Mar  6 2012 Jorge Morgado <jorge@morgado.ch> - 1:1.0-1
- Initial release.
