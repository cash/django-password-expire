import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="django-password-expire",
    version="0.2",
    description="Django app for forcing password expiration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cash/django-password-expire",
    author="Cash Costello",
    author_email="cash.costello@gmail.com",
    license="BSD",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=["humanize"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
    ]
)
