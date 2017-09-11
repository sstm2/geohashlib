# geohashlib
Library of frequently used functions related to geohashes. Convert shapes to 
geohashes, geohashes back to shapes, and whatever else. This library relies 
on the ```python-geohash``` package by Hiroaki Kawai from [here](https://github.com/hkwi/python-geohash)

## Installing
```bash
pip install git+https://github.com/sstm2/geohashlib.git
```

## Getting Started
```python
In[1]: import geohashlib as g
In[2]: g.neighbors('dr5rustf')
Out[2]:
['dr5rust9',
 'dr5rustd',
 'dr5ruste',
 'dr5rustc',
 'dr5rustg',
 'dr5rusw1',
 'dr5rusw4',
 'dr5rusw5']
```
## Contributing

