#
# spec file for package SUNWlcms
#
# temp spec for lcms until SFW integrate it
#

%include Solaris.inc

%define python_version 2.4

Name:                    SUNWlcms
Summary:                 Little ColorManagement System
Version:                 1.17
Source:                  http://www.littlecms.com/lcms-%{version}.tar.gz
Patch1:                  lcms-01-python-libs.diff
URL:                     http://www.littlecms.com
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          default-copyright.txt
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires: SUNWTiff
Requires: SUNWjpg
Requires: SUNWzlib
Requires: SUNWlibms
Requires: SUNWPython
Requires: SUNWlibC
BuildRequires: SUNWPython-devel
BuildRequires: SUNWTiff-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWzlib
BuildRequires: SFEswig
%include default-depend.inc

%ifarch sparc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n lcms-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags"

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
aclocal $ACLOCAL_FLAGS
automake -c -f
./configure --prefix=%{_prefix} --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --includedir=%{_includedir} \
            --with-python --mandir=%{_mandir} --enable-static=no
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

cd $RPM_BUILD_ROOT%{_prefix}/lib/python%{python_version}
mv site-packages vendor-packages
rm vendor-packages/_lcms.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/python%{python_version}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

# endif for "ifarch sparc"
%endif

%changelog
* Thu May 15 2008 - damien.carbery@sun.com
- Only build package on sparc as SUNWlcms is in snv_89 x86.
* Sun Sep 16 2007 - dougs@truemail.co.th
- Bump to 1.17
* Tue Feb  6 2007 - damien.carbery@sun.com
- Bump to 1.16. Add aclocal call because automake version mismatch.
* Fri Jun 23 2006 - laca@sun.com
- rename to SFElcms
- update file attributes to match JDS
* Tue Mar 21 2006 - damien.carbery@sun.com
- Minor mods to %files (/usr/lib -> %{_libdir}).
* Fri Mar 17 2006 - markgraf@neuro2.med.uni.magdeburg.de
- Initial spec
