# TODO: review security issues
%define		mod_name	ntlm
%define 	apxs		/usr/sbin/apxs
Summary:	This is the NTLM authentication module for Apache
Summary(pl):	Modu³ uwierzytelnienia NTLM dla Apache
Name:		apache-mod_%{mod_name}
Version:	0.1
Release:	0.1
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/modntlm/mod_%{mod_name}2-%{version}.tgz
# Source0-md5:	8abe4f235af6825f723412e187cac96b
#Patch0:	%{name}-security.patch
URL:		http://modntlm.sourceforge.net/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that allows you to
authenticate HTTP clients using samba or windows-like server (using
NTLM protocol).

%description -l pl
To jest modu³ uwierzytelnienia dla Apache pozwalaj±cy na
uwierzytelnianie klientów HTTP poprzez sambê lub serwer na Windows (z
u¿yciem protoko³u NTLM).

%prep
%setup -q -n mod_%{mod_name}2-%{version}
#%patch -p1

%build
%{__make} APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
echo 'LoadModule %{mod_name}_module modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%preun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
