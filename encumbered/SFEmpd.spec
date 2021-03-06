#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#


# For the output section of ~/.mpdconf or /etc/mpd.conf try:
#
# audio_output {
#     type	"ao"
#     name      "libao audio device"
#     driver	"sun"
# }

%define build_encumbered %{?_without_encumbered:0}%{?!_without_encumbered:1}

%include Solaris.inc
%include packagenamemacros.inc

%define srcname mpd

Name:                SFEmpd
IPS_Package_Name:    media/mpd
Summary:             Daemon for remote access music playing & managing playlists
License:             GPLv2
SUNW_Copyright:	     mpd.copyright
Meta(info.upstream): Max Kellermann <max@duempel.org>
Version:             0.17.1
Source:              http://downloads.sourceforge.net/musicpd/%version/%srcname-%version.tar.bz2

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SFElibao-devel
BuildRequires: SFElibsamplerate-devel
BuildRequires: SUNWogg-vorbis-devel
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SUNWflac-devel
BuildRequires: SFElibshout
BuildRequires: SFElibcdio
BuildRequires: %{pnm_buildrequires_SUNWsqlite3}
BuildRequires: SUNWglib2
BuildRequires: SUNWlibsndfile
BuildRequires: SUNWcurl
#TODO# BuildRequires: SFElibpulse-devel
BuildRequires: SUNWavahi-bridge-dsd-devel
## MPD INSTALL file says AO "should be used only if there is no native plugin
## available or if the native plugin doesn't work."
Requires: SFElibao
Requires: SFElibsamplerate
Requires: SUNWogg-vorbis
Requires: SUNWgnome-audio
Requires: SUNWflac
Requires: SFElibshout
Requires: SFElibcdio
Requires: %{pnm_requires_SUNWsqlite3}
Requires: SUNWglib2
Requires: SUNWlibsndfile
Requires: SUNWcurl
#TODO# Requires: SFElibpulse
Requires: SUNWavahi-bridge-dsd
%if %build_encumbered
BuildRequires: SFElibmpcdec-devel
BuildRequires: SFEmpg123-devel
BuildRequires: SFEfaad2-devel
BuildRequires: SFElame-devel
BuildRequires: SFEtwolame-devel
# libid3tag is not encumbered, but it is not used by flac or ogg
BuildRequires: SFElibid3tag-devel
Requires: SFElibmpcdec
Requires: SFEfaad2
Requires: SFElame
Requires: SFEtwolame
Requires: SFEmpg123
Requires: SFElibid3tag
%endif


%description
Music Daemon to play common audio fileformats to audio devices or 
audio-networks. 
Uses a database to store indexes (mp3-tags,...) and supports Playlists.
Controlled via Network by SFEgmpc, SFEmpc, SFEncmpc, pitchfork and others.
Output might go to local Solaris Audio-Hardware, Streams with SFEicecast,
auto-network SFEpulseaudio ( via pulseaudio, libao (sun|pulse) ).


%prep
%setup -q -n %srcname-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -D_XOPEN_SOURCE -D_XOPEN_SOURCE_EXTENDED=1 -D__EXTENSIONS__"
export LDFLAGS="%_ldflags"

sed -i -e 's,#! */bin/sh,#! /usr/bin/bash,' configure 

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
    	    --enable-ao          \
	    --enable-iso9660     \
	    --enable-shout       \
            --disable-alsa       \
            --disable-ffmpeg     \
            --disable-mad        \
%if %build_encumbered
            --enable-mpg123      \
%else
            --disable-mpg123     \
            --disable-aac        \
            --disable-mpc        \
            --disable-lame-encoder \
            --disable-twolame-encoder \
%endif
#optional:
            # --with-zeroconf=no   \
            # --enable-pulse

# Be modern and use libxnet instead of libsocket
sed 's/-lsocket -lnsl/-lxnet/' Makefile > Makefile.xnet
mv Makefile.xnet Makefile

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin; export PATH' ;
  echo 'retval=0';
  echo '[ -f /etc/mpd.conf ] || cp -p $PKG_INSTALL_ROOT%{_datadir}/doc/mpd/mpdconf.example $PKG_INSTALL_ROOT%{_sysconfdir}/mpd.conf'
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/mpd
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/mpd.1
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/mpd.conf.5
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Thu Aug 19 2012 - Thomas Wagner
- bump to 0.17.1
- make configure use bash
* Thu Jul  5 2012 - Thomas Wagner
- bump to 0.17, changed download URL
- change to (Build)Requires to %{pnm_buildrequires_SUNWsqlite3}, %include packagenamacros.inc
* Fri Jun 22 2012 - Logan Bruns <logan@gedanken.org>
- added ips package name.
* Wed Oct 19 2011 - Alex Viskovotoff
- Use mpg123 instead of libmad for mp3s, since libmad is for integer-only CPUs
* Mon Aug  8 2011 - Alex Viskovatoff
- Add missing (build) dependencies
* Mon Jul 18 2011 - Alex Viskovatoff
- ffmpeg currently breaks build, so disable it
* Mon May 16 2011 - Alex Viskovatoff
- Add missing dependency; fix setting of build_encumbered
* Tue Apr 12 2011 - Alex Viskovatoff
- Bump to 0.16.2; add --without-encumbered option
* Tue Jan 18 2011 - Alex Viskovatoff
- Update to 0.16.1; use libxnet
* Sun Oct  3 2010 - Alex Viskovatoff
- Bump to 0.15.12; use gmake.
- mpd does not use id3lib (only faad2 does): remove the dependency.
* Thu Nov 19 2009 - oliver.mauras@gmail.com
- Version bump to 0.15.6
* Thu Jul 30 2009 - oliver.mauras@gmail.com
- Remove libMAD fix as libMAD spec fixed in r1997
* Wed Jul 29 2009 - oliver.mauras@gmail.com
- Small fix to the srcname declaration
* Tue Jul 28 2009 - oliver.mauras@gmail.com
- Version bump to 0.15.1
- Add realname variable
- No problems found with libsamplerate so reactivated it
* Sun Mar 15 2009 - oliver.mauras@gmail.com 
- Version bump
- Fix LibMAD detection
* Sat Dec 20 2008 - Thomas Wagner
- add nice and clean conditional (Build-)Requires: %if %SUNWid3lib ... %else ... SFEid3lib(-devel)
* Wed Nov 28 2007 - Thomas Wagner
- add --disable-lsr, remove (Build-)Requires SFElibsamplerate(-devel) (maybe cause for skipping music every few seconds)
- comment out --enable-pulse to not require pulseaudio
- comment out --*-zeroconf   to not require avahi/bonjour/zeroconf (should be included if it's present on the build-system, pending final solution - suggestions welcome)
- quick fix to "empty struct" when --disable-lsr is used (patch5) (remove patch5 if change is upstream)
* Sun Nov 18 2007 Thomas Wagner
- (Build)Requires: SUNWavahi-bridge-dsd(-devel)
  since parts of avahi interface made it into Nevada :-)
  if you have problems witch avahi/zeroconf, change ./configure to --with-zeroconf=no
* Sun Nov 18 2007 Thomas Wagner
- --disable-alsa (at the moment we use libao)
- (Build)Requires SFElibsamplerate(-devel)
* Tue Sep 04 2007 Thomas Wagner
- add description
- add libao example to mpd.conf (sun|pulse)
- enable missed patch3
- add more configexamples see share/doc/mpd/mpdconf.example if you are upgrading
  pulseaudio native output, libao driver "sun" or "pulse", icecast streaming (second example)
* Mon May 28 2007 Thomas Wagner
- bump to 0.13.0
- --enable-flac --enable-oggflac
  mpd now compiles with newer flac versions
- --enable-shout for buffered streaming to the net in ogg format
- add depency SFElibshout(-devel)
- if SFEavahi is present, mpd resources will be announced with
  zeroconf/avahi/mDNS broadcasts
- patch3: make id3_charset in mpdconf.example default to UTF-8
  NOTE: If files with special characters in id3_tags are missing in your
  database, then update your existing /etc/mpd.conf|~/.mpdconf to set
      id3v1_encoding  "UTF-8"
  and recreate the db (mpd --create-db).
- removed wrong export PKG_CONFIG=/usr/lib/pkgconfig
* May 17 2007 - Thomas Wagner
- --enable-shout - you need gcc to have configure detect shout libs
- added dependcies SFElibshout(-devel)
* Thu Apr 26 2007 - Thomas Wagner
- --disable-flac, --disable-oggflac
  mpd possibly has to be updated to reflect new libFLAC includes
  does not compile with libflac from vermillion_64 (sorry, 62 was a typo)
  you may enable *flac if using oder versions of libFLAC
* Thu Apr 26 2007 - Thomas Wagner
- make filesystem_charset in mpdconf.example default to UTF-8
  NOTE: If directories/files with UTF-8 names missing in the 
  database, then update your existing /etc/mpd.conf|~/.mpd.conf 
  and recreate the db (mpd --create-db).
  does not compile with libflac from vermillion_62
* Wed Apr 04 2007 - Thomas Wagner
- missing " in patch to mpdconf.example 
* Wed Apr 04 2007 - Thomas Wagner
- bump to 0.12.2
- added dependencies
- modified configuration note to name /etc/mpd.conf
- copy patched mdconf.example to /etc/mpd.conf
- re-add id3 tags (untested)
* Mon Nov 06 2006 - Eric Boutilier
- Fix attributes
* Tue Sep 26 2006 - Eric Boutilier
- Initial spec
