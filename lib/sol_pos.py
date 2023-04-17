import pvlib as pl
from datetime import datetime
from datetime import timedelta


def solarposition(tab, latitude, longitude, tz):

    """ Determine the position of the sun """

    time = [datetime.strptime(date, "%Y-%m-%d %H:%M:%S") - timedelta(hours=tz) for date in tab['TIMESTAMP']]

    pos = pl.solarposition.get_solarposition(time, latitude, longitude, altitude=90)

    del pos['apparent_zenith']
    del pos['apparent_elevation']
    del pos['equation_of_time']

    return pos
