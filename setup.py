from distutils.core import setup

setup(
    name='geohashlib',
    packages=['geohashlib'],
    version='0.1',
    description='Transform GeoJSON shape to a list of geohashes',
    author='Jerry Xu and Jonathan Johannemann',
    author_email='info@sstm2.com',
    url='https://github.com/sstm2/geohashlib',
    download_url='https://github.com/sstm2/geohashlib',
    keywords=['geohash', 'geo'],
    install_requires=[
        'python-geohash',
        'shapely',
        'geojson',
        'numpy',
    ],
    extras_requires={
        'dev': [
            'pytest>=3',
            'matplotlib',
        ]
    },
    classifiers=[],
)
