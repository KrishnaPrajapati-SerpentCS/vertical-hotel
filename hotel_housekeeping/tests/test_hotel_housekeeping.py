# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo.tests import common
from datetime import datetime
import time


class TestHousekeeping(common.TransactionCase):

    def setUp(self):
        super(TestHousekeeping, self).setUp()
        self.housekeeping_obj = self.env['hotel.housekeeping']
        self.hotel_act_obj = self.env['hotel.housekeeping.activities']
        self.hotel_act_type_obj = self.env['hotel.housekeeping.activity.type']
        self.housekeeper = self.env.ref('base.user_root')
        self.inspector = self.env.ref('base.user_demo')
        self.act_type = self.env.\
            ref('hotel_housekeeping.hotel_housekeeping_activity_type_1')
        self.room = self.env.ref('hotel.hotel_room_0')

        cur_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.housekeeping = self.housekeeping_obj.\
            create({'current_date': time.strftime('%Y-%m-%d'),
                    'room_no': self.room.id,
                    'clean_type': 'daily',
                    'inspector': self.inspector.id,
                    'state': 'dirty',
                    'quality': 'excellent',
                    'inspect_date_time': cur_date,
                    })

        self.hotel_act_type = self.hotel_act_type_obj.\
            create({'name': 'Test Room Activity',
                    'activity_id': self.act_type.id,
                    })
        self.hotel_act_type.name_get()
        hotel_activity_type = self.hotel_act_type_obj.\
            name_search('Test Room Activity')
        self.assertEqual(len(hotel_activity_type), 1,
                         'Incorrect search number result for name_search')

    def test_action_set_to_dirty(self):
        self.housekeeping.action_set_to_dirty()

    def test_room_cancel(self):
        self.housekeeping.room_cancel()
        self.assertEqual(self.housekeeping.state == 'cancel', True)

    def test_room_done(self):
        self.housekeeping.room_done()
        self.assertEqual(self.housekeeping.state == 'done', True)

    def test_room_inspect(self):
        self.housekeeping.room_inspect()
        self.assertEqual(self.housekeeping.state == 'inspect', True)

    def test_room_clean(self):
        self.housekeeping.room_clean()
        self.assertEqual(self.housekeeping.state == 'clean', True)