#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# - runtime Requires if any
%define		kdeframever	6.2
%define		qtver		5.15.2
%define		kfname		karchive

Summary:	Reading, creating, and manipulating file archives
Name:		kf6-%{kfname}
Version:	6.2.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	8877110a5b99432ea52fc292590bfb1c
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	bzip2-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	qt6-linguist
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
Obsoletes:	kf5-%{kfname} < %{version}
Requires:	Qt6Core >= %{qtver}
Requires:	kf6-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KArchive provides classes for easy reading, creation and manipulation
of "archive" formats like ZIP and TAR.

If also provides transparent compression and decompression of data,
like the GZip format, via a subclass of QIODevice.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Obsoletes:	kf5-%{kfname}-devel < %{version}
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core-devel >= %{qtver}
Requires:	cmake >= 3.16

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname} --all-name --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}.lang
%defattr(644,root,root,755)
%doc AUTHORS README.md
%ghost %{_libdir}/libKF6Archive.so.6
%attr(755,root,root) %{_libdir}/libKF6Archive.so.*.*
%config(noreplace) %verify(not md5 mtime size) %{_datadir}/qlogging-categories6/karchive.categories
%{_datadir}/qlogging-categories6/karchive.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KArchive
%{_libdir}/libKF6Archive.so
%{_libdir}/cmake/KF6Archive
