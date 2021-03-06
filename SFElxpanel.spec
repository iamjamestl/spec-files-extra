#
# spec file for package SFElxpanel
#
# includes module(s): lxpanel
#
# https://sourceforge.net/tracker/index.php?func=detail&aid=$bugid&group_id=180858&atid=894869
#
%include Solaris.inc

Name:                    SFElxpanel
Summary:                 LXDE desktop panel
Version:                 0.5.6
Source:                  http://downloads.sourceforge.net/lxde/lxpanel-%{version}.tar.gz
URL:                     http://sourceforge.net/projects/lxde/
Requires: SFEmenu-cache
BuildRequires: SFEmenu-cache

# owner:alfred date:2009-03-16 type:bug
Patch1:                  lxpanel-01-solaris.diff
Patch2:                  lxpanel-02-ifhwaddr.diff
Patch3:                  lxpanel-03-batt.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n lxpanel-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CFLAGS="-DHAVE_SYS_SOCKIO_H"

libtoolize --force
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} --libdir=%{_libdir}
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

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
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}/lxpanel
%{_libdir}/lxpanel/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/lxpanel
%{_datadir}/lxpanel/*
%dir %attr (0755, root, bin) %{_datadir}/man
%{_datadir}/man/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Aug 03 2010 - brian.cameron@oracle.com
- Bump to 0.5.6.  Add lxpanel-03-batt.diff
* Fri Mar 05 2010 - brian.cameron@sun.com
- Bump to 0.5.5.
* Mon Feb 15 2010 - brian.cameron@sun.com
- Bump to 0.5.4.1
* Thu Aug 06 2009 - alfred.peng@sun.com
- Bump to 0.5.2.
* Tue Aug 04 2009 - brian.cameron@sun.com
- Bump to 0.5.1.
* Wed Jun 03 2009 - alfred.peng@sun.com
- Bump to 0.4.1. Remove the upstreamed patch crash.diff.
* Mon Mar 16 2009 - alfred.peng@sun.com
- Initial version with gcc.
