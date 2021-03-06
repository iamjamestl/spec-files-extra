#
# spec file for package SFElibmatroska
#
# includes module(s): libmatroska
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define _prefix %_basedir/g++
%define srcname libmatroska

Name:		SFElibmatroska-gpp
IPS_package_name: library/video/g++/libmatroska
License:	LGPL
Summary:	Matroska Video Container
Group:		System Environment/Libraries
URL:		http://www.matroska.org
Vendor:		Moritz Bunkus <moritz@bunkus.org>
Version:	1.3.0
Source:		http://dl.matroska.org/downloads/%srcname/%srcname-%version.tar.bz2
Patch1:		libmatroska-01-makefile.diff

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SFEgcc
Requires:	SFEgccruntime
BuildRequires:	SFElibebml-gpp-devel
Requires:	SFElibebml-gpp

%description
Matroska aims to become THE Standard of Multimedia Container Formats.
It was derived from a project called MCF, but differentiates from it
significantly because it is based on  EBML (Extensible Binary Meta
Language), a binary derivative of XML. EBML enables the Matroska
Development Team to gain significant advantages in terms of future
format extensibility, without breaking file support in old parsers.
These libraries are used by mkvtoolnix.

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %srcname-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CXXFLAGS="%cxx_optflags -I%/usr/g++/include"
export ACLOCAL_FLAGS="-I/usr/share/aclocal -I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

cd make/linux
gmake -j$CPUS  CXX=g++ AR=CC  DEBUGFLAGS=-g WARNINGFLAGS="" \
ARFLAGS="-xar -o" LOFLAGS=-fpic \
LIBSOFLAGS="%_ldflags -L/usr/g++/lib -L/usr/gnu/lib -R/usr/g++/lib:/usr/gnu/lib -G -h "

%install
rm -rf $RPM_BUILD_ROOT
cd make/linux
gmake install_headers prefix=$RPM_BUILD_ROOT%{_prefix} INSTALL=ginstall
gmake install_sharedlib prefix=$RPM_BUILD_ROOT%{_prefix} INSTALL=ginstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Sun Aug 05 2012 - Milan Jurik
- bump to 1.3.0
* Sun Jun 17 2012 - Thomas Wagner
- fix (Build)Requires on SFElibebml-gpp(-devel)
* Fri Dec  2 2011 - Thomas Wagner
- Add IPS package name
- copy SFElibmatroska.spec to SFElibmatroska-gpp.spec
- move to gcc/g++ and relocate to prefix /usr/g++
- add (Build)Requires on SFElibebml-gpp
- remove (Build)Requires on SUNWstdcxx 
* Sat Feb  5 2011 - Alex Viskovatoff
- Bump to 1.1.0
* Thu Jan 27 2011 - Alex Viskovatoff
- Go back to using -library=stdcxx4
* Tue Nov 23 2010 - Alex Viskovatoff
- Use stdcxx.inc instead of -library=stdcxx4; install in /usr/stdcxx
* Fri Oct  1 2010 - Alex Viskovatoff
- Update to 1.0.0; use stdcxx (requires Solaris Studio 12.2)
- Patch linux Makefile so that it works with Linux and Solaris
  instead of creating a new Makefile for Solaris.
* Mar 2010  - Gilles Dauphin
- look at install dir. Example search for /usr/SFE/include
- idem for _libdir
* Fri Jul 13 2007 - dougs@truemail.co.th
- Initial version
