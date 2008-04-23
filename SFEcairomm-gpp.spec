#
# spec file for package SFEcairomm-gpp
#
# includes module(s): cairomm
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use cairomm = cairomm.spec

Name:                    SFEcairomm-gpp
Summary:                 cairomm - C++ API for the Cairo Graphics Library (g++-built)
Version:                 %{cairomm.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SFEsigcpp-gpp
BuildRequires: SFEsigcpp-gpp-devel
BuildRequires: SUNWsigcpp-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SUNWsigcpp-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%cairomm.prep -d %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags"
export CFLAGS="%optflags"
export PERL_PATH=/usr/perl5/bin/perl
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
%cairomm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%cairomm.install -d %name-%version
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

# delete files already included in SUNWcairomm-devel:
rm -r $RPM_BUILD_ROOT%{_datadir}
rm -r $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%dir %attr (0755, root, other) %{_cxx_libdir}/pkgconfig
%{_cxx_libdir}/pkgconfig/*

%changelog
* Mon Mar 03 2008 - damien.carbery@sun.com
- Use base spec version for package version.
* Tue Feb 19 2008 - ghee.teo@sun.com
- Updated after review.
* Fri Jan 08 2008 - ghee.teo@sun.com
- Modified SFEcairomm.spec to make SUNWcairomm.spec and cairomm.spec
* Mon Nov 12 2007 - daymobrew@users.sourceforge.net
- Bump to 1.4.6.
* Wed Sep 19 2007 - trisk@acm.jhu.edu
- Bump to 1.4.4
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 1.4.2
* Sun Feb 25 2007 - laca@sun.com
- create
