'''
Hypothetical command-line tool for searching a
collection of files for one or more text patterns.
'''
import os
import argparse
import requests
import keys

parser = argparse.ArgumentParser(description='Sends logs to Datadog'
                                 ' from your command line.'
                                 ' Accepts a simple string or a text file.')

parser.add_argument('string')
parser.add_argument('--source', dest='source',
                    default='cli',
                    help='set the value of reserved attribute SOURCE.')
parser.add_argument('--service', dest='service',
                    default='cli',
                    help='set the value of reserved attribute SERVICE.')
parser.add_argument('--nodef', dest='nodefaults',
                    action='store_true',
                    help='remove the values set for SOURCE and SERVICE'
                    ' (including defaults)')
parser.add_argument('--host', dest='host',
                    help='set the value of reserved attribute HOST.')
parser.add_argument('-t', '--tags', dest='tags',
                    help='apply comma-separated list of tags.')
parser.add_argument('-e', '--env', dest='environment', metavar='ENV',
                    choices=['us', 'eu', 'staging', 'azure'],
                    default='us',
                    help='specify which Datadog org to send logs to.'
                    ' Possible values are: %(choices)s')
args = parser.parse_args()


def main():
    send_logs()


def send_logs():

    URL = construct_url()

    if os.path.exists(args.string):
        data = open(args.string)
        headers = {'Content-Type': 'text/plain'}
    else:
        data = args.string
        headers = {'Content-Type': 'application/json'}

    response = requests.post(URL, data, headers=headers)
    print(response.status_code)


def construct_url():

    if args.environment == 'eu':
        endpoint = keys.EU_ENDPOINT
        api_key = keys.DD_API_KEY_EU
    elif args.environment == 'staging':
        endpoint = keys.STAGING_ENDPOINT
        api_key = keys.DD_API_KEY_STAGING
    elif args.environment == 'azure':
        endpoint = keys.AZURE_ENDPOINT
        api_key = keys.DD_API_KEY_AZURE
    else:
        endpoint = keys.HTTP_ENDPOINT
        api_key = keys.DD_API_KEY

    parameters = get_parameters(api_key)

    URL = 'https://'+endpoint+'/v1/input/'+parameters
    return URL


def get_parameters(key):
    logparams = key

    if not args.nodefaults:
        logparams = logparams+'?ddsource='+args.source+'&service='+args.service
    else:
        logparams = logparams+'?'

    if args.host:
        logparams = logparams+'&host='+args.host

    if args.tags:
        logparams = logparams+'&ddtags='+args.tags

    return logparams


if __name__ == "__main__":
    main()
