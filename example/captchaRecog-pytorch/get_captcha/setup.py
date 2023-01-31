from setuptools import setup, find_packages

setup(
    name='getcap',
    version='1.0.0',
    long_description=open('README.md', encoding='utf-8').read(),
    author='gaozhiyuan',
    packages=find_packages(),
    data_files=[
        ('getcap/data', ['getcap/data/background.png','getcap/data/DroidSansMono.ttf','getcap/data/shape.png'])
    ],
    zip_safe=False
)