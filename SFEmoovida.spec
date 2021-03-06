#
# spec file for package SFEmoovida
#
# includes modules: moovida
#
# Copyright (c) 2008, 2010, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner yippi 
#
# bugdb: https://bugs.launchpad.net/elisa
#
%include Solaris.inc

%use moovida = moovida.spec

%define default_python_version 2.6

Name:              SFEmoovida
IPS_package_name:  desktop/media-player/moovida
Meta(info.classification): %{classification_prefix}:Applications/Sound and Video
License:           GPL v3, MIT
Vendor:            Sun Microsystems, Inc.
Summary:           Media center written in Python
Version:           %{moovida.version}
SUNW_BaseDir:      %{_basedir}

BuildRoot:         %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:     SUNWdbus-python26
BuildRequires:     SUNWPython26-devel
BuildRequires:     SUNWPython26-extra
BuildRequires:     SUNWimagick
BuildRequires:     SUNWsqlite3
BuildRequires:     SUNWgnome-python26-extras
BuildRequires:     SFElibpigment-devel
BuildRequires:     SUNWpython26-simplejson
BuildRequires:     SUNWpython26-pyopenssl
BuildRequires:     SUNWpython26-setuptools
Requires:          SUNWgnome-media
Requires:          SUNWimagick
Requires:          SUNWPython26
Requires:          SUNWsqlite3
Requires:          SUNWPython26-extra
Requires:          SUNWdbus-python26
Requires:          SUNWgnome-python26-extras
Requires:          SUNWgst-python26
Requires:          SFElibpigment
Requires:          SFElibpigment-python26
Requires:          SUNWpython26-imaging
Requires:          SUNWpython26-pyopenssl
Requires:          SUNWpython26-setuptools
Requires:          SUNWpython26-twisted
Requires:          SUNWpython26-twisted-web2
Requires:          SUNWpython26-simplejson
Requires:          SUNWpython26-cssutils
Requires:          SUNWdesktop-cache

%description
Moovida is an open source cross-platform media center solution.
Moovida runs on top of the GStreamer multimedia framework and takes
full advantage of harware acceleration provided by modern graphic
cards by using OpenGL APIs. You can watch movies, listen to music 
and view pictures with Moovida.

%prep
rm -rf %name-%version
mkdir %name-%version
%moovida.prep -d %name-%version

%build
export PYTHONPATH=%{_builddir}/%name-%version/elisa-%{elisa.version}:$PYTHONPATH

%install
rm -rf $RPM_BUILD_ROOT

%moovida.install -d %name-%version
export PYTHONPATH=%{_builddir}/%name-%version/elisa-%{elisa.version}:$PYTHONPATH

mv $RPM_BUILD_ROOT%{_bindir}/elisa $RPM_BUILD_ROOT%{_bindir}/moovida
# move to verndor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{default_python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{default_python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{default_python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{default_python_version}/site-packages

# Do not ship mobile desktop file.
rm $RPM_BUILD_ROOT%{_datadir}/applications/moovida-mobile.desktop

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache

%postun
%restart_fmri desktop-mime-cache


%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{default_python_version}/vendor-packages/elisa
%{_libdir}/python%{default_python_version}/vendor-packages/elisa-*-py%{default_python_version}.egg-info
%{_libdir}/python%{default_python_version}/vendor-packages/elisa-*-py%{default_python_version}-nspkg.pth
%doc -d elisa-%{moovida.version} AUTHORS
%doc(bzip2) -d elisa-%{moovida.version} COPYING README
%doc(bzip2) -d elisa-%{moovida.version} LICENSE.GPL
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/*.service
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, other) %{_datadir}/icons
%{_datadir}/icons/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


%changelog
* Mon Oct 12 2009 - brian.cameron@sun.com
- Now use %{default_python_version}.
* Wed May 27 2009 - brian.cameron@sun.com
- Move elisa spec files to moovida spec files.
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Thu Mar 05 2009 - brian.cameron@sun.com
- Change SUNWdbus-bindings to SUNWdbus-python.
* Wed Mar 04 2009 - li.yuan@sun.com
- Change owner to liyuan and don't build this package on sparc.
* Fri Jan 23 2009 - brian.cameron@sun.com
- Remove call to gtk-update-icon-cache since elisa does not install icons to an
  icon theme directly, but just directly to /usr/share/icons.  Therefore, it
  is not necessary to update the cache.  This is only needed when installing
  themed icons.  Fixes bug #6796488.
* Wed Dec 03 2008 - jijun.yu@sun.com
- Change a Requires name.
* Mon Dec 01 2008 - takao.fujiwara@sun.com
- Add %elisa_plugins_bad.build
* Thu Nov 20 2008 Jerry Yu <jijun.yu@sun.com>
- Created spec.
