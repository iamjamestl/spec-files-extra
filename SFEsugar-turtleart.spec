#
# spec file for package SFEsugar-turtleart
#
# includes module(s): sugar-turtleart
#

%define pythonver 2.6

%include Solaris.inc
Name:                    SFEsugar-turtleart
Summary:                 Sugar TurtleArt
URL:                     http://www.sugarlabs.org/
Version:                 126 
Source:                  http://download.sugarlabs.org/sources/sucrose/fructose/TurtleArt/TurtleArt-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:                SFEsugar
BuildRequires:           SFEsugar

%if %build_l10n
%package l10n
Summary:      %{summary} - l10n files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc
Requires:     %{name}
%endif

%prep
%setup -q -n TurtleArt-%version

%build
export PYTHON=/usr/bin/python%{pythonver}
python%{pythonver} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{pythonver} setup.py install --prefix=$RPM_BUILD_ROOT/usr

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

# replace the old scripts with script files
%post
%restart_fmri gconf-cache desktop-mime-cache icon-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/sugar

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%changelog
* Sat Nov 19 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 126
* Tue Sep 27 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 115
* Sat Oct 23 2010 - Brian Cameron  <brian.cameron@oracle.com>
- Bump to 100.
* Sat Aug 07 2010 - Brian Cameron  <brian.cameron@oracle.com>
- Bump to 93.
* Tue Apr 27 2010 - Brian Cameron  <brian.cameron@sun.com
- Bump to 86.
* Wed Mar 10 2010 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 83.
* Tue Feb 02 2010 - Brian Cameron  <brian.cameron@sun.com>
- Created with 56.
