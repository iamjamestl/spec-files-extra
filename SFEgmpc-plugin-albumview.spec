%include Solaris.inc
%define pluginname albumview
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
Summary:                gmpc-%{pluginname} - Draws all album covers
# Version e.g. 0.20.0
Version:                %{gmpcplugin.version}
 
BuildRequires: SFEgcc
Requires: SFEgccruntime

BuildRequires: SFEgmpc-devel
Requires: SFEgmpc

%description
http://gmpc.wikia.com/wiki/GMPC_PLUGIN_ALBUMVIEW

%prep
%gmpcplugin.prep
 
%build
%gmpcplugin.build
 
%install
%gmpcplugin.install

%clean
%gmpcplugin.clean

%files
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%{_libdir}/gmpc/plugins/*.so
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gmpc-%{pluginname}/icons/*


%changelog
* Wed Apr 25 2012 - Thomas Wagner
- add (Build)Requires: SUNWgcc(runtime)
* Tue Apr 24 2012 - Thomas Wagner
- bump to 0.20.0
- adjust %files new lib location, use variable for icons path
* Wed Oct  6 2010 - Alex Viskovatoff
- Update to 0.20.0, adding icon packaging
* Sun Sep 27 2009 - Thomas Wagner
- *new*
* Sat Feb 21 2009 - Thomas Wagner
- add (Build-)Requires: SFEgmpc(-devel) (moved from base-specs/gmpc-plugin.spec)
- removed %doc from %files (usually no docs contained in plugins)
* Sun Dec 02 2007 - Thomas Wagner
- rework into base-spec
- bump to 0.15.5.0
