#
# spec file for package SFEopenafs
#
# includes module(s): openafs
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define _basedir /
%define _bindir /usr/bin
%define _includedir /usr/include
%define _libdir /usr/lib

%define srcname openafs

Name:                    SFEopenafs
IPS_Package_Name:        system/file-system/openafs
Summary:                 OpenAFS - Distributed file system
Group:                   Utility
Version:                 1.6.1.5
License: 		 IBM Public License Version 1.0
Patch1:                  openafs-01-configure.diff
Patch2:                  openafs-02-afs-rc.diff
Patch3:                  openafs-03-enable-multiarch.diff
Patch4:                  openafs-04-krb5_conf_path.diff
#Source:                  http://openafs.org/dl/openafs/%{version}/%{srcname}-%{version}-src.tar.bz2
Source:                  http://openafs.org/dl/openafs/1.6.1/%{srcname}-1.6.1-src.tar.bz2
#Source2:                 http://openafs.org/dl/openafs/%{version}/%{srcname}-%{version}-doc.tar.bz2
Source2:                 http://openafs.org/dl/openafs/1.6.1/%{srcname}-1.6.1-doc.tar.bz2
Source3:                 openafs.xml
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		SUNWhea
BuildRequires:		SUNWlibm

%description
AFS is a distributed filesystem product, pioneered at Carnegie Mellon
University and supported and developed as a product by Transarc
Corporation (now IBM Pittsburgh Labs). It offers a client-server
architecture for federated file sharing and replicated read-only
content distribution, providing location independence, scalability,
security, and transparent migration capabilities. AFS is available for
a broad range of heterogeneous systems including UNIX, Linux, MacOS X,
and Microsoft Windows

IBM branched the source of the AFS product, and made a copy of the
source available for community development and maintenance. They
called the release OpenAFS.

%prep
#%setup -q -n %{srcname}-%{version}
%setup -q -n %{srcname}-1.6.1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

(cd .. ; tar xjf %{SOURCE2} )

#openafs manifest
cp -p %{SOURCE3} openafs.xml

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export KRB5_CONFIG=/usr/bin/krb5-config
./configure --prefix=/usr        			\
            --includedir=/usr/include/openafs           \
            --libexecdir=/usr/lib                       \
            --localstatedir=/var                        \
            --sysconfdir=/etc                           \
            --enable-namei-fileserver                   \
            --enable-bitmap-later                       \
            --with-krb5

# parallel build not reliable with multi-arch
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

# remove extra files that aren't need for krb5 use
rm $RPM_BUILD_ROOT/usr/bin/kpasswd
rm $RPM_BUILD_ROOT/usr/share/man/man1/kpasswd.1

# install kernel modules
mkdir -p $RPM_BUILD_ROOT/kernel/drv/amd64
cp $RPM_BUILD_ROOT/usr/lib/openafs/libafs64.nonfs.o $RPM_BUILD_ROOT/kernel/drv/amd64/afs
cp $RPM_BUILD_ROOT/usr/lib/openafs/libafs.nonfs.o $RPM_BUILD_ROOT/kernel/drv/afs

mkdir -p $RPM_BUILD_ROOT/etc/init.d
cp src/afsd/afs.rc.solaris.2.11 $RPM_BUILD_ROOT/etc/init.d/openafs

mkdir -p $RPM_BUILD_ROOT/etc/openafs
cp src/afsd/CellServDB $RPM_BUILD_ROOT/etc/openafs
echo "/afs:/usr/vice/cache:100000" > $RPM_BUILD_ROOT/etc/openafs/cacheinfo.sample
echo "openafs.org" > $RPM_BUILD_ROOT/etc/openafs/ThisCell.sample

mkdir -p $RPM_BUILD_ROOT/var/openafs/logs
mkdir -p $RPM_BUILD_ROOT/afs

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp openafs.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) /usr/bin
/usr/bin/*
%dir %attr (0755, root, bin) /usr/include
%dir %attr (0755, root, bin) /usr/include/openafs
/usr/include/openafs/*
%dir %attr (0755, root, bin) /usr/lib
/usr/lib/*
%defattr (0755, root, sys)
%dir %attr (0755, root, bin) /usr/sbin
/usr/sbin/*
%dir %attr (0755, root, sys) /usr/share
%dir %attr (0755, root, sys) /usr/share/openafs/C
/usr/share/openafs/C/*
/kernel/drv/afs
/kernel/drv/amd64/afs
/etc/init.d/openafs
%dir %attr (0755, root, sys) /etc/openafs
/etc/openafs/*
%defattr (-, root, bin)
%dir %attr (0755, root, bin) /usr/share/man
%dir %attr (0755, root, bin) /usr/share/man/man1
/usr/share/man/man1/*
%dir %attr (0755, root, bin) /usr/share/man/man5
/usr/share/man/man5/*
%dir %attr (0755, root, bin) /usr/share/man/man8
/usr/share/man/man8/*
%dir %attr (0755, root, sys) /var/openafs
%dir %attr (0755, root, sys) /var/openafs/logs
%dir %attr (0755, root, sys) /afs

%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/openafs.xml

%changelog
* Mon Jun 18 2012 - Logan Bruns <logan@gedanken.org>
- Fixed default path for krb5.conf (/etc/krb5.conf -> /etc/krb5/krb5.conf)
- Added missing buildrequires for math headers
* Sun May 27 2012 - Logan Bruns <logan@gedanken.org>
- Enabled multi-arch. Added 32 bit kernel module in addition to normal
  64 bit kernel module.
* Sun May 6 2012 - Logan Bruns <logan@gedanken.org>
- Increased the smf method start timeout.
* Sat Apr 28 2012 - Logan Bruns <logan@gedanken.org>
- Fixed some permissions and also changed it to no longer enable the service by default.
* Mon Apr 16 2012 Logan Bruns <logan@gedanken.org>
- Fixed some permissions and removed some unnecessary and conflicting files.
* Sun Apr 15 2012 Logan Bruns <logan@gedanken.org>
- Relocated some directories and moved package out of experimental
* Sat Mar 31 2012 Logan Bruns <logan@gedanken.org>
- Updated to 1.6.1
* Thu Mar 8 2012 Logan Bruns <logan@gedanken.org>
- Updated to 1.6.1pre4, added manifest, added ips name and relocated into standard directories
* Mon Nov 26 2007 Petr Sobotka <sobotkap@centrum.cz>
- Initial version
