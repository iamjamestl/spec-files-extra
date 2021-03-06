#
# spec file for package SFEimagemagick.spec
#
# includes module(s): imagemagick
#
%include Solaris.inc
%include packagenamemacros.inc

%define src_name	ImageMagick
%define major		6.7.9
%define minor		10

# Note: we purposely take the latest version from legacy since these
# are stable (permanent) links whereas the absolute latest version is
# placed one directory up but only temporarily while it is new.
%define src_url		ftp://ftp.imagemagick.org/pub/ImageMagick/legacy

Name:                   SFEimagemagick
IPS_Package_Name:	image/editor/imagemagick
Summary:                ImageMagick - Image Manipulation Utilities and Libraries
Version:                %{major}.%{minor}
License:                ImageMagick License
SUNW_Copyright:         imagemagick.copyright
Source:                 %{src_url}/%{src_name}-%{major}-%{minor}.tar.gz
Group:			Graphics
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%include perl-depend.inc

BuildRequires:	SFEjasper-devel
Requires:	SFEjasper
BuildRequires:	SFElibwebp-devel
Requires:	SFElibwebp
BuildRequires:	SUNWlibrsvg-devel
Requires:	SUNWlibrsvg
BuildRequires:	%{pnm_buildrequires_SUNWfftw3}
Requires:	%{pnm_requires_SUNWfftw3}
BuildRequires:	SUNWpango-devel
Requires:	SUNWpango
BuildRequires:  SUNWpng-devel
Requires:       SUNWpng
BuildRequires:  SUNWTiff-devel
Requires:       SUNWTiff
BuildRequires:  SUNWlcms
Requires:       SUNWlcms
BuildRequires:  SUNWjpg-devel
Requires:       SUNWjpg
BuildRequires:  SUNWzlib
Requires:       SUNWzlib
BuildRequires:  SUNWopenexr
Requires:       SUNWopenexr

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
Requires: %name


%prep
%setup -q -n %{src_name}-%{major}-%{minor}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-I/usr/include/freetype2 -I/usr/X11/include"
export LDFLAGS="%_ldflags -L/usr/X11/lib -R/usr/X11/lib"
if [ "x`basename $CC`" = xgcc ]
then
	%error "Building this spec with GCC is not supported."
fi
export CFLAGS="%optflags -xCC"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
	    --with-perl=yes		\
            --with-gs-font-dir=/usr/share/ghostscript/fonts \
	    --enable-shared		\
	    --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a
find $RPM_BUILD_ROOT%{_libdir} -name lib\*.\*a -exec rm {} \;
find $RPM_BUILD_ROOT -name .packlist -exec %{__rm} {} \; -o -name perllocal.pod  -exec %{__rm} {} \;
site_perl=$RPM_BUILD_ROOT/usr/perl5/site_perl
vendor_perl=$RPM_BUILD_ROOT/usr/perl5/vendor_perl
mv $site_perl $vendor_perl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/%{src_name}-%{major}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/%{src_name}-%{major}
%{_mandir}
%dir %attr (0755,root,other) %{_datadir}/doc
%{_datadir}/doc/*
%{_prefix}/perl5

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%files root
%defattr (-, root, sys)
%dir %attr (-, root, sys) %_sysconfdir
%attr (-, root, root) %_sysconfdir/ImageMagick

%changelog
* Tue Oct 30 2012 - Thomas Wagner
- remove perllocal.pod
* Sun Oct 26 2012 - Thomas Wagner
- change (BuildRequires) to %{pnm_buildrequires_SUNWfftw3}, %include packagenamemacros.inc
- fix code error at configure, trailing space at end of line: "   \ $"
* Thu Oct 25 2012 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.9-10
* Mon Oct 15 2012 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.8-10
- Added more graphic dependencies for better usage
- added fix for fonts dir in GNU Ghostscript Fonts
* Sun Aug 05 2012 - Milan Jurik
- add more build dependencies
* Sun May 20 2012 - Logan Bruns <logan@gedanken.org>
- update to 6.7.6-10
* Sun Apr 29 2012 - Logan Bruns <logan@gedanken.org>
- update to 6.7.5-10
* Sun Feb 26 2012 - Logan Bruns <logan@gedanken.org>
- update to 6.7.4-10 and added ips package name
* Thu Jan 19 2012 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.4-7
* Thu Dec 8 2011 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.3-10
* Wed Sep 14 2011 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.2-6
* Wed Aug 24 2011 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.1-10
* Fri Jul 29 2011 - Alex Viskovatoff
- Add missing (build) dependency
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Jul 03 2011 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.0-10
* Mon Jun 06 2011 - Ken Mays <kmays2000@gmail.com>
- update to 6.7.0-4
* Tue Apr 12 2011 - Alex Viskovatoff
- update to 6.6.9-4
* Thu Jan 13 2010 - Milan Jurik
- bump to 6.6.7-0
* Thu Nov 26 1009 - Thomas Wagner
- bump to 6.5.8-0
- new download-URL
- changed include path /usr/include/freetype2
* Sat Jan 26 2008 - moinak.ghosh@sun.com
- Bump version to 6.3.6-10.
- Add check to prevent build using Gcc.
- Add dependency on Perl.
* Sun Nov 18 2007 - daymobrew@users.sourceforge.net
- Bump to 6.3.6-9.
* Tue Jul 10 2007 - brian.cameron@sun.com
- Bump to 6.3.5.  Remove the -xc99=%none from CFLAGS since
  it is breaking the build.
* Tue Jun  5 2007 - dougs@truemail.co.th
- Initial version - version in sfw is too old :(
