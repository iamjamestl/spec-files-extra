#
# spec file for package SFEemacs-xft
#
# includes module(s): Xft GNU emacs 
#
%include Solaris.inc

Name:                    SFEemacs-xft
Summary:                 GNU Emacs text editor with experimental Xft support
Version:                 23.0.2008.01.01
%define emacs_version    23.0.60
Source:                  http://pkgbuild.sf.net/spec-files-extra/tarballs/emacs-xft-%{version}.tar.bz2
Patch1:                  emacs-xft-01-fonts.diff
URL:                     http://www.emacswiki.org/cgi-bin/wiki/XftGnuEmacs
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %option_with_fox
Requires: FSWxorg-clientlibs
Requires: FSWxwrtl
BuildRequires: FSWxorg-headers
%else
Requires: SUNWxwrtl
Requires: SUNWxwplt
Requires: SUNWxwice
%endif
Requires: SUNWTiff
Requires: SUNWpng
Requires: SUNWjpg
Requires: SUNWlibms
Requires: SUNWzlib
Requires: SUNWperl584core
Requires: SUNWtexi
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%prep
%setup -q -c -n SFEemacs-xft-%version
cd emacs
%patch1 -p1

%build
cd emacs

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CPP="/usr/sfw/bin/gcc -E"
export CC=/usr/sfw/bin/gcc
export CFLAGS="-O4"
%if %option_with_fox
export CFLAGS="$CFLAGS -I/usr/X11/include"
%endif
export LDFLAGS="-Xlinker -zignore -lX11 -L/usr/sfw/lib -R/usr/sfw/lib -lfreetype"
export PERL=/usr/perl5/bin/perl

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --infodir=%{_infodir}            \
            --sysconfdir=%{_sysconfdir}      \
            --localstatedir=%{_localstatedir} \
            --with-gif=no \
            --with-gtk --enable-font-backend --with-xft --with-freetype

make clean
make bootstrap
make

%install
cd emacs

rm -rf $RPM_BUILD_ROOT
make install prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	libexecdir=$RPM_BUILD_ROOT%{_libexecdir} \
        infodir=$RPM_BUILD_ROOT%{_infodir} \
        localstatedir=$RPM_BUILD_ROOT%{_localstatedir}

rm $RPM_BUILD_ROOT%{_bindir}/ctags
rm $RPM_BUILD_ROOT%{_bindir}/etags
rm $RPM_BUILD_ROOT%{_bindir}/b2m
rm $RPM_BUILD_ROOT%{_bindir}/ebrowse
rm $RPM_BUILD_ROOT%{_bindir}/emacs
rm $RPM_BUILD_ROOT%{_bindir}/emacsclient
rm $RPM_BUILD_ROOT%{_bindir}/grep-changelog
rm $RPM_BUILD_ROOT%{_bindir}/rcs-checkin
mv $RPM_BUILD_ROOT%{_bindir}/emacs-%{emacs_version} $RPM_BUILD_ROOT%{_bindir}/emacs-xft-%{emacs_version}
rm $RPM_BUILD_ROOT%{_mandir}/man1/ctags.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/etags.1
rm $RPM_BUILD_ROOT%{_mandir}/man1/emacsclient.1
mv $RPM_BUILD_ROOT%{_mandir}/man1/emacs.1 $RPM_BUILD_ROOT%{_mandir}/man1/emacs-xft
rm -r $RPM_BUILD_ROOT%{_infodir}
rm $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp/*

rm -r $RPM_BUILD_ROOT%{_localstatedir}

echo '#!/bin/bash'                      > $RPM_BUILD_ROOT%{_bindir}/emacs-xft
echo 'mydir=$(cd $(dirname $0); pwd);' >> $RPM_BUILD_ROOT%{_bindir}/emacs-xft
echo 'exec ${mydir}/emacs-xft-%{emacs_version} \' \
                                       >> $RPM_BUILD_ROOT%{_bindir}/emacs-xft
echo '       --font "Bitstream Vera Sans Mono-13" \' \
echo '       "${@}"' \
                                       >> $RPM_BUILD_ROOT%{_bindir}/emacs-xft
chmod 755 $RPM_BUILD_ROOT%{_bindir}/emacs-xft

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, root) %{_datadir}/emacs
%{_datadir}/emacs/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Thu Jan  3 2008 - laca@sun.com
- update snapshot tarball
- add patch fonts.diff that customizes the mode-line fonts so that they
  look sane
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWlibsdl or SFEsdl.
* Sun Feb 25 2007 - laca@sun.com
- update to new cvs snapshot tarball
* Fri Feb 16 2007 - dougs@truemail.co.th
- Removed -j from make
* Sun Nov  5 2006 - laca@sun.com
- create
