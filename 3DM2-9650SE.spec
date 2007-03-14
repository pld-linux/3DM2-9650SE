Summary:	3DM2 Management Utility
Summary(pl.UTF-8):	Narzędzie do zarządzania kontrolerami 3DM2
Name:		3DM2-9650SE
Version:	9.4.0.1
Release:	1
License:	commercial
Group:		Applications/System
Source0:	http://www.3ware.com/download/Escalade9650SE-Series/%{version}/3DM2-Linux-%{version}.tgz
# NoSource0-md5:	9505131021bafae54aa6d935202ce8e2
NoSource:	0
# NoSource1-md5:	a1f1cf93813592ea3499735ee598e673
Source1:	http://www.3ware.com/download/Escalade9650SE-Series/%{version}/%{version}_Release_Notes_Web.pdf
NoSource:	1
Source2:	3dm2-9650SE.init
URL:		http://www.3ware.com/products/raid_management.asp
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
3DM2 Management Utility for 3ware RAID controllers. It supports AMCC
3ware 9650SE controlers.

%description -l pl.UTF-8
Narzędzie 3DM2 do zarządzania kontrolerami RAID 3ware. Obsługuje
kontrolery z serii AMCC 3ware 9650SE.

%prep
%setup -q -c -n 3DM2
tar -xvzf 3dm-lnx.tgz
tar -xvzf 3dm-help.tgz
tar -xvzf 3dm-msg.tgz
cp %{SOURCE1} .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/3dm2
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_datadir}/3dm2/msg

cp -a en $RPM_BUILD_ROOT%{_datadir}/3dm2
install *_msg_en $RPM_BUILD_ROOT%{_datadir}/3dm2/msg
%ifarch %{ix86}
install 3dm2.x86 $RPM_BUILD_ROOT%{_sbindir}/3dm2
%endif
%ifarch %{x8664}
install 3dm2.x86_64 $RPM_BUILD_ROOT%{_sbindir}/3dm2
%endif
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/3dm2

cat > $RPM_BUILD_ROOT%{_sysconfdir}/3dm2/3dm2.conf << EOF
Port 888
EmailEnable 0
EmailSender [none]
EmailServer [none]
EmailRecipient [none]
EmailSeverity 3
ROpwd twOmwmsK8lKk2
ADMINpwd twOmwmsK8lKk2
RemoteAccess 0
Language 0
Logger 0
Refresh 5
BGRate 3333333333333333
MsgPath %{_datadir}/3dm2/msg
imgPath %{_datadir}/3dm2
Help %{_datadir}/3dm2
OEM 0
AutoLogout 0
CommandLog 1
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add 3dm2
%service 3dm2 restart "3DM2 Utility"

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del 3dm2
	%service 3dm2 stop
fi

%files
%defattr(644,root,root,755)
%doc version.3dm license.txt %{version}_Release_Notes_Web.pdf
%attr(755,root,root) %{_sbindir}/3dm2
%attr(754,root,root) /etc/rc.d/init.d/3dm2
%dir %{_sysconfdir}/3dm2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/3dm2/3dm2.conf
%{_datadir}/3dm2
