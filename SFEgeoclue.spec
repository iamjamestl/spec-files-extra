#
# spec file for package SFEgeoclue
#
# includes module(s): geoclue
#
# bugdb: bugzilla.freedesktop.org
#

%include Solaris.inc
Name:                    SFEgeoclue
IPS_Package_Name:	system/library/geoclue
License:                 LGPL v2
Group:                   Libraries/Multimedia
Version:                 0.12.0
Summary:                 Geoinformation Server
Source:                  http://launchpad.net/geoclue/trunk/0.12/+download/geoclue-%{version}.tar.gz
Patch1:                  geoclue-01-Wall.diff
URL:                     http://www.freedesktop.org/wiki/Software/GeoClue
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:            %{_basedir}

%include default-depend.inc
Requires:                SUNWglib2
Requires:                SUNWdbus-glib
BuildRequires:           SUNWglib2-devel
BuildRequires:           SUNWdbus-glib-devel
# New gpsd unsupported
#BuildRequires:           SFEgpsd-devel
#Requires:                SFEgpsd
BuildRequires:           SUNWlxsl
BuildRequires:           SUNWgtk-doc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
%setup -q -n geoclue-%version
%patch1 -p1

%build
./configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir}	    \
	--bindir=%{_bindir}	    \
	--libexecdir=%{_libexecdir} \
	--mandir=%{_mandir}	    \
	--enable-gpsd=no	\
	--enable-gtk-doc
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/lib*.so*
%{_libexecdir}/geoclue-example
%{_libexecdir}/geoclue-geonames
%{_libexecdir}/geoclue-gsmloc
%{_libexecdir}/geoclue-hostip
%{_libexecdir}/geoclue-localnet
%{_libexecdir}/geoclue-manual
%{_libexecdir}/geoclue-master
%{_libexecdir}/geoclue-nominatim
%{_libexecdir}/geoclue-plazes
%{_libexecdir}/geoclue-skyhook
%{_libexecdir}/geoclue-yahoo
#%{_libexecdir}/geoclue-gpsd
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1/services/*
%{_datadir}/geoclue-providers

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%changelog
* Sun Apr 01 2012 - Pavel Heimlich
- fix source url
* Sat Oct 29 2011 - Milan Jurik
- disable gpsd because it does not support new version
* Fri Jan 07 2011 - Milan Jurik
- add missing deps
* Tue Apr 27 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 0.12.0.
* Sun Oct 11 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created with version 0.11.1.
