#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%define _basedir /usr/g++
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
# Build multithreaded libs: no need for non-multithreaded libs
%define boost_with_mt 1

%include packagenamemacros.inc

%use boost = boost.spec

Name:                SFEboost-gpp
IPS_Package_Name:	system/library/g++/boost
Summary:             Free peer-reviewed portable C++ libraries (g++-built)
License:             Boost License Version
SUNW_Copyright:      boost.copyright
Version:             %{boost.version}
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: %{pnm_buildrequires_python_default}
BuildRequires:	SFEicu-gpp-devel
Requires:	SFEicu-gpp

%package -n %name-devel
IPS_package_name:	system/library/g++/boost/header-boost
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%package -n %name-doc
IPS_package_name:	system/library/g++/boost/documentation
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%boost.prep -d %name-%version

%build
%boost.build -d %name-%version

%install
rm -rf %{buildroot}
%boost.install -d %name-%version

cd %{_builddir}/%name-%version/boost_%{boost.ver_boost}

mkdir -p %{buildroot}%{_docdir}/boost-%{version}
cd "doc/html"
for i in `find . -type d`; do
  mkdir -p %{buildroot}%{_docdir}/boost-%{version}/$i
done
for i in `find . -type f`; do
  cp $i %{buildroot}%{_docdir}/boost-%{version}/$i
done

# It's not worth figuring out how to get the Boost build system
# to set the runpath correctly
%define rpath 'dyn:runpath /usr/g++/lib:/usr/gnu/lib'
pushd %{buildroot}%{_libdir}
for i in *.so.*; do
  elfedit -e %rpath $i
done
popd

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files -n %name-devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/boost
%{_libdir}/lib*.a

%files -n %name-doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/boost-%{version}

%changelog
* Sun Apr 29 2012 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_python_default}, %include packagenamacros.inc
* Thu Jan 12 2012 - Milan Jurik
- package restructuralization, static libs re-added
* Sun Jun 31 2011 - Alex Viskovatoff
- set correct runpath for some more shared libraries
* Fri Jul 29 2011 - Alex Viskovatoff
- add License and SUNW_Copyright tags
* Thu Jun 23 2011 - Alex Viskovatoff
- set correct runpath for libboost_regex, so it finds ICU libraries
* Sun Apr  3 2011 - Alex Viskovatoff
- use new g++ libs pathname; build multithreaded libs
* Fri Jan 11 2011 - Milan Jurik
- do not deliver static libs
* Mon May 17 2010 - Albert Lee <trisk@opensolaris.org>
- Remove SUNWicu* dependencies added in error
* Sat Jan 30 2010 - Brian Cameron <brian.cameron@sun.com>
- Install header files, so it isn't necessary to install the Sun Studio
  version of boost to access these.
* Wed Dec 02 2009 - Albert Lee <trisk@opensolaris.org>
- Re-add SUNWicud
* Mon Oct 12 2009 - jchoi42@pha.jhu.edu
- changed %builddir, created base-specs/boost.spec
* Wed Apr 23 2008 - laca@sun.com
- create, based on SFEboost.spec
- force building with g++ and install the libs to /usr/lib/g++/<version>
* Thu Nov 22 2007 - daymobrew@users.sourceforge.net
- Comment out SUNWicud dependency to get module to build.
* Mon Aug 13 2007 - trisk@acm.jhu.edu
- Initial version
