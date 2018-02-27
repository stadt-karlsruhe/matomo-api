# Python wrapper for the Matomo (formerly Piwik) API

A simple, pythonic wrapper around [Matomo's API](https://developer.matomo.org/api-reference/):

    from matomo_api import Matomo

    m = Matomo('https://demo.matomo.org', idSite=7)
    statistics = m.VisitsSummary.getVisits(period='day', date='last10')

    for date, visits in statistics.items():
        print('{} visitors on {}'.format(visits, date))


## Installation

This package requires Python 3.3 or later.

    pip install git+https://github.com/stadt-karlsruhe/matomo-api.git


## Usage

First create an instance of `matomo_api.Matomo`:

    from matomo_api import Matomo

    m = Matomo('https://my-matomo-instance.com')

You can then call any [Matomo API function](https://developer.matomo.org/api-reference/)
via `m`. For example, to get the number of visitors to a site over the last 10 days via
the [`VisitsSummary.getVisits`](https://developer.matomo.org/api-reference/reporting-api#VisitsSummary)
function:

    visitors = m.VisitsSummary.getVisits(idSite=1, period='day', date='last10')

Results are returned as JSON. If the Matomo API returns an error then a
`matomo_api.MatomoException` is raised.

Parameters can also be set directly on the `Matomo` instance, they are then
used for all following API calls. This is especially handy for `idSite` (when
working with a single site) and `token_auth` (when targeting a private
instance):

    m = Matomo('https://my-matomo-instance.com', idSite=3, token_auth='XYZ')
    visitors = m.VisitsSummary.getVisits(period='day', date='last10')


## License

(c) 2018, Stadt Karlsruhe (www.karlsruhe.de)

Distributed under the MIT license, see the file `LICENSE` for details.

