#
# spec file for package SFEdsniff.spec
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define src_name dsniff
%define src_version 2.4b1

Summary:		Tools for network auditing and penetration testing
IPS_Package_Name:	diagnostic/dsniff
Name:			SFEdsniff
Version:		2.4.0.1
License:		GPL
Group:			Applications/Internet
URL:			http://www.monkey.org/~dugsong/dsniff/
Source:			%{url}/beta/%{src_name}-%{src_version}.tar.gz
Patch1:			dsniff-01-modernization.diff
SUNW_BaseDir:		%{_basedir}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root
%include default-depend.inc

Requires: SUNWlibnet
BuildRequires: SUNWlibnet
Requires: SUNWopenssl-libraries
BuildRequires: SUNWopenssl-include
Requires: SFEbdb
BuildRequires: SFEbdb
Requires: SFElibnids
BuildRequires: SFElibnids-devel

%description
dsniff is a collection of tools for network auditing and penetration testing.

%prep
%setup -q -n %{src_name}-2.4
%patch1 -p1

%build
export CC=/usr/sfw/bin/gcc
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/lib -R/lib -L/usr/gnu/lib -R/usr/gnu/lib"

./configure 			\
    --prefix=%{_prefix}		\
    --bindir=%{_bindir}		\
    --sbindir=%{_sbindir}	\
    --mandir=%{_mandir}		\
    --with-db=/usr/gnu

make

%install
rm -rf $RPM_BUILD_ROOT
make install install_prefix=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin, 0755)
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%_libdir/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1m
%_mandir/man1m/*

%changelog
* Wed May 12 2010 - Milan Jurik
- added SFElibnids to deps
* Thu Sep 17 2009 - Milan Jurik
- cleanup of linker problems
* Mon Sep 14 2009 - Milan Jurik
- Initial version
