#
# spec file for package SFEseamonkey
#
# SFEseamonkey-2.2.en-US.opensolaris-x86_64.tar.bz2
#
# License: MPLv1.1 or GPLv2+ or LGPLv2+

%include Solaris.inc

Name:          SFEseamonkey
Summary:       Mozilla Seamonkey - All-in-one internet application suite
Url:           http://www.mozilla.org/projects/seamonkey
Version:       2.2
Source:        http://releases.mozilla.org/pub/mozilla.org/seamonkey/releases/%{version}/seamonkey-%{version}.source.tar.bz2
URL:           http://www.mozilla.org/projects/seamonkey/
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWzip
BuildRequires: SUNWgtar
Requires:      SUNWdtbas
Requires:      SUNWfreetype2
Requires:      SUNWfontconfig
Requires:      SUNWglib2
Requires:      SUNWgnome-component
Requires:      SUNWgnome-libs
Requires:      SUNWgnome-vfs
Requires:      SUNWgtk2
Requires:      SUNWlibC
Requires:      SUNWlibms
Requires:      SUNWlibmsr
Requires:      SUNWpango
Requires:      SUNWsqlite3
Requires:      SUNWxwplt
#Requires:      SFEhunspell

%description
Web-browser, advanced e-mail and newsgroup client, IRC chat client,
and HTML editing made simple -- all your Internet needs in one application.

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
%setup -q -n %name-%version -c
cd mozilla

%build
cd mozilla

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

export LDFLAGS="-z ignore -L%{_libdir} -L/usr/sfw/lib -R'\$\$ORIGIN:\$\$ORIGIN/..' -R%{_libdir}/mps -L/usr/X11/lib -L/usr/gnu/lib -R/usr/X11/lib -R/usr/gnu/lib"
export CFLAGS="-xlibmil -I/usr/X11/include -I/usr/gnu/include"
export CXXFLAGS="-norunpath -xlibmil -xlibmopt -features=tmplife -lCrun -lCstd"
%ifarch sparc
export CFLAGS="$CFLAGS -xO5"
export CXXFLAGS="$CXXFLAGS -xO5"
%else
export CFLAGS="$CFLAGS -xO3"
export CXXFLAGS="$CXXFLAGS -xO3"
%endif

cat << "EOF" > .mozconfig
MOZILLA_OFFICIAL=1
export MOZILLA_OFFICIAL

BUILD_OFFICIAL=1
export BUILD_OFFICIAL

ac_add_options --prefix=%{_prefix}
ac_add_options --libdir=%{_libdir}
ac_add_options --mandir=%{_mandir}
ac_add_options --enable-application=suite
ac_add_options --enable-optimize=-xO3
ac_add_options --enable-crypto
ac_add_options --enable-xinerama
ac_add_options --enable-image-decoders=all
ac_add_options --enable-extensions=all
ac_add_options --enable-x11-shm
ac_add_options --enable-ctl
ac_add_options --enable-default-toolkit=gtk2
ac_add_options --enable-ldap
ac_add_options --disable-tests
ac_add_options --disable-debug --disable-dtd-debug
ac_add_options --disable-auto-deps
ac_add_options --with-xprint
ac_add_options --enable-system-cairo
ac_add_options --disable-mochitest 
#ac_add_options --disable-crashreporter 
#ac_add_options --enable-ldap-experimental
#ac_add_options --enable-libxul 
#ac_add_options --with-system-nspr 
#ac_add_options --with-system-nss 
#ac_add_options --with-system-jpeg 
#ac_add_options --with-system-zlib 
#ac_add_options --with-system-png  
#ac_add_options --disable-installer 
#ac_add_options --enable-startup-notification 
#ac_add_options --enable-system-hunspell 
#ac_add_options --enable-libproxy 
#ac_add_options --enable-system-mozldap 
mk_add_options MOZ_CO_PROJECT=suite
mk_add_options BUILD_OFFICIAL=1
mk_add_options MOZILLA_OFFICIAL=1
#mk_add_options MOZ_MAKE_FLAGS=%{?jobs:-j%jobs}
#mk_add_options MOZ_OBJDIR=@TOPSRCDIR@/../obj
EOF

make -f client.mk build_all
cd xpinstall/packager
make

%install
/bin/rm -rf $RPM_BUILD_ROOT

cd mozilla
BUILD_OFFICIAL=1 MOZILLA_OFFICIAL=1 \
    DESTDIR=$RPM_BUILD_ROOT \
    make install

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT


%files 
%defattr(0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/seamonkey
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/seamonkey-%{version}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/seamonkey.1

%files devel
%defattr(0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/seamonkey-config
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/idl
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Jul 8 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 2.2
* Sat Jun 25 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 2.1
- Added SFEhunspell and additional config options 
* Thu Mar 18 2010 - matt@greenviolet.net
- bump to 1.1.19
- first attempt to fix dependencies
* Sat Jul 18 2009 - matt@greenviolet.net
- bump to 1.1.17
* Fri Dec 09 2008 - alfred.peng@sun.com
- bump to 1.1.14
* Thu Apr 18 2008 - evan.yan@sun.com
- bump to 1.1.9
* Thu Mar 6 2008 - alfred.peng@sun.com
- bump to 1.1.8
- add --enable-system-cairo to option to resolve the dependency of pango on cairo
- This could be removed when the seamonkey tree cairo is upgraded.
* Wed Oct 17 2007 - laca@sun.com
- bump to 1.1.4
- add /usr/gnu and /usr/X11 to search paths
* Sun Jan 21 2007 - laca@sun.com
- bump to 1.1; remove --enable-calendar option as it's not longer supported
* Wed Jan  3 2007 - laca@sun.com
- bump to 1.0.7
* Thu Aug 17 2006 - laca@sun.com
- created
