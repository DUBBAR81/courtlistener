# This software and any associated files are copyright 2010 Brian Carver and
# Michael Lissner.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# imports of local settings and views
from alert import settings
from alert.alertSystem.models import PACER_CODES
from alert.alertSystem.views import *
from alert.alertSystem.sitemap import DocumentSitemap
from alert.contact.views import *
from alert.feeds.views import *
from alert.pinger.views import *
from alert.search.views import *
from alert.userHandling.views import *


# needed to make urls work
from django.conf.urls.defaults import *

# for the flatfiles in the sitemap
from django.contrib.sitemaps import FlatPageSitemap
from django.contrib.auth.views import login as signIn, logout as signOut,\
    password_reset, password_reset_done, password_reset_confirm,\
    password_reset_complete

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

sitemaps = {
    "Opinion": DocumentSitemap,
    "Flatfiles": FlatPageSitemap,
}

# creates a list of the first element of the choices variable for the courts field
pacer_codes = []
for code in PACER_CODES:
    pacer_codes.append(code[0])

urlpatterns = patterns('',
    # Admin docs and site
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    # Court listing pages
    (r'^opinions/(' + "|".join(pacer_codes) + '|all)/$', viewDocumentListByCourt),

    # Display a case
    url(r'^(' + "|".join(pacer_codes) + ')/(.*)/$', viewCases, name="viewCases"),

    # Contact us pages
    (r'^contact/$', contact),
    (r'^contact/thanks/$', thanks),

    # Various sign in/out etc. functions as provided by django
    url(r'^sign-in/$', signIn, name="sign-in"),
    (r'^sign-out/$', signOut),

    # Homepage and favicon
    (r'^$', home),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/media/images/ico/favicon.ico'}),

    # Settings pages
    (r'^profile/settings/$', viewSettings),
    (r'^profile/alerts/$', viewAlerts),
    (r'^profile/password/change/$', password_change),
    (r'^profile/delete/$', deleteProfile),
    (r'^profile/delete/done/$', deleteProfileDone),
    url(r'^register/$', register, name="register"),
    (r'^register/success/$', registerSuccess),

    #Reset password pages
    (r'^reset-password/$', password_reset),
    (r'^reset-password/instructions-sent/$', password_reset_done),
    (r'^confirm-password/(?P<uidb36>.*)/(?P<token>.*)/$', password_reset_confirm, {'post_reset_redirect': '/reset-password/complete/'}),
    (r'^reset-password/complete/$', signIn, {'template_name': 'registration/password_reset_complete.html'}),

    # Alert/search pages
    # These URLs support either GET requests or things like /alert/preview/searchterm.
    #url(r'^(alert/preview)/$', showResults, name="alertResults"),
    url(r'^search/results/$', showResults, name="searchResults"),
    (r'^search/$', showResults), #for the URL hackers in the crowd
    (r'^alert/edit/(\d{1,6})/$', editAlert),
    (r'^alert/delete/(\d{1,6})/$', deleteAlert),
    (r'^alert/delete/confirm/(\d{1,6})/$', deleteAlertConfirm),
    (r'^tools/$', toolsPage),

    # Feeds
    (r'^feed/(search)/$', searchFeed()), #lacks URL capturing b/c it will use GET queries.
    (r'^feed/court/all/$', allCourtsFeed()),
    (r'^feed/court/(?P<court>' + '|'.join(pacer_codes) + ')/$', courtFeed()),

    # SEO-related stuff
    (r'^y_key_6de7ece99e1672f2.html$', validateForYahoo),
    (r'^LiveSearchSiteAuth.xml$', validateForBing),
    # Sitemap generator
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps}),
    #(r'^robots.txt$', robots), # removed for lack of need.
)

# if it's not the production site, serve the static files this way.
if settings.DEVELOPMENT:
    urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/mlissner/Documents/Cal/FinalProject/alert/assets/media',
        'show_indexes': True}),
    (r'^500/$', 'django.views.generic.simple.direct_to_template',
        {'template': '500.html'}),
    (r'^404/$', 'django.views.generic.simple.direct_to_template',
        {'template': '404.html'}),
)
