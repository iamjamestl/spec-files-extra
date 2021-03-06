#
# spec file for package moovida-plugins-bad
#
# Copyright (c) 2008, 2010, Oracle and/or its affiliates. All rights reserved.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner yippi

%define OSR 12197:1.0.1

#
# bugdb: http://bugs.launchpad.net/moovida/+bug/
#

Name:              moovida-plugins-bad
License:           GPL v3
Vendor:            moovidia.com
Summary:           Bad plugins for Moovida
URL:               http://www.moovida.com/
Version:           1.0.9
Source:            http://www.moovida.com/media/public/%{name}-%{version}.tar.gz
# Refer to spec file to see reasons why we disable some plugins.
#date:2008-10-24 owner:yippi type:branding
Patch1:		   moovida-plugins-bad-01-rm-plugins.diff
#date:2009-03-19 owner:yippi type:bug bugzilla:345633
Patch2:            moovida-plugins-bad-02-exit.diff

# We remove the following plugins:
# - smbwin32, since it only works on the Windows platform
# - winremote, ditto
# - wmd, ditto
# - yesfm, since it is only available in Spain
# - avahi, since this plugin does not work for now
# - coherence, since we do not ship the coherence dependency
# - filtered_shares, since this plugin does not work for now
# - osso, ditto
# - dvd, ditto
# - daap, since we do not yet ship the PythonDAAP dependencies
# - ipod, since we do not ship the libgpod, python-gpod dependencies
# 
%description
The Moovida bad plugins set contains plugins known to be working well but with
code needing more QA (unittests, code reviews). However, these plugins are 
needed for Moovida to work.

%prep
%setup -q -n elisa-plugins-bad-%{version}
%patch1 -p1
%patch2 -p1

%build
python setup.py build_po
 
%install
python%{default_python_version} setup.py install --root=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/python%{default_python_version}/elisa/plugins/__init__.py
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{default_python_version}/elisa/plugins/__init__.pyc

# l10n source files
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{default_python_version}/[a-z]*-packages/elisa/plugins/[a-z]*/i18n/__init__.py
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{default_python_version}/[a-z]*-packages/elisa/plugins/[a-z]*/i18n/__init__.pyc
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{default_python_version}/[a-z]*-packages/elisa/plugins/[a-z]*/i18n/messages.pot
rm -f $RPM_BUILD_ROOT%{_libdir}/python%{default_python_version}/[a-z]*-packages/elisa/plugins/[a-z]*/i18n/[_a-zA-Z]*/LC_MESSAGES/*.po

# Move python dir to /usr/share/locale
for FROM_DIR in $RPM_BUILD_ROOT%{_libdir}/python%{default_python_version}/[a-z]*-packages/elisa/plugins/[a-z]*/i18n/[_a-zA-Z]*
do
  if [ ! -d $FROM_DIR/LC_MESSAGES ] ; then
    continue
  fi
  LANG_DIR=`basename $FROM_DIR`
  case $LANG_DIR in
  pt_BR) ;;
  *) LANG_DIR=`echo $LANG_DIR | awk -F_ '{print $1}'`;;
  esac
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/$LANG_DIR
  ( cd $FROM_DIR; tar cfp - LC_MESSAGES ) |\
  ( cd $RPM_BUILD_ROOT%{_datadir}/locale/$LANG_DIR; tar xfp - )
  /bin/rm -r $FROM_DIR/LC_MESSAGES
  rmdir $FROM_DIR
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{default_python_version}/vendor-packages/elisa
%{_libdir}/python%{default_python_version}/vendor-packages/elisa_plugin_*-nspkg.pth
%{_libdir}/python%{default_python_version}/vendor-packages/elisa_plugin_*.egg-info

%changelog
* Tue Dec 08 2009 Brian Cameron <brian.cameron@sun.com>
- Bump to 1.0.9.
* Wed Nov 04 2009 Brian Cameron <brian.cameron@sun.com>
- Bump to 1.0.8.
* Mon Nov 02 2009 Brian Cameron <brian.cameron@sun.com>
- Bump to 1.0.7.
* Mon Oct 12 2009 Brian Cameron <brian.cameron@sun.com>
- Now use %{default_python_version}.
* Wed Jul 15 2009 Brian Cameron <brian.cameron@sun.com>
- Created with version 1.0.5.
