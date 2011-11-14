#
# spec file for package SFEopenjpeg
#
# includes module(s): openjpeg
#
%include Solaris.inc

%define	src_name openjpeg
%define	src_url	http://www.openjpeg.org
%define src_version 1_4_sources_r697

Name:		SFEopenjpeg
IPS_Package_Name:	image/library/openjpeg
Group:		System/Libraries
Summary:	Open Source multimedia framework
License:	BSD
SUNW_Copyright:	openjpeg.copyright
Version:	1.4
Source:		http://openjpeg.googlecode.com/files/openjpeg_v%{src_version}.tgz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFEcmake

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}_v%{src_version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

mkdir -p builds/unix
cd builds/unix

cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} ../..
make VERBOSE=1 -j$CPUS

%install
rm -rf %{buildroot}
cd builds/unix
make install DESTDIR=%{buildroot} INSTALL="%{_bindir}/ginstall -c -p"

rm -f %{buildroot}/%{_includedir}/openjpeg.h
ln -s openjpeg-%{version}/openjpeg.h %{buildroot}/%{_includedir}/openjpeg.h

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/openjpeg-%{version}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Tue Oct 11 2011 - Milan Jurik
- bump to 1.4
- add IPS package name
* Sun Jul 24 2011 - Alex Viskovatoff
- Add SUNW_Copyright
* Fri May 21 2010 - Milan Jurik
- update to 1.3, split devel package
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
