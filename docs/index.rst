korexo_profile Python package documentation
=============================================================

This package contains Python code to load sonde profile CSV files produced
by the KorEXO sondes.

The source code is stored at `GitLab
<https://gitlab.com/dew-waterscience/korexo_profile>`_.

Contact Kent Inverarity for access to the GitLab site.

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

Sometimes, people open the raw file in Excel to view or edit it in some small
way and then save as a CSV. This seems innocuous, but completely changes
the format (and usually the encoding also - see below). 

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

I believe the sondes use UTF-16-LE by default. Most text editors do not use
this, so if someone has opened the file and then saved it, it likely will
have converted it to UTF-8 or Windows-1252.

The default behaviour is simplest:

.. code-block::

  >>> data = korexo_profile.read("example2.csv")

This is equivalent internally to:

.. code-block::

  >>> data = korexo_profile.read("example2.csv", encoding="utf-16", auto_revert_encoding="cp1252")

Because ``auto_revert_encoding`` is not False, the code will first check
whether example2.csv is UTF-16. If it is not, then the file will be loaded
using the value of ``auto_revert_encoding`` (``'cp1252'``). If it is UTF-16,
it will be loaded as such.

If you want the code to simply use the encoding you direct it to, set
``auto_revert_encoding=False``. This may result in messy errors and weird
behaviour.

Skip all that... just give me a complete spreadsheet.
-----------------------------------------------------

.. code-block::

  >>> data = korexo_profile.read("example1_full.csv")
  >>> df = korexo_profile.convert_datasets_to_df(data["datasets"])
  >>> df.head()
              datetime        date      time  time_sec    site  cond  water_depth  cond_nlf  do_sat  do_local  do_conc  orp_mv  press  sal_psu  spcond  tds    ph  ph_mv    temp  vert_pos  battery  cable_power  
  0 2019-11-12 08:40:30  2019-11-12  08:40:30       0.0  SQR100   9.1        0.002      11.5    98.0      97.4    10.02    11.8  0.002      0.0    11.4    7  7.59  -44.0  14.354     0.003     3.06         11.1 
  1 2019-11-12 08:40:31  2019-11-12  08:40:31       0.0  SQR100   9.0        0.002      11.5    98.0      97.5    10.02    12.2  0.002      0.0    11.4    7  7.59  -43.8  14.352     0.004     3.06         11.1 
  2 2019-11-12 08:40:32  2019-11-12  08:40:32       0.0  SQR100   9.0        0.002      11.5    98.1      97.6    10.03    11.0  0.002      0.0    11.3    7  7.59  -43.7  14.349     0.000     3.06         11.1 
  3 2019-11-12 08:40:33  2019-11-12  08:40:33       0.0  SQR100   9.0        0.002      11.5    98.6      98.1    10.09     8.7  0.003      0.0    11.3    7  7.61  -45.4  14.357     0.003     3.06         11.1 
  4 2019-11-12 08:40:34  2019-11-12  08:40:34       0.0  SQR100   9.1        0.002      11.5    99.3      98.8    10.16    -9.7  0.003      0.0    11.4    7  7.87  -59.5  14.420     0.001     3.06         11.1 

And let's say the depth to water was 5.15 m, so let's add that offset: 

.. code-block::

  >>> df["dtw"] = df.water_depth + 5.15
  >>> df.head()
              datetime        date      time  time_sec    site  cond  water_depth  cond_nlf  do_sat  do_local  do_conc  orp_mv  press  sal_psu  spcond  tds    ph  ph_mv    temp  vert_pos  battery  cable_power    dtw
  0 2019-11-12 08:40:30  2019-11-12  08:40:30       0.0  SQR100   9.1        0.002      11.5    98.0      97.4    10.02    11.8  0.002      0.0    11.4    7  7.59  -44.0  14.354     0.003     3.06         11.1  5.152
  1 2019-11-12 08:40:31  2019-11-12  08:40:31       0.0  SQR100   9.0        0.002      11.5    98.0      97.5    10.02    12.2  0.002      0.0    11.4    7  7.59  -43.8  14.352     0.004     3.06         11.1  5.152
  2 2019-11-12 08:40:32  2019-11-12  08:40:32       0.0  SQR100   9.0        0.002      11.5    98.1      97.6    10.03    11.0  0.002      0.0    11.3    7  7.59  -43.7  14.349     0.000     3.06         11.1  5.152
  3 2019-11-12 08:40:33  2019-11-12  08:40:33       0.0  SQR100   9.0        0.002      11.5    98.6      98.1    10.09     8.7  0.003      0.0    11.3    7  7.61  -45.4  14.357     0.003     3.06         11.1  5.152
  4 2019-11-12 08:40:34  2019-11-12  08:40:34       0.0  SQR100   9.1        0.002      11.5    99.3      98.8    10.16    -9.7  0.003      0.0    11.4    7  7.87  -59.5  14.420     0.001     3.06         11.1  5.152

Then re-index so the profile is at 5 cm intervals:

.. code-block::

  >>> df2 = korexo_profile.make_regularly_spaced(df, "dtw", step=0.05)
  >>> df2.head()
            time_sec         cond  water_depth     cond_nlf     do_sat   do_local   do_conc     orp_mv     press   sal_psu       spcond         tds        ph      ph_mv       temp  vert_pos  battery  cable_power
  dtw
  5.150000       0.0     9.533333     0.000000    11.500000  91.700000  91.200000  8.910000 -39.200000  0.001000  0.000000    11.366667    7.000000  8.390000 -89.133333  16.663667  0.001333     3.06         11.2
  5.202174       0.0  1203.097516     0.052174  1324.406211  92.240373  91.670186  8.264037 -42.380745  0.073963  0.660000  1313.976398  854.192547  8.364037 -88.661491  20.583807  0.419938     3.06         11.2
  5.254348       0.0  1220.579710     0.104348  1343.950483  91.725845  91.225845  8.212585 -41.203382  0.148539  0.670000  1333.350483  866.483092  8.305169 -85.658454  20.573034  0.694548     3.06         11.2
  5.306522       0.0  1225.072347     0.156522  1348.894872  91.595905  91.095905  8.199795 -40.589761  0.222054  0.670205  1338.192824  870.184295  8.289795 -84.583618  20.575123  0.807270     3.06         11.2
  5.358696       0.0  1225.987800     0.208696  1349.886039  91.582138  91.082138  8.199107 -40.555346  0.296185  0.670893  1339.177108  870.803774  8.289107 -84.528553  20.575536  0.811537     3.06         11.2

Development 
------------

An issue tracker is located at `GitLab
<https://gitlab.com/dew-waterscience/korexo_profile>`_.


The documentation is accessible on `GitLab
<https://dew-waterscience.gitlab.io/korexo_profile>`_ when you are signed in.

Contact Kent Inverarity for access to the GitLab site.

To build:

If necessary, create a new version with a git tag per setuptools-scm:

.. code-block::

  $ git log --oneline
  0ad38e0 (HEAD -> master) update everything
  13a8644 (tag: v0.2) update
  ab86ff2 (tag: v0.1) Initial commit
  $ git tag v0.3

Then the usual way with `pyc_wheel <https://pyc-wheel.readthedocs.io/en/stable/>`_:

.. code-block::
  
  $ python setup.py bdist_wheel

And to publish, the usual:

.. code-block::

  $ twine upload dist\korexo_profile-0.3-py3-none-any.whl
