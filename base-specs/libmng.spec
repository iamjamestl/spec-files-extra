#
# spec file for package SFElibmng
#
# includes module(s): libmng
#

Name:                    SFElibmng
Summary:                 libmng  - the MNG reference library
Version:                 1.0.10
Source:                  %{sf_download}/libmng/libmng-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWlcms-devel
#note: needs 64-bit version of SUNWlcms
Requires: SUNWlcms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n libmng-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
cp makefiles/configure.in .
cp makefiles/Makefile.am .
for f in *.[ch]; do dos2unix -ascii $f $f; done
libtoolize --force
aclocal $ACLOCAL_FLAGS
autoconf
automake -a -c -f
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sat Mar 22 2008 - Thomas Wagner
- (Build-)Requires: SUNWlcms(-devel)  (was: SFElcms)
* Wed Mar  5 2008 - Thomas Wagner
- add 64bit support, move to base-spec, new SFElibmng.spec
* Sun Nov 4 2007 - markwright@internode.on.net
- Bump to 1.1.10
* Fri Mar 30 2007 - daymobrew@users.sourceforge.net
- Change source URL to one working sourceforge mirror
* Sun Jan  7 2007 - laca@sun.com
- create
