#
# spec file for package SFEperl-io-compress-zlib
#
# includes module(s): IO-Compress-Zlib
#


%include Solaris.inc
%include packagenamemacros.inc

#note: download file version differs from package version (for IPS not accepting "015" / leading zero)
%define module_version 2.15
%define module_version_download 2.015
%define module_package_name io-compress-zlib

Name:                    SFEperl-io-compress-zlib
IPS_package_name:        library/perl-5/%{module_package_name}
Summary:                 IO-Compress-Zlib-%{module_version_download} PERL module
Version:                 %{perl_version}.%{module_version}
Source:                  http://www.cpan.org/modules/by-module/IO/IO-Compress-Zlib-%{module_version_download}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           %{pnm_buildrequires_perl_default}
Requires:                %{pnm_requires_perl_default}
BuildRequires:           %{pnm_buildrequires_SUNWsfwhea}

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version

%build
cd IO-Compress-Zlib-%{module_version_download}
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLDIRS=vendor \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_site_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_site_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLVENDORLIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLVENDORARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLVENDORMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLVENDORMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd IO-Compress-Zlib-%{module_version_download}
make install

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib
find $RPM_BUILD_ROOT -name .packlist -exec %{__rm} {} \; -o -name perllocal.pod  -exec %{__rm} {} \;

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/%{perl_path_vendor_perl_version}
%{_prefix}/%{perl_path_vendor_perl_version}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Mon May 14 2012 - Thomas Wagner
- simplify %files
- add missing INSTALLVENDORLIB to get path vendor_perl work on perl 5.12
- bump version to 2.015 (2.15 on IPS)
- add IPS_package_name library/perl-5/%{module_package_name}
* Fri Jun 23 2011 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default} and make module 
  paths dynamic, define fewer directories in %files
- make version number IPS capable
* Tue Nov 13 2007 - trisk@acm.jhu.edu
- Initial spec
