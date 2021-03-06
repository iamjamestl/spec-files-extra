#
# spec file for package SFEdevice-manager
#
# includes module(s): device-manager
#

%include Solaris.inc
%define python_version 2.4

Name:         SFEdevice-manager
License:      Other
Group:        System/GUI
Version:      0.5.9
Summary:      Device-manager is a GUI interface provided by hal to display information about devices.
Source:       http://people.freedesktop.org/~david/dist/hal-%{version}.tar.gz
URL:          http://www.freedesktop.org/wiki/Software_2fhal
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SUNWPython
BuildRequires: SUNWhal
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-python-libs
Requires: SUNWPython
Requires: SUNWhal
Requires: SFEexpat

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n hal-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
./configure --prefix=%{_prefix} \
			--datadir=%{_datadir}

%install
rm -rf $RPM_BUILD_ROOT
cd tools/device-manager
make DESTDIR=$RPM_BUILD_ROOT install
%if %build_l10n
cd ../..
cd po
make DESTDIR=$RPM_BUILD_ROOT install
%endif
rm $RPM_BUILD_ROOT%{_datadir}/hal/device-manager/*.pyo

# Rename sl_SI dir to sl as sl_SI is a symlink to sl and causing installation
# problems as a dir.
%if %build_l10n
cd $RPM_BUILD_ROOT%{_datadir}/locale
mv sl_SI sl
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%{_bindir}/hal-device-manager
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/hal/device-manager/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/locale
%endif

%changelog
* Wed Jun 06 2007 - nonsea@users.sourceforge.net
- Bump to 0.5.9.
- Remove patch hal-01-configure.diff.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Fixed configure.in typo
- Fixed non l10n build
* Thu Mar 29 2007 - daymobrew@users.sourceforge.net
- Rename sl_SI dir to sl in %install as sl_SI is a symlink to sl and causing
  installation problems as a dir.
* Wed Jan  3 2007 - laca@sun.com
- fix %{_datadir} attributes
* Wed Dec 13 2006 - jedy.wang@sun.com
- L10n support added.
* Mon Dec 11 2006 - jedy.wang@sun.com
- Initial spec
