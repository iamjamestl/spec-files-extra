#
# spec file for package SFEopenbox
#
# includes module(s): openbox
#
# bugdb: http://bugzilla.icculus.org
#
%include Solaris.inc

Name:		SFEopenbox
IPS_Package_Name:	desktop/window-manager/openbox
Summary:	A free window manager for the X Window System
License:	GPLv2
SUNW_Copyright:	openbox.copyright
Version:	3.5.0
Source:		http://icculus.org/openbox/releases/openbox-%{version}.tar.gz
Patch1:		openbox-01-emptystruct.diff
URL:		http://icculus.org/openbox/index.php/Main_Page
Group:		Desktop (GNOME)/Window Managers
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SFEimlib2
Requires:	SFEimlib2

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n openbox-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export LDFLAGS="-lsocket"

autoconf
./configure --prefix=%{_prefix} --libdir=%{_libdir} --libexecdir=%{_libexecdir} --sysconfdir=%{_sysconfdir}
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT/%{_libdir}/*a

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*so*
%{_libdir}/openbox*autostart
#%dir %attr (0755, root, bin) %{_libdir}/openbox
#%{_libdir}/openbox/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_datadir}/xsessions
%{_datadir}/xsessions/*
%dir %attr (0755, root, bin) %{_datadir}/themes
%{_datadir}/themes/*
%dir %attr (0755, root, bin) %{_datadir}/man
%{_datadir}/man/*

%files root
%defattr (0755, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/xdg/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Oct 2 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 3.5.0
* Sun Jul 24 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Thu Jun 10 2010 - pradhap (at) gmail.com
- Bump to 3.4.11.2
* Mon Feb 15 2010 - brian.cameron@sun.com
- Bump to 3.4.11.
* Tue Aug 04 2009 - brian.cameron@sun.com
- Add patch openbox-02-session.diff so that the script works
  with Nevada bourne-shell.
* Tue Jun 02 2009 - alfred.peng@sun.com
- Add patch union.diff for anonymous union usage.
* Sun Mar 16 2009 - alfred.peng@sun.com
- Initial version
