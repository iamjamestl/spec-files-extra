#
# spec file for package boost
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jchoi42
#

%define        major      1
%define        minor      46
%define        patchlevel 1
%define        ver_boost  %{major}_%{minor}_%{patchlevel}

%{!?boost_with_mt: %define boost_with_mt 0}

Name:         boost
License:      Boost License Version
Group:        System/Libraries
Version:      %{major}.%{minor}.%{patchlevel}
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      boost - free peer-reviewed portable C++ source libraries
Source:       %{sf_download}/boost/boost_%{ver_boost}.tar.bz2
# date:2007-08-13 owner:trisk 
Patch1:       boost-01-studio.diff
# date:2007-08-13 owner:laca
Patch2:       boost-02-gcc34.diff
# date:2009-11-04 owner:sobi
Patch3:       boost-03-xmlparser.diff
Patch4:       boost-04-compiler.diff
Patch6:       boost-06-bjam-math.diff

URL:          http://www.boost.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{name}_%{major}_%{minor}_%{patchlevel}
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

BOOST_ROOT=`pwd`
%if %cc_is_gcc
export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags"
export LDFLAGS="%_ldflags"
%else
export CXXFLAGS="%cxx_optflags -library=stlport4 -staticlib=stlport4 -norunpath -features=tmplife -features=tmplrefstatic"
export LDFLAGS="%_ldflags -library=stlport4 -staticlib=stlport4"
%endif

# Do not build with ICU if building with GCC since ICU is built with SunStudio.
%if %cc_is_gcc
./bootstrap.sh --prefix=%{_prefix} --with-toolset=gcc --without-icu 
%else
./bootstrap.sh --prefix=%{_prefix} --with-toolset=sun --with-icu --without-libraries=graph
%endif

./bjam --v2 -d+2 -q -j$CPUS -sBUILD="release <threading>single/multi" \
  release stage

%install

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Mar 19 2011 - Milan Jurik
- bump to 1.46.1 but disable graph lib for Sun Studio build
* Thu Aug 26 2010 - Brian Cameron <brian.cameron@oracle.com
- Bump to 1.44.
* Wed Aug 04 2010 - Brian Cameron <brian.cameron@oracle.com>
- Bump to 1.43.
* Fri Mar 05 2010 - Brian Cameron <brian.cameron@sun.com>
- Bump to 1.42.
* Fri Jan 29 2010 - Brian Cameron <brian.cameron@sun.com>
- Add boost-with-mt option to build the mt version of the libraries.
  Do not build with ICU support if building the GCC version, otherwise the
  boost regex library is not usable.
* Wed Dec 02 2009 - Albert Lee <trisk@opensolaris.org>
- Add patch4 from upstream for #2602
- Update URL
* Mon Oct 12 2009 - jchoi42@pha.jhu.edu
- Bump to 1.40.0, updated boost-01-studio patch
- Initial base spec
