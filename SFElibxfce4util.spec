#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_name libxfce4util
%define src_url http://archive.xfce.org/src/xfce/libxfce4util/4.8

Name:		SFElibxfce4util
IPS_Package_Name:	library/desktop/libxfceutil
Summary:	Utility library for the Xfce desktop environment
License:	LGPLv2+
SUNW_Copyright:	libxfce4util.copyright
Version:	4.8.2
URL:		http://www.xfce.org/
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Group:		Desktop (GNOME)/Libraries
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:  SUNWglib2
Requires:       SUNWglib2
BuildRequires:	SFExfce4-dev-tools
Requires:	SFExfce4-dev-tools
BuildRequires:	SUNWgtk-doc
BuildRequires:	SUNWgnome-xml-share

%package devel
Summary:	%{summary} - developer files
Group:		Development/Libraries
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	--sbindir=%{_sbindir}		\
	--libdir=%{_libdir}		\
	--datadir=%{_datadir}		\
	--mandir=%{_mandir}		\
	--sysconfdir=%{_sysconfdir} 	\
	--enable-gtk-doc		\
	--enable-debug=no		\
	--disable-static

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# delete libtool .la files
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

%if %build_l10n
%else
#REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_sbindir}
%{_libdir}/lib*.so*

%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Sep 25 2011 -Milan Jurik
- fix download URL
* Sat Sep 24 2011 - Ken Mays <kmays2000@gmail.com>
- Backed to 4.8.2
* Sat Jul 23 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Sun Mar 20 2011 - Milan Jurik
- bump to 4.8.1, move to SFE from osol xfce
* Wed Aug 19 2009 - sobotkap@gmail.com
- Added IPS meta-tags required by juicer.
* Sun Dec 21 2008 - sobotkap@gmail.com
- Clean svn build method as we don't build from svn anymore
- As version use main version of Xfce release (defined in prod.inc)
* Wed Apr 11 2007 - dougs@truemail.co.th
- Changed to multi-isa build method
* Tue Apr  3 2007 - laca@sun.com
- delete libtool .la files
* Thu Jan 25 2007 - dougs@truemail.co.th
- Initial version
