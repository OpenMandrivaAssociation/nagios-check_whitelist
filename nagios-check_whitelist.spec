%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	Examine and manipulate SpamAssassin's auto-whitelist db
Name:		nagios-check_whitelist
Version:	0
Release:	%mkrel 4
License:	Apache License
Group:		Networking/Other
URL:		http://www.apache.org/
Source0:	http://svn.apache.org/repos/asf/spamassassin/trunk/tools/check_whitelist
Source1:	check_whitelist.cfg
Requires:	nagios
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
Check or clean a SpamAssassin auto-whitelist (AWL) database file.

The name of the file is specified after any options, as <dbfile>.
The default is <\$HOME/.spamassassin/auto-whitelist>.

%prep

%setup -q -c -T

cp %{SOURCE0} check_whitelist
cp %{SOURCE1} check_whitelist.cfg

perl -pi -e "s|_LIBDIR_|%{_libdir}|g" *.cfg

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/nagios/plugins.d
install -d %{buildroot}%{_libdir}/nagios/plugins

install -m0755 check_whitelist %{buildroot}%{_libdir}/nagios/plugins/
install -m0644 *.cfg %{buildroot}%{_sysconfdir}/nagios/plugins.d/

%post
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%postun
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_whitelist.cfg
%attr(0755,root,root) %{_libdir}/nagios/plugins/check_whitelist

