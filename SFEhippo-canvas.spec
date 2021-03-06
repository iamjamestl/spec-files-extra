#
# spec file for package SFEhippo-canvas
#
# includes module(s): hippo-canvas
#

%include Solaris.inc
Name:		SFEhippo-canvas
IPS_Package_Name:	library/desktop/hippo-canvas
Summary:	Hippo Canvas
URL:		http://live.gnome.org/HippoCanvas
Version:	0.3.0
License:	LGPL
Source:		http://ftp.gnome.org/pub/GNOME/sources/hippo-canvas/0.3/hippo-canvas-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Requires:	SUNWPython26
Requires:	SUNWlibcroco
Requires:	SUNWlibrsvg
Requires:	SUNWgtk2
Requires:	SUNWgnome-python26-libs
BuildRequires:	SUNWPython26-devel
BuildRequires:	SUNWlibcroco-devel
BuildRequires:	SUNWlibrsvg-devel
BuildRequires:	SUNWgtk2-devel
BuildRequires:	SUNWgnome-python26-libs-devel

%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: SFEhippo-canvas

%define python_version 2.6

%prep
%setup -q -n hippo-canvas-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export PYTHON=/usr/bin/python%{python_version}
./configure --prefix=%{_prefix}	\
	--disable-static

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT/%{_libdir} -type f -name "*.a" -exec rm -f {} ';'

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
%{_libdir}/lib*.so*
%{_libdir}/python%{python_version}/vendor-packages/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%changelog
* Fri Jan 07 2011 - Milan Jurik
- python 2.6 deps
* Tue Feb 02 2010 - brian.cameron@sun.com
- Created with version 0.3.0.
