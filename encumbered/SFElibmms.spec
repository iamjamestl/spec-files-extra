#
# spec file for package SFElibmms
#
# includes module(s): libmms
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#

%include Solaris.inc

%use libmms = libmms.spec

Name:		SFElibmms
IPS_Package_Name:	library/video/libmms
Summary:	mms stream protocol library
Group:		System/Multimedia Libraries
License:	LGPLv2
SUNW_Copyright:	libmms.copyright
URL:		http://libmms.sourceforge.net/
Version:	%{libmms.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	SUNWgnome-base-libs
Requires:	SUNWlibm
BuildRequires:	SUNWgnome-base-libs-devel
Conflicts:	SUNWmmsu
BuildRequires:	SUNWgnome-common-devel

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}

%prep
rm -rf %name-%version
mkdir -p %name-%version
%libmms.prep -d %name-%version

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
%libmms.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%libmms.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Wed Jul 20 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Tue Sep 02 2008 - halton.huo@sun.com
- Initial version
