korexo_profile Python package documentation
=============================================================

This package contains Python code to load sonde profile CSV files produced
by the KorEXO sondes.

.. contents:: :local:

How to use
----------------------

Example file:

.. literalinclude:: ../tests/example2.csv
  :encoding: utf-16

To read this file:

.. code-block:: 
   
   >>> import korexo_profile
   >>> data = korexo_profile.read("example2.csv")

This returns a dictionary with three keys:

.. code-block::

  >>> data.keys()
  dict_keys(['metadata', 'datasets', 'dataframe'])

Raw pandas dataframe
~~~~~~~~~~~~~~~~~~~~~~~~~~

The raw data is read into a pandas dataframe:

.. code-block::

  >>> df = data["dataframe"]
  >>> df.info()
  <class 'pandas.core.frame.DataFrame'>
  RangeIndex: 9 entries, 0 to 8
  Data columns (total 22 columns):
  #   Column               Non-Null Count  Dtype
  ---  ------               --------------  -----
  0   Date (MM/DD/YYYY)    9 non-null      object
  1   Time (HH:mm:ss)      9 non-null      object
  2   Time (Fract. Sec)    9 non-null      int64
  3   Site Name            9 non-null      object
  4   Cond µS/cm           9 non-null      int64
  5   Depth m              9 non-null      float64
  6   nLF Cond µS/cm       9 non-null      float64
  7   ODO % sat            9 non-null      float64
  8   ODO % local          9 non-null      float64
  9   ODO mg/L             9 non-null      float64
  10  ORP mV               9 non-null      float64
  11  Pressure psi a       9 non-null      float64
  12  Sal psu              9 non-null      int64
  13  SpCond µS/cm         9 non-null      float64
  14  TDS mg/L             9 non-null      int64
  15  pH                   9 non-null      float64
  16  pH mV                9 non-null      float64
  17  Temp °C              9 non-null      float64
  18  Vertical Position m  9 non-null      float64
  19  Battery V            9 non-null      float64
  20  Cable Pwr V          9 non-null      float64
  21  DTW                  1 non-null      float64
  dtypes: float64(15), int64(4), object(3)
  memory usage: 1.7+ KB
  >>> df.head()
    Date (MM/DD/YYYY) Time (HH:mm:ss)  Time (Fract. Sec) Site Name  Cond µS/cm  Depth m  nLF Cond µS/cm  ODO % sat  ...  TDS mg/L    pH  pH mV  Temp °C  Vertical Position m  Battery V  Cable Pwr V  DTW
  0        10/16/2020        15:49:33                  0    SQR097           3   -0.001             3.4      102.3  ...         2  9.23 -137.6   18.996               -0.002       3.13         11.4  4.2
  1        10/16/2020        15:49:34                  0    SQR097           3   -0.001             3.4      102.3  ...         2  9.23 -137.6   18.998               -0.001       3.13         11.4  NaN
  2        10/16/2020        15:49:35                  0    SQR097           3   -0.001             3.4      102.3  ...         2  9.23 -137.6   18.999               -0.001       3.13         11.4  NaN
  3        10/16/2020        15:49:36                  0    SQR097           3   -0.001             3.4      102.3  ...         2  9.23 -137.6   19.001               -0.001       3.13         11.4  NaN
  4        10/16/2020        15:49:37                  0    SQR097           3   -0.001             3.4      102.3  ...         2  9.23 -137.6   19.002               -0.001       3.13         11.4  NaN

  [5 rows x 22 columns]

Per dataset (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The information is also stored per-dataset, with some data-type conversions applied under the ``"datasets"`` key.
I would recommend using this in most cases. Each item is a dictionary with keys as shown below.

The Date, Time, and Site Name columns have the handy ``"median"`` key, while all others you'd be more interested
in the ``"data"`` key which contains a numpy ``ndarray`` with the data:

.. code-block::

  >>> data["datasets"][0]
  {'column': 'Date (MM/DD/YYYY)',
   'data': [datetime.date(2020, 10, 16),
            datetime.date(2020, 10, 16),
            datetime.date(2020, 10, 16),
            datetime.date(2020, 10, 16),
            datetime.date(2020, 10, 16),
            datetime.date(2020, 10, 16),
            datetime.date(2020, 10, 16),
            datetime.date(2020, 10, 16),
            datetime.date(2020, 10, 16)],
   'mean': <NA>,
   'median': datetime.date(2020, 10, 16),
   'name': 'Date',
   'sensor': '',
   'stdev': <NA>}
  >>> data["datasets"][1]
  {'column': 'Time (HH:mm:ss)',
   'data': array(['15:49:33', '15:49:34', '15:49:35', '15:49:36', '15:49:37',
         '15:49:38', '15:49:39', '15:49:40', '15:49:41'], dtype=object),
   'mean': <NA>,
   'median': '15:49:33',
   'name': 'Time',
   'sensor': '',
   'stdev': <NA>}
  >>> data["datasets"][9]
  {'column': 'ODO mg/L',
   'data': array([9.5 , 9.5 , 9.49, 9.49, 9.5 , 9.49, 9.49, 9.5 , 9.49]),
   'mean': 7.66,
   'median': 9.49,
   'name': 'ODO mg/L',
   'sensor': '19D101830',
   'stdev': 0.97}

Other metadata
~~~~~~~~~~~~~~~~~~~~~~~~

Raw file metadata is also available:

.. code-block::

   >>> data["metadata"]
   {'created_file': datetime.datetime(2021, 10, 8, 15, 53, 33, 328977),
    'created_info': '10/16/2020 6:21:53 AM,,,,,,,,,,,,,,,,,,,,',
    'header_line_no': 9,
    'means': [1172.5,
              0.605,
              1277.2,
              85.5,
              85.6,
              7.66,
              47.1,
              0.859,
              0.64,
              1268.1,
              824,
              <NA>,
              -126,
              20.679,
              0.812,
              3.13,
              11.4,
              nan],
    'modified_file': datetime.datetime(2021, 10, 8, 16, 5, 47, 429739),
    'params': ['Cond µS/cm',
                'Depth m',
                'nLF Cond µS/cm',
                'ODO % sat',
                'ODO % local',
                'ODO mg/L',
                'ORP mV',
                'Pressure psi a',
                'Sal psu',
                'SpCond µS/cm',
                'TDS mg/L',
                'pH',
                'pH mV',
                'Temp °C',
                'Vertical Position m',
                'Battery V',
                'Cable Pwr V',
                'DTW'],
    'sensors': ['19A103955',
                '19B104242',
                '19A103955',
                '19D101830',
                '19D101830',
                '19D101830',
                '19B105042',
                '19B104242',
                '19A103955',
                '19A103955',
                '19A103955',
                '19B105042',
                '19B105042',
                '19A103955',
                '19B104242',
                '19C000969',
                '19C000969',
                ''],
    'stdevs': [566.7,
                0.791,
                617.1,
                9.2,
                9.2,
                0.97,
                1.1,
                1.123,
                0.31,
                612.7,
                398,
                0.1,
                5.7,
                0.8,
                0.972,
                0,
                0,
                nan]}

Date formats
------------------------

I have found that the way the KorEXO sondes encode dates to be a little messy.
Note that the column header for the first column seems to encode the date
format: ``Date (MM/DD/YYYY)``. This is detected and used automatically by default.
However, I've seen some files produced where the date format is backwards, so
you can also choose to specify the appropriate format in Python datetime 
format specifiers:

For this example:

.. literalinclude:: ../tests/example1.csv
  :encoding: utf-16-le

The default automatic detection:

.. code-block:: 

  >>> data = korexo_profile.read("example1.csv", datefmt="auto")
  >>> data["datasets"][0]["median"]
  datetime.date(2019, 11, 12)

Specifying it directly should provide the same result:

.. code-block:: 

  >>> data = korexo_profile.read("example1.csv", datefmt="%m/%d/%Y")
  >>> data["datasets"][0]["median"]
  datetime.date(2019, 11, 12)

But in this case the true date is actually December 11th, which we can force:

.. code-block:: 

  >>> data = korexo_profile.read("example1.csv", datefmt="%d/%m/%Y")
  >>> data["datasets"][0]["median"]
  datetime.date(2019, 12, 11)

Beware encodings
--------------------

I believe the sondes use UTF-16-LE by default. Most text editors use UTF-8
and will convert files to the latter. Note then that ``korexo_profile`` assumes
UTF-16-LE so you will end up with an error. I have included a UTF-8 example
in the repository, so for example you would load it:

.. code-block::

  >>> data = korexo_profile.read("example2_utf8.csv", encoding="utf-8")