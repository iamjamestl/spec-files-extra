#
# spec file for package SFEntfs-3g
#
#
# you will need FUSE see: http://www.opensolaris.org/os/project/fuse

#
# Note: Use GCC 3.4.3 on oi_151a/Solaris 11 Express <kmays>
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define SUNWlibfuse	%(/usr/bin/pkginfo -q SUNWlibfuse && echo 1 || echo 0)

Name:                    SFEntfs-3g
Summary:                 NTFS-3G Stable Read/Write Driver
Version:                 2011.10.9-RC
License:                 GPLv2
Source:			 http://tuxera.com/opensource/ntfs-3g_ntfsprogs-%{version}.tgz
Url:                     http://www.tuxera.com/community/ntfs-3g-download/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
%define _execprefix %{_prefix}

BuildRequires:	SUNWgnome-common-devel

%if %SUNWlibfuse
BuildRequires:	SUNWlibfuse
Requires:	SUNWfusefs
Requires:	SUNWlibfuse
%else
BuildRequires:	SFElibfuse
Requires:	SFEfusefs
Requires:	SFElibfuse
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%if %SUNWlibfuse
Requires:	SUNWlibfuse
%else
Requires:	SFElibfuse
%endif

%prep
%setup -q -n ntfs-3g_ntfsprogs-%{version}

cat <<_EOF > fstyp
#!/bin/sh
while [ -n "\$1" ];  do
        case "\$1" in
        -*)
                shift   
                ;;
        *)
                %{_bindir}/ntfs-3g.probe --readonly "\$1" >/dev/null 2>&1 && echo "ntfs-3g" && exit 0
                exit 1
                ;;
        esac
done
exit 1
_EOF

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%gcc_optflags"
export FUSE_MODULE_CFLAGS="-D_FILE_OFFSET_BITS=64 -I/usr/include/fuse"
export FUSE_MODULE_LIBS="-pthread -lfuse"

./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}                 \
	    --mandir=%{_mandir}                 \
            --sysconfdir=%{_sysconfdir}         \
	    --datadir=%{_datadir}               \
            --bindir=%{_bindir}                 \
            --includedir=%{_includedir}         \
            --exec-prefix=%{_execprefix}	\
	    --with-fuse=external

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -r $RPM_BUILD_ROOT%{_prefix}/sbin
mkdir -p $RPM_BUILD_ROOT%{_libdir}/fs/ntfs-3g
cp fstyp $RPM_BUILD_ROOT%{_libdir}/fs/ntfs-3g/fstyp
chmod 755 $RPM_BUILD_ROOT%{_libdir}/fs/ntfs-3g/fstyp
ln -s %{_bindir}/ntfs-3g $RPM_BUILD_ROOT%{_libdir}/fs/ntfs-3g/mount
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libntfs-3g.so*
%dir %attr (0755, root, sys) %{_libdir}/fs
%dir %attr (0755, root, sys) %{_libdir}/fs/ntfs-3g
%{_libdir}/fs/ntfs-3g/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*



%changelog
* Thu Nov 3 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 2011.10.9-RC
* Tue Sep 27 2011 - Alex Viskovatoff
- Build with gcc-3, as does not duild with gcc 4.6
* Thu Jul 07 2011 - Alex Viskovatoff
- Revert the previous change, so the package gets built
* Mon Jun 06 2011 - Ken Mays <kmays2000@gmail.com>
- Bump to 2011.4.12
* Tue Mar 22 2011 - Thomas Wagner
- Bump to 2011.1.15
* Sat Jun 19 2010 - Milan Jurik
- support SFEfusefs
* Fri Mar 26 2010 - Albert Lee <trisk@opensolaris.org>
- Bump to 2010.3.6
- Update URL, License
- Add mount helper
* Sun Jun 21 2009 - trisk@forkgnu.org
- Bump to 2009.4.4
* Tue Mar 24 2009 - andras.barna@gmail.com
- bump version
* Fri Aug 15 2008 - andras.barna@gmail.com
- new version: 1.2812 
* Wed Aug 06 2008 - andras.barna@gmail.com
- initial spec
