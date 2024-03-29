%define appname    makelib
%define installdir /usr/local/makelib

Summary: Framework to build RPM packages.
Name:    %{appname}
Epoch:   1
Version: 3.6
Release: 1%{?dist}.yourtag
License: GPLv2+
Group:   Applications/Utils
URL:     https://github.com/jorgemorgado/makelib-rpm

Source0: Makefile.rpm
Source1: makelib.cfg
Source2: makelib.sudo
Source3: index_repo
Source4: release_local
Source5: release_remote

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: openssh-clients
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
%{__install} -m644 -D %{SOURCE0} %{buildroot}%{installdir}/Makefile.rpm
%{__install} -m644 -D %{SOURCE1} %{buildroot}/etc/makelib.cfg
%{__install} -m440 -D %{SOURCE2} %{buildroot}/etc/sudoers.d/makelib
%{__install} -m755 -D %{SOURCE3} %{buildroot}%{installdir}/index_repo
%{__install} -m755 -D %{SOURCE4} %{buildroot}%{installdir}/release_local
%{__install} -m755 -D %{SOURCE5} %{buildroot}%{installdir}/release_remote

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/local/makelib/Makefile.rpm
/usr/local/makelib/release_remote
%config(noreplace) /etc/makelib.cfg

%files release
%defattr(-,root,root)
/usr/local/makelib/index_repo
/usr/local/makelib/release_local
%config(noreplace) /etc/makelib.cfg
%config(noreplace) /etc/sudoers.d/makelib

%changelog
* Wed Mar 2 2022 Jorge Morgado <jorge@morgado.ch> - 1:3.6-1
- Add multiple release stages: remote, local, index repo
- Add configuration file
- Add support for different repository names

* Mon Nov 27 2017 Fabien Hochstrasser - 1:3.4-1
- Release to the same platform as the one where this script is running
- Fix version parsing
- Add more dependencies

* Tue Mar 20 2012 Jorge Morgado <jorge@morgado.ch> - 1:2.0-1
- Implement 'release' target.
- Add sub-package makelib-release which includes only the release function.

* Tue Mar  6 2012 Jorge Morgado <jorge@morgado.ch> - 1:1.0-1
- Initial release.
