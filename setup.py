import os

os.environ['MACOSX_DEPLOYMENT_TARGET'] = '11.0'

try:
    from setuptools import setup, Extension
    from setuptools.command import build_ext as build_module
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command import build_ext as build_module

import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def build_swift():
    print("Building swift object files")
    os.system("mkdir -p build/swift")
    os.system("swiftc -parse-as-library -c src/metalpy.swift -I src -target arm64-apple-macos11 -o build/swift/metalpyswiftarm.a")
    os.system("swiftc -parse-as-library -c src/metalpy.swift -I src -target x86_64-apple-macos11 -o build/swift/metalpyswiftx64.a")
    os.system("lipo -create build/swift/metalpyswiftarm.a build/swift/metalpyswiftx64.a -o build/swift/metalpyswift.a")

class build(build_module.build_ext):
    def run(self):
        build_swift()
        build_module.build_ext.run(self)

setup(name="metalpy",
    version="0.2.4",
    author="Tejas Narayanan",
    author_email="tejasn100@gmail.com",
    description="A Python library to run Metal compute kernels on macOS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tnarayanan/metal-py",
    project_urls={
        "Issue Tracker": "https://github.com/tnarayanan/metal-py/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Environment :: GPU",
    ],
    python_requires=">=3.8",
    cmdclass = {'build_ext': build,},
    ext_modules=[Extension(
        'metalpy', 
        ['src/metalpy.c'], 
        extra_compile_args=["-mmacosx-version-min=11.0","-arch","arm64","-arch","x86_64","-Wno-unused-command-line-argument"],
        extra_link_args=["-mmacosx-version-min=11.0","-arch","arm64","-arch","x86_64","-Wno-unused-command-line-argument"],
        library_dirs=[".","/usr/lib","/usr/lib/swift"],
        libraries=["swiftFoundation","swiftMetal"],
        extra_objects=["build/swift/metalpyswift.a"])],
    scripts=["examples/metalpy-mandelbrot", 
             "examples/metalpy-measure",
             "examples/metalpy-raymarch",
             "examples/metalpy-pipe"]
    )