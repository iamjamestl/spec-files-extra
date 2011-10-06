#
# spec file for package XFCE ristretto 
#
# by Ken Mays

%include Solaris.inc

%define src_name ristretto
%define src_url http://archive.xfce.org/src/apps/ristretto/0.0/

Name:           SFExfce-ristretto
Summary:        Image Viewer
Version:        0.0.93
URL:            http://www.xfce.org/
Source:         %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:  SFElibxfcegui4 
BuildRequires:  SUNWlibexif
BuildRequires:  SFElibxfce4ui
BuildRequires:  SFEthunar
BuildRequires:  SFExfce4-dev-tools 
Patch1: 	ristretto-01-window.diff
Patch2:		ristretto-02-string.diff
Patch3: 	ristretto-03-main.diff
Patch4:		ristretto-04-makefile.diff
 
%description
Ristretto is a simple image viewer for Xfce

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi 

./configure --prefix=%{_prefix}         \
        --bindir=%{_bindir}             \
        --libdir=%{_libdir}             \
        --libexecdir=%{_libexecdir}     \
        --datadir=%{_datadir}           \
        --mandir=%{_mandir}             \
        --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,bin)
%{_bindir}/ristretto 
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/applications/ristretto.desktop 
%{_datadir}/icons/hicolor/*/apps/ristretto.* 
%{_datadir}/doc 
%{_datadir}/locale

%changelog
* Tue Oct 5 2011 - Ken Mays <kmays2000@gmail.com>
- Initial spec (0.0.93) 