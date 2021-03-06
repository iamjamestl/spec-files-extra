#
# NoCopyright 2009 - Gilles Dauphin 
#
#

%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%include base.inc

%define texlive_ver	20110705

%define _texmf_dir /usr/texlive

Name:		SFEtexlive
IPS_Package_Name:	 text/texlive
Version:	%{texlive_ver}
Summary:	Binaries for the TeX formatting system
URL:		http://tug.org/texlive

Group:		Applications/Publishing
License:	GPLv2 and More
URL:		http://tug.org/texlive/

Source:         ftp://tug.org/historic/systems/texlive/2011/texlive-%{texlive_ver}-source.tar.xz
Source1:        ftp://tug.org/historic/systems/texlive/2011/texlive-%{texlive_ver}-texmf.tar.xz

BuildRoot:	%{_tmppath}/%{name}-%{version}-build

BuildRequires:	SUNWflexlex
BuildRequires:	SUNWbison
BuildRequires:	SUNWncurses
BuildRequires:	SUNWzlib
BuildRequires:	SUNWpng
BuildRequires:	SUNWgd2
BuildRequires:	%{pnm_buildrequires_SFExz}
Requires:	SFEtexlive-texmf

%description
TeXLive is an implementation of TeX for Linux or UNIX systems. TeX takes
a text file and a set of formatting commands as input and creates a
printable file as output. Usually, TeX is used in conjunction with
a higher level formatting package like LaTeX or PlainTeX, since TeX by
itself is not very user-friendly.

Install texlive if you want to use the TeX text formatting system. Consider
to install texlive-latex (a higher level formatting package which provides
an easier-to-use interface for TeX).

The TeX documentation is located in the texlive-doc package.

%prep
#%setup -q -c -n %{name}-%{version}
tar xJf %{SOURCE}

%build
set -x
cd texlive-%{version}-source
#TL_WORKDIR=Work
# equiv. --prefix=%{prefix} in configure
# @ install do DESTDIR=make install DESTDIR=$RPM_BUILD_ROOT
#TL_INSTALL_DEST=%{_prefix}/texlive
#export TL_INSTALL_DEST
export CC=gcc
export CXX=g++
CFLAGS="$CFLAGS -DZZIP_inline= "
export CFLAGS
TL_TARGET=all
export TL_TARGET
#TODO look at utils/dialog,ps2eps,pdfopen and process DESTDIR in a Makefile.am...
./Build \
	--enable-shared=no \
	--with-x \
	--with-system-ncurses \
	--with-system-zlib \
	--with-system-pnglib \
	--with-system-gd \
	--with-gd-includes=/usr/include/gd2 \
	--with-system-freetype2 \
	--with-freetype2-include=/usr/include/freetype2 \
	--disable-native-texlive-build

# because freetype2 is in /usr/include , hard code the path
#	--with-freetype2-include=%{_includedir}/freetype2 \
#	--without-omega \
#	--without-aleph 
#	--with_dialog=no \
#	--without-ps2eps \
#	--with_psutils=no \
#	--with-tpic2pdftex=no \


%install
rm -rf ${RPM_BUILD_ROOT}
cd texlive-%{version}-source/Work

#export LD_LIBRARY_PATH=`pwd`/texk/kpathsea/.libs
mkdir -p ${RPM_BUILD_ROOT}/usr/texlive
# don't install kpathsea
# ruse
# mv texk/kpathsea/Makefile texk/kpathsea/Makefile.save
#make install  DESTDIR=$RPM_BUILD_ROOT
make install
tex_arch=`../build-aux/config.guess`
#ln -s /usr/texlive/bin/$tex_arch ../inst/share/bin
# Note: binary MUST BE in /usr/texlive/bin/$ARCH/ , because some link would break
mv ../inst/* ${RPM_BUILD_ROOT}/usr/texlive
rm ${RPM_BUILD_ROOT}/usr/texlive/texmf/scripts/texlive/tlmgr.pl
rm ${RPM_BUILD_ROOT}/usr/texlive/texmf/web2c/fmtutil.cnf

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
set -x
PATH=$PATH:/usr/texlive/bin
export PATH
/usr/texlive/bin/mktexlsr /usr/texlive/texmf /usr/texlive/texmf-dist /usr/texlive/texmf-doc /usr/texlive 
/usr/texlive/bin/texconfig-sys init 
/usr/texlive/bin/texconfig-sys rehash 
/usr/texlive/bin/fmtutil-sys --all 
/usr/texlive/bin/updmap-sys --syncwithtrees 
exit 0		# johny be good

#TODO
# postun: post-uninstall

%files
%defattr (-,root,bin)
%dir %attr (0755, root, sys) /usr
# config files
%dir %attr (0755, root, bin) %{_texmf_dir}
%{_texmf_dir}/*

%changelog
* Sat Jun 23 2012 - Thomas Wagner
- change to (Build)Requires pnm_buildrequires_SFExz (solves SFExz conflict w/ compress/xz), %include packagenamemacros.inc
* Thu Mar 15 2012 - Logan Bruns <logan@gedanken.org>
- update to 20110705 
- TODO: post steps are not being run on OI/S11. so you have to update
  texmf/web2c/texmf.cnf and run them manually at the moment. that
  should be fixed.
* April 2010 - Gilles Dauphin
- hardcode the path of freetype2
# because freetype2 is in /usr/include , hard code the path
* 17 Aug 2009 - Gilles Dauphin
- check with texmf files.
* Aug 2009 - Gilles Dauphin
- Initial setup, I look at Fedora and Pkgsrc
