#
# spec file for package SFElyx
#
# includes module: lyx
#

# To be able to typeset LyX documents, you need to have TeX installed.
# Since SFEtexlive.spec is not currently maintained, it is probably best
# to install TeX Live using its own native installer.  See
#   http://www.tug.org/texlive/acquire-netinstall.html.
# You need to make sure that the various TeX executables are in your PATH.
# The TeX Live installer gives you the option of creating symbolic links
# to them automatically; creating symbolic links of TeX executables to
# a directory in your PATH is probably the best way of making LyX find them.

# Since the libraries of SFEqt47-gpp are now in a non-standard location,
# you will need to do, for example:
# pfexec elfedit -e 'dyn:runpath /usr/gnu/lib' pdftex

%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%include base.inc
%define srcname lyx

Name:		SFElyx
IPS_Package_Name:	desktop/publishing/lyx
Summary:	Graphical LaTeX front end: What you see is what you mean
URL:		http://www.lyx.org
License:	GPLv2
Group:		Applications/Office
SUNW_Copyright:	lyx.copyright
Version:	2.0.4
Source:		ftp://ftp.lyx.org/pub/lyx/stable/2.0.x/%srcname-%version.tar.gz
Source1:	%srcname.desktop
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SFEgcc
BuildRequires:	SFEqt-gpp-devel
BuildRequires:	SFEboost-gpp-devel
BuildRequires:	SUNWgnome-spell
BuildRequires:	%{pnm_buildrequires_python_default}
Requires:	SFEgccruntime
Requires:	SFEqt-gpp
Requires:	SFEboost-gpp
Requires:	SUNWgnome-spell
Requires:	SFElibiconv
Requires:	%{pnm_requires_python_default}

%if %build_l10n
%package l10n
Summary:        %summary - l10n files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires:       %name
%endif


%prep
%setup -q -n %srcname-%version


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CXX=g++
export CPPFLAGS="-I/usr/g++/include -I/usr/g++/include/qt"
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -pthreads -fpermissive"
export LDFLAGS="%_ldflags -pthreads -lxnet -L/usr/g++/lib -R/usr/g++/lib"

# SFEhunspell is built with CC, so SFElyx can't link against it
# aspell is deprecated
./configure --prefix=%_prefix --with-qt4-dir=/usr/g++ --without-included-boost --without-aspell --without-hunspell

make -j$CPUS


%install
rm -rf %buildroot

make install DESTDIR=%buildroot
mkdir %buildroot%_datadir/applications
cp %SOURCE1 %buildroot%_datadir/applications

%if %build_l10n
%else
rm -rf %buildroot%_datadir/locale
%endif

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%_bindir/lyx
%_bindir/lyxclient
%_bindir/tex2lyx
%dir %attr (-, root, sys) %_datadir
%_datadir/%srcname
%_mandir
%dir %attr(0755, root, other) %_datadir/applications
%_datadir/applications/%srcname.desktop

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale
%endif


%changelog
* Sun Aug 05 2012 - Milan Jurik
- bump to 2.0.4
* Sat Jun 23 2012 - Thomas Wagner
- make (Build)Requries  %{pnm_buildrequires_python_default}
* Sun Jan 08 2012 - Milan Jurik
- bump to 2.0.2
* Sun Jul 31 2011 - Alex Viskovatoff
- Add missing (build) dependency
* Sat Jul 23 2011 - Alex Viskovatoff
- Use system Boost; add SUNW_Copyright
* Sun Apr  3 2011 - Alex Viskovatoff <herzen@imap.cc>
- Disable aspell; LyX can use library/spell-checking/enchant
* Wed Mar 30 2011 - Alex Viskovatoff
- Adapt to gcc-built Qt now being in /usr/g++
- Update to 2.0.0rc2; disable hunspell; remove build dependency on Boost
* Tue Feb  8 2011 - Alex Viskovatoff
- Adapt to Qt gcc libs now being in /usr/stdcxx
* Sun Jan 30 2011 - Alex Viskovatoff
- Initial spec
