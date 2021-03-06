#
# spec file for package SFEpython26-abiword
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                    SFEpython26-abiword
Summary:                 Python abiword
Version:                 0.8.0
URL:                     http://www.abisource.com/
Source:                  http://www.abisource.com/downloads/pyabiword/0.8.0/pyabiword-%{version}.tar.gz
Patch1:                  pyabiword-01-makefile.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython26
Requires:                SFEabiword
BuildRequires:           SUNWPython26-devel
BuildRequires:           SFEabiword-devel

%include default-depend.inc

%define cc_is_gcc 1
%define python_version 2.6

%prep
%setup -q -n pyabiword-%{version}
%patch1 -p1

%build
export CC=gcc
export CXX=g++
export CFLAGS="$CFLAGS -I/usr/include/python%{python_version}"
export CXXFLAGS="%gcc_cxx_optflags -I/usr/include/python%{python_version}"
export LDFLAGS="%{_ldflags} -L%{_cxx_libdir} -R%{_cxx_libdir}"

export PYTHON=/usr/bin/python%{python_version}
export PYGTK_DEFSDIR="/usr/share/pygtk/2.0/defs"
aclocal $ACLOCAL_FLAGS
automake -a -c -f
./configure --prefix=%{_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/pygtk

%changelog
* Wed Mar 10 2010 - brian.cameron@sun.com
- We build abiword with gcc, also build the bindings with them.
* Tue Feb 03 2010 - brian.cameron@sun.com
- Created with version 0.8.0
