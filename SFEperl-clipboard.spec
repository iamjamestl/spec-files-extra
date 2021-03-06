#
# spec file for package: SFEperl-clipboard
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
%include Solaris.inc
%include packagenamemacros.inc

%define tarball_version 0.13
%define tarball_name    Clipboard

Name:		SFEperl-clipboard
IPS_package_name: library/perl-5/clipboard
Version:	0.13
IPS_component_version: 0.13
Summary:	Perl module Clipboard
License:	Artistic
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~king/%{tarball_name}-%{tarball_version}
SUNW_Basedir:	%{_basedir}
#SUNW_Copyright: %{name}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/K/KI/KING/Clipboard-%{tarball_version}.tar.gz

BuildRequires:  %{pnm_buildrequires_perl_default}
Requires:  	%{pnm_requires_perl_default}
Requires: 	SFExclip

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin@justplayer.com>
Meta(info.upstream):            Ryan King <rking@panoptic.com>
Meta(info.upstream_url):        http://search.cpan.org/~king/%{tarball_name}-%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

%description

%prep
%setup -q -n %{tarball_name}-%{tarball_version}

%build
perl Makefile.PL PREFIX=%{_prefix} DESTDIR=$RPM_BUILD_ROOT LIB=%{_prefix}/%{perl_path_vendor_perl_version}
make

%install
rm -rf $RPM_BUILD_ROOT
make pure_install
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_datadir}/man/man3 $RPM_BUILD_ROOT%{_datadir}/man/man3perl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%{_prefix}/perl5
%dir %attr(0755,root,sys) %{_datadir}
%{_mandir}
%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*

%changelog
* Sat Jun 18 2011 - Thomas Wagner
- comment Copyright. need a general solution to point to perl license.
* Fri Jun 17 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic
* Mon Jun 13 2011 - Thomas Wagner
- Initial spec
