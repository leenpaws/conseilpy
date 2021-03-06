from conseil.core import not_
from tests.mock_api import ConseilCase


class PredicatesTest(ConseilCase):

    def test_in(self):
        c = self.conseil.tezos.alphanet.accounts

        self.assertDictEqual({
            'field': 'account_id',
            'operation': 'in',
            'set': [1, 2, 3],
            'inverse': False
        }, c.account_id.in_(1, 2, 3))

        self.assertDictEqual({
            'field': 'account_id',
            'operation': 'in',
            'set': ['1', '2', '3'],
            'inverse': True
        }, c.account_id.notin_('1', '2', '3'))

        self.assertDictEqual({
            'field': 'account_id',
            'operation': 'isnull',
            'set': [],
            'inverse': False
        }, c.account_id.in_())

        self.assertDictEqual({
            'field': 'account_id',
            'operation': 'isnull',
            'set': [],
            'inverse': True
        }, c.account_id.notin_())

        self.assertDictEqual({
            'field': 'account_id',
            'operation': 'eq',
            'set': ['1'],
            'inverse': False
        }, c.account_id.in_('1'))

        self.assertDictEqual({
            'field': 'account_id',
            'operation': 'eq',
            'set': ['2'],
            'inverse': True
        }, c.account_id.notin_('2'))

    def test_between(self):
        c = self.conseil.tezos.alphanet.operations

        self.assertDictEqual({
            'field': 'timestamp',
            'operation': 'between',
            'set': [1, 3],
            'inverse': False
        }, c.timestamp.between(1, 3))

        self.assertDictEqual({
            'field': 'timestamp',
            'operation': 'between',
            'set': [1, 3],
            'inverse': True
        }, not_(c.timestamp.between(1, 3)))

    def test_like(self):
        c = self.conseil.tezos.alphanet.operations

        self.assertDictEqual({
            'field': 'destination',
            'operation': 'like',
            'set': ['tz'],
            'inverse': False
        }, c.destination.like('tz'))

        self.assertDictEqual({
            'field': 'destination',
            'operation': 'like',
            'set': ['tz'],
            'inverse': True
        }, c.destination.notlike('tz'))

    def test_lt(self):
        c = self.conseil.tezos.alphanet.operations

        self.assertDictEqual({
            'field': 'timestamp',
            'operation': 'lt',
            'set': [999999],
            'inverse': False
        }, c.timestamp < 999999)

        self.assertDictEqual({
            'field': 'timestamp',
            'operation': 'lt',
            'set': [0],
            'inverse': True
        }, c.timestamp >= 0)

    def test_gt(self):
        c = self.conseil.tezos.alphanet.operations

        self.assertDictEqual({
            'field': 'timestamp',
            'operation': 'gt',
            'set': [0],
            'inverse': False
        }, c.timestamp > 0)

        self.assertDictEqual({
            'field': 'timestamp',
            'operation': 'gt',
            'set': [999999],
            'inverse': True
        }, c.timestamp <= 999999)

    def test_eq(self):
        c = self.conseil.tezos.alphanet.operations

        self.assertDictEqual({
            'field': 'source',
            'operation': 'eq',
            'set': ['tz1'],
            'inverse': False
        }, c.source == 'tz1')

        self.assertDictEqual({
            'field': 'source',
            'operation': 'eq',
            'set': ['tz1'],
            'inverse': True
        }, c.source != 'tz1')

        self.assertDictEqual({
            'field': 'source',
            'operation': 'isnull',
            'set': [],
            'inverse': False
        }, c.source.is_(None))

        self.assertDictEqual({
            'field': 'source',
            'operation': 'isnull',
            'set': [],
            'inverse': True
        }, c.source.isnot(None))

    def test_startswith(self):
        c = self.conseil.tezos.alphanet.operations

        self.assertDictEqual({
            'field': 'source',
            'operation': 'startsWith',
            'set': ['KT1'],
            'inverse': False
        }, c.source.startswith('KT1'))

        self.assertDictEqual({
            'field': 'source',
            'operation': 'startsWith',
            'set': ['KT1'],
            'inverse': True
        }, not_(c.source.startswith('KT1')))

    def test_endswith(self):
        c = self.conseil.tezos.alphanet.operations

        self.assertDictEqual({
            'field': 'source',
            'operation': 'endsWith',
            'set': ['00'],
            'inverse': False
        }, c.source.endswith('00'))

        self.assertDictEqual({
            'field': 'source',
            'operation': 'endsWith',
            'set': ['00'],
            'inverse': True
        }, not_(c.source.endswith('00')))

    def test_filter(self):
        c = self.conseil.tezos.alphanet.operations

        query = c.query(c.destination, c.kind) \
            .filter(c.destination.startswith('KT1'),
                    c.kind == c.kind.transaction)

        self.assertEqual(2, len(query.payload()['predicates']))

    def test_filter_by(self):
        c = self.conseil.tezos.alphanet.accounts

        query = c.query(c.balance) \
            .filter_by(account_id='KT1abcd')

        self.assertDictEqual({
            'field': 'account_id',
            'operation': 'eq',
            'set': ['KT1abcd'],
            'inverse': False
        }, query.payload()['predicates'][0])
