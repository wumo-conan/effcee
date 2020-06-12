import os
from conans import ConanFile, CMake, tools

class EffceeConan(ConanFile):
    name = "effcee"
    version = "2019.0"
    description = "Effcee is a C++ library for stateful pattern matching of strings, inspired by LLVM's FileCheck"
    url = "https://github.com/wumo-conan/effcee"
    homepage = "https://github.com/google/effcee/"
    license = "Apache-2.0"
    
    exports_sources = ["CMakeLists.txt", "CONAN_PKG__.patch"]
    generators = "cmake"
    
    settings = "os", "arch", "build_type", "compiler"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, "fPIC": True}
    
    _source_subfolder = "source_subfolder"
    no_copy_source = True
    
    def requirements(self):
        self.requires("re2/20200601")
        self.requires("gtest/1.10.0")
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
    
    def configure(self):
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, 11)
    
    def source(self):
        # https://github.com/glfw/glfw/tree/e0c77f71f90e3bb8495c5c88fb0fb054d71cf7fc
        sha256 = "d8acda17b0e8bfc36e44c159a3dbb7a8d1bff603a085125ee99a2d790ef0ed6b"
        tools.get("{}/archive/v{}.zip".format(self.homepage, self.version))
        extracted_folder = f"{self.name}-{self.version}"
        os.rename(extracted_folder, self._source_subfolder)
        tools.patch(base_path=self._source_subfolder, patch_file="CONAN_PKG__.patch")
    
    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["EFFCEE_BUILD_TESTING"] = False
        cmake.configure()
        return cmake
    
    def build(self):
        cmake = self.configure_cmake()
        cmake.build()
    
    def package(self):
        cmake = self.configure_cmake()
        cmake.install()
        # tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
    
    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "effcee"
        self.cpp_info.names["cmake_find_package_multi"] = "effcee"
        self.cpp_info.libs = tools.collect_libs(self)
