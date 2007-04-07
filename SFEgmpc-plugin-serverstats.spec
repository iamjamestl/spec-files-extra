#
# spec file for package SFEgmpc-plugins-serverstats (plugin)
#
# use gcc to compile
#

%include Solaris.inc
Name:                    SFEgmpc-plugins-serverstats
Summary:                 gmpc-serverstats - server statistics and database details from mpd server  - plugin for gmpc
URL:                     http://sarine.nl/gmpc-plugins-serverstats
Version:                 0.14.0
%define gmpc_version 0.14.0
Source:                  http://download.sarine.nl/gmpc-%{gmpc_version}/plugins/gmpc-serverstats-%{version}.tar.gz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires:           SFEgmpc-devel
Requires:                SFEgmpc

%include default-depend.inc

%prep
%setup -q -n gmpc-serverstats-%version

%build

export LDFLAGS="-lX11"
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++

./configure --prefix=%{_prefix}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README ChangeLog CREDITS COPYING INSTALL NEWS AUTHORS TODO ABOUT-NLS
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gmpc
%dir %attr (0755, root, other) %{_datadir}/gmpc/plugins
%{_datadir}/gmpc/plugins/*.so
%{_datadir}/gmpc/plugins/serverstats/*


%changelog
* Thu Apr 06 2007  - Thomas Wagner
- Initial spec
