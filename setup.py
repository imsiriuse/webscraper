import setuptools

if __name__ == "__main__":
    setuptools.setup(
        name="webscraper",
        packages=setuptools.find_namespace_packages(where='src'),
        package_dir={'': 'src'},
    )