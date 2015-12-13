# Copyright (c) 2015 Louis Taylor <louis@kragniz.eu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from collections import namedtuple
import datetime

import icalendar
import yaml


Event = namedtuple('Event', ['name', 'description'])


class Week(object):
    def __init__(self, week_data):
        self.date = list(week_data)[0]
        items = week_data.get(self.date)
        self.events = []

        for event in items:
            name = list(event.keys())[0]
            description = event.get(name).strip()
            self.events.append(Event(name, description))


def make_events(week):
    events = []
    for event_data in week.events:
        event = icalendar.Event()
        event.add('summary', event_data.name)
        event.add('description', event_data.description)
        event.add('dtstart', week.date)
        event.add('duration', datetime.timedelta(days=4))

        events.append(event)
    return events


def make_ical(schedule_content):
    cal = icalendar.Calendar()
    cal.add('prodid', '-//OpenStack release-schedule-generator//mxm.dk//')
    cal.add('version', '2.0')

    for cycle in schedule_content:
        for name, events in cycle.items():
            for week in events:
                for calendar_entry in make_events(Week(week)):
                    cal.add_component(calendar_entry)
    return cal


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('schedule')
    args = parser.parse_args()

    with open(args.schedule) as f:
        content = yaml.load(f)

    cal = make_ical(content.get('schedule'))

    with open('openstack-release-schedule.ics', 'wb') as f:
        f.write(cal.to_ical())
