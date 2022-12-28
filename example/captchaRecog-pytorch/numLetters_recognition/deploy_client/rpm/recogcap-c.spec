%define name recogcap-c
%define version 1.0.0
%define unmangled_version 1.0.0
%define release 1

Summary: This is an AI tool for captcha recognition client.
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: UNKNOWN
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: UNKNOWN <gaozhiyuan>
Url: https://gitee.com/openeuler/ai-tools.git
BuildRequires: python3-setuptools
Requires: python3-requests

%description
This is an AI tool for captcha recognition client.

%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
/usr/bin/python3 setup-c.py build

%install
/usr/bin/python3 setup-c.py install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
