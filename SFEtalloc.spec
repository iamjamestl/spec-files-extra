#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define source_name samba-4.0.0alpha11

Name:                SFEtalloc
Summary:             A hierarchical pool based memory system with destructors.
Version:             2.0.1 
Source:              http://us5.samba.org/samba/ftp/samba4/%{source_name}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWswig
Requires:SUNWswig

%prep
rm -rf  %name-%version
%setup -q -c -n  %name-%version 

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="-g -mt %optflags"
export LDFLAGS="-z ignore %_ldflags"

cd %{source_name}/lib/talloc
./autogen.sh
./configure --prefix=%{_prefix}  \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
cd %{source_name}/lib/talloc

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/swig/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Sat Mar 13 2010 - brian.lu@sun.com
- Build talloc under SFEtalloc-2.0.1 direcotory
* Wed Dec 02 2009 - brian.lu@sun.com
- Bump to samba4 alpha9
* Thu Aug 27 2009 - brian.lu@sun.com
- add "-mt" to CFLAGS to set errno correctly in MT environment
* Wed Jun 03 2009 - brian.lu@sun.com
- Add dependency SUNWswig
* Wed Feb 18 2009 - jedy.wang@sun.com
- Do not use optimization option for now.
* Tue Feb 17 2009 - jedy.wang@sun.com
- Fix file attribute problem.
* Tue Feb 10 2009 - jedy.wang@sun.com
- Initial spec
