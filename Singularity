BootStrap: yum
OSVersion: 7
MirrorURL: http://mirror.centos.org/centos-%{OSVERSION}/%{OSVERSION}/os/$basearch/
Include: yum

# If you want the updates (available at the bootstrap date) to be installed
# inside the container during the bootstrap instead of the General Availability
# point release (7.x) then uncomment the following line
#UpdateURL: http://mirror.centos.org/centos-%{OSVERSION}/%{OSVERSION}/updates/$basearch/


%runscript
    echo "This container provides a pipeline for identification pseudogenes in plant species"


%post
    echo "Hello from inside the container"
    yum -y install vim-minimal
    yum -y update
    yum -y groupinstall 'Development Tools'
    yum install -y libarchive-devel
    yum install -y git
    yum install -y  wget
    yum install -y unzip zip
    yum -y install epel-release
    yum -y install python-pip
    pip install pandas -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
    pip install biopython -i https://pypi.tuna.tsinghua.edu.cn/simple/ 

# Dependencies
#  git clone https://github.com/bjfupoplar/PlantPseudo.git
