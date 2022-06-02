'''
Command-line tool for sending logs
to Datadog with arguments for different environments
and reserved attribute settings.
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

    env = get_env()
    parameters = get_parameters()

    URL = 'https://'+env['endpoint']+'/api/v2/logs/'+parameters

    headers = {'DD-API-KEY': env['api_key']}

    if os.path.exists(args.string):
        data = open(args.string)
        headers.update({'Content-Type': 'text/plain'})
    else:
        data = args.string
        headers.update({'Content-Type': 'application/json'})

    response = requests.post(URL, data, headers=headers)
    print(response.status_code)


def get_env():

    env = {}

    if args.environment == 'eu':
        env.update({
            'endpoint': keys.EU_ENDPOINT,
            'api_key': keys.DD_API_KEY_EU
        })
    elif args.environment == 'staging':
        env.update({
            'endpoint': keys.STAGING_ENDPOINT,
            'api_key': keys.DD_API_KEY_STAGING
        })
    elif args.environment == 'azure':
        env.update({
            'endpoint': keys.AZURE_ENDPOINT,
            'api_key': keys.DD_API_KEY_AZURE
        })
    else:
        env.update({
            'endpoint': keys.HTTP_ENDPOINT,
            'api_key': keys.DD_API_KEY
        })

    return env


def get_parameters():

    if not args.nodefaults:
        parameters = '?ddsource='+args.source+'&service='+args.service
    else:
        parameters = '?'

    if args.host:
        parameters = parameters+'&host='+args.host

    if args.tags:
        parameters = parameters+'&ddtags='+args.tags

    return parameters


if __name__ == "__main__":
    main()
