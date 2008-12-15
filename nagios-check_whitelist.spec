%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	Examine and manipulate SpamAssassin's auto-whitelist db
Name:		nagios-check_whitelist
Version:	0
Release:	%mkrel 5
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

The name of the file is specified after any options, as <dbfile>.
The default is <\$HOME/.spamassassin/auto-whitelist>.

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
