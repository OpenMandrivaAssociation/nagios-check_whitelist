%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	Examine and manipulate SpamAssassin's auto-whitelist db
Name:		nagios-check_whitelist
Version:	0
Release:	%mkrel 7
License:	Apache License
Group:		Networking/Other
URL:		http://www.apache.org/
Source0:	http://svn.apache.org/repos/asf/spamassassin/trunk/tools/check_whitelist
Source1:	check_whitelist.cfg
Requires:	nagios-plugins
BuildArch:  noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Check or clean a SpamAssassin auto-whitelist (AWL) database file.

%prep
%setup -q -c -T

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/nagios/plugins
install -m 755 %{SOURCE0} %{buildroot}%{_datadir}/nagios/plugins/

install -d -m 755 %{buildroot}%{_sysconfdir}/nagios/plugins.d
cat > %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_whitelist.cfg <<'EOF'
define command {
	command_name    check_whitelist
	command_line    %{_datadir}/nagios/plugins/check_whitelist --clean --min $ARG1$ $ARG2$
}
EOF

%if %mdkversion < 200900
%post
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%postun
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_whitelist.cfg
%{_datadir}/nagios/plugins/check_whitelist


%changelog
* Sat Dec 11 2010 Oden Eriksson <oeriksson@mandriva.com> 0-7mdv2011.0
+ Revision: 620470
- the mass rebuild of 2010.0 packages

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 0-6mdv2010.0
+ Revision: 440231
- rebuild

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - description is not a usage guide

* Mon Dec 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0-5mdv2009.1
+ Revision: 314658
- now a noarch package
- use a herein document for configuration
- reply on filetrigger for reloading nagios

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 0-4mdv2009.0
+ Revision: 253543
- rebuild

* Wed Feb 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0-2mdv2008.1
+ Revision: 163163
- whoops!, it can't be a noarch package :-)
- import nagios-check_whitelist


* Wed Feb 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0-1mdv2008.1
- initial Mandriva package
