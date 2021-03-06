#
# spec file for package SFEasciidoc
#
# includes module(s): asciidoc
#

%include Solaris.inc
%include packagenamemacros.inc

Name:                    SFEasciidoc
IPS_Package_Name:	developer/documentation-tool/asciidoc
Summary:                 AsciiDoc - Text based document generation
Group:                   Development/Distribution Tools
License:                 GPLv2
Version:                 8.6.8
URL:                     http://www.methods.co.nz/asciidoc/
Source:                  %{sf_download}/asciidoc/asciidoc-%{version}.tar.gz
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: 	         %{pnm_requires_python_default}
BuildRequires: 	         %{pnm_buildrequires_python_default}
Requires: %{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
%setup -q -n asciidoc-%version

%build
./configure --prefix=%{_prefix}	\
	--sysconfdir=%{_sysconfdir}

make
# Disabled because of docbook problem
#python a2x.py -f manpage doc/asciidoc.1.txt
#python a2x.py -f manpage doc/a2x.1.txt

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/asciidoc

%changelog
* Sun Aug 05 2012 - Milan Jurik
- bump to 8.6.8
* Fri Apr 20 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_python_default}, %include packagenamemacros.inc
* Fri Apr 20 2012 - Logan Bruns <logan@gedanken.org>
- bump to 8.6.7
* Mon Dec 12 2011 - Milan Jurik
- bump to 8.6.6
* Mon Jul 11 2011 - Guido Berhoerster
- added copyright file
* Sat Feb 05 2011 - Milan Jurik
- bump to 8.6.3
* Sun Jul 11 2010 - Milan Jurik
- update to 8.5.3
* Sat Aug 16 2008 - nonsea@users.sourceforge.net
- Bump to 8.2.7
* Mon May 05 2008 - brian.cameron@sun.com
- Bump to 8.2.6.
* Wed Dec 05 2007 - trisk@acm.jhu.edu
- Bump to 8.2.5, correct URL
* Tue Sep 18 2007 - nonsea@users.sourceforge.net
- Bump to 8.2.3
* Mon Aug 06 2007 - brian.cameron@sun.com
- Bump to 8.2.2.
* Fri Jun 22 2007 - laca@sun.com
- bump to 8.2.1
* Tue Feb 13 2007 - laca@sun.com
- create
