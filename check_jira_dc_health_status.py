#!/usr/bin/python
# Checks the statuses of various health check attributes for Jira
# For Atlassian Docs see https://confluence.atlassian.com/jirakb/how-to-retrieve-health-check-results-using-rest-api-867195158.html
# Example Usage (must be run as 'nagios' user):
# ./check_jira_health_status -u https://jira/

import argparse
import json
import os
import requests
from nagios_check import NagiosCheck

def get_args():
    parser = argparse.ArgumentParser(description='Retrieves the statuses of various health check attributes for Jira', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--url',
                        help='Jira Base URL',
                        default='https://jira
                        
                        
                        
                        
                        
                        
                        ')
    args = parser.parse_args()
    return args


def get_jira_pw(file):
    credential_lines  = open(file).read().strip()
    for line in credential_lines.split('\n'):
        try:
            p, v = line.split(':')
        except:
            p = 'invalid.parameter'
        if p == 'password':
            return v.strip('"')
    return False


def do_check(args, check):
    jira_admin_user = 'jira-admin'
    jira_admin_pw = False
    # Configuration file managed by the jira_dc role in ansible
    jira_dc_cfg = '/home/nagios/.check_jira_dc.cfg'

    # We don't care about getting alerts on these health checks
    excluded_statuses = ['End of Life', 'Application links'] 

    if os.path.exists(jira_dc_cfg):
        jira_admin_pw = get_jira_pw(jira_dc_cfg)
        if jira_admin_pw:
            with requests.session() as s:
                health_check_path = '/rest/troubleshooting/1.0/check'
                headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

                try:
                    s.auth = (jira_admin_user, jira_admin_pw)
                    response = s.get(args.url + health_check_path, headers=headers)
                    statuses = response.json()['statuses']
                except:
                    check.unkn('HTTP_%d: Unsuccessful GET request to %s' % (response.status_code, args.url + health_check_path))
                    check.output()
                    return

                if response.status_code != 200:
                    check.unkn('HTTP_%d: Unsuccessful request to %s' % (response.status_code, args.url + healh_check_path))
                    check.output()
                    return

                def get_unhealthy(status):
                    return not status['healthy'] and status['name'] not in excluded_statuses

                unhealthy = filter(get_unhealthy, statuses)

                if len(unhealthy) == 0:
                    check.ok('All Health Checks PASSED')
                    check.output()
                    return
                else:
                    unhealthy_output = ''
                    for status in unhealthy:
                        # status checks with tag: "Cluster" don't have a failureReason key
                        if status ['tag'] == 'Cluster':
                            unhealthy_output += status['name'] + ': (No Failure Reason)\n'
                        else:
                            unhealthy_output += status['name'] + ': ' + status['failureReason'] + '\n'
                    check.crit(unhealthy_output)
                    check.output()
                    return
    else:
        check.crit('Jira Admin Password File (%s) not found' % jira_dc_cfg)
        check.output()
        return


def main():
    check = NagiosCheck('Check Jira Health Status')
    args = get_args()
    do_check(args, check)


if __name__ == '__main__':
    main()
