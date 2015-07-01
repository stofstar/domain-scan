import logging
from scanners import utils
import json
import os

##
# == pageload ==
#
# Evaluate page laod time information using Phantomas.
#
# If data exists for a domain from `inspect`, will use the
# previously detected "canonical" endpoint for a domain.
##

command = os.environ.get("PHANTOMAS_PATH", "phantomas")
init = None

def scan(domain, options):
    logging.debug("[%s][pageload]" % domain)

    # phantomas needs a URL, not just a domain.
    if not (domain.startswith('http://') or domain.startswith('https://')):

        # If we have data from inspect, use the canonical endpoint.
        inspection = utils.data_for(domain, "inspect")
        if inspection and inspection.get("canonical"):
            url = inspection.get("canonical")

        # Otherwise, well, whatever.
        else:
            url = 'http://' + domain
    else:
        url = domain

    # TODO: check cache first

    # We'll cache prettified JSON from the output.
    cache = utils.cache_path(domain, "pageload")

    logging.debug("\t %s %s" % (command, url))
    raw = utils.scan([command, url, "--reporter=json"])
    if not raw:
        logging.warn("No response from phantomas.")
        return None

    # It had better be JSON, which we can cache in prettified form.
    data = json.loads(raw)
    utils.write(utils.json_for(data), cache)

    # TODO: handle invalid response

    yield [data['metrics'][metric] for metric in interesting_metrics]


# All of the available metrics are listed here:
# https://www.npmjs.com/package/phantomas#metrics

# There are many other interesting metrics generated by Phantomas. For now,
# we'll just return some related to page load performance...
interesting_metrics = [
    'requests',
    'httpsRequests',
    'timeToFirstByte',
    'timeToLastByte',
    'httpTrafficCompleted',
    'domContentLoaded',
    'domComplete',
    'timeBackend',
    'timeFrontend',
]

headers = interesting_metrics
