* conan을 이용해서 외부 라이브러리 들을 관리하고 있습니다
* python 3.6 이상 버전 설치
* pip install conan, conan 설치
* 프로젝트에서 conan을 관리하기 위해 ./conan 폴더 생성
* conan 프로필 생성(profile_debug & release)
* ./conan/conanfile.txt 생성
* root 폴더에서python setup.py 를 실행해서 lib 설치 & 프로젝트에 적용

* ./conan  폴더 안에서. 아래 명령어를 사용해 conan install
    * conan install . --profile:host=./profile_debug --profile:build=./profile_debug --output-folder=conanbuild/debug --build=missing
    * conan install . --profile:host=./profile_release --profile:build=./profile_release --output-folder=conanbuild/release --build=missing
* 프로젝트의 vcxproj 수정(conan_test.vcxproj) 
* 기존 <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" /> 위에 아래 코드를 2개를 담는다
* 아래와 같은 형태가 됨
    <Import Condition="'$(Configuration)' == 'Debug'" Project="conan\conanbuild\debug\conandeps.props" />
    <Import Condition="'$(Configuration)' == 'Release'" Project="conan\conanbuild\release\conandeps.props" />
    <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />