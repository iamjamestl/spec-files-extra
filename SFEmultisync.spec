#
# spec file for package SFEmultisync
#
# includes module(s): multisync-gui.spec
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# owner: JerryYu
#

%include Solaris.inc

%use msyncgui = multisync-gui.spec

Name:               SFEmultisync
Summary:            OpenSync - multisync - A data synchronization framework CLI/GUI
Version:            %{default_pkg_version}
SUNW_BaseDir:       %{_basedir}
BuildRoot:          %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgnome-base-libs
Requires: SUNWlxml
Requires: SUNWmlib
Requires: SUNWzlib
Requires: SFEswig
Requires: SFElibopensync


%prep
rm -rf %name-%version
mkdir -p %name-%version
%msyncgui.prep -d %name-%version


%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%optflags"
%if %option_with_fox
export CFLAGS="$CFLAGS -I/usr/X11/include"
export CXXFLAGS="$CXXFLAGS -I/usr/X11/include"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
%msyncgui.build -d %name-%version


%install
rm -rf $RPM_BUILD_ROOT
%msyncgui.install -d %name-%version


%clean
rm -rf $RPM_BUILD_ROOT


%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait


%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/multisync-gui
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/man1/*


%changelog
* Sat Nov 17 2007 - daymobrew@users.sourceforge.net
- Add further support for Indiana.
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Add support for Indiana.
* Tue Jun 05 2007 - jijun.yu@sun.com
- Split into SFEmultisync.spec and SFEmsynctool.spec
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires/BuildRequries after check-deps.pl run.
* Tue Nov 14 2006 - halton.huo@sun.com
- initial version created
