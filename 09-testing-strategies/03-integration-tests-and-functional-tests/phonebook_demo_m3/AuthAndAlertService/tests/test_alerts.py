from collections import defaultdict
from io import StringIO
from textwrap import dedent

from alerts import count_alerts


def test_count_clashes():
    clashes = StringIO(dedent("""\
    Bob with number 1234
    Bob with number 1234
    Bob with number 1234"""))

    alerts = count_alerts(clashes)

    assert alerts == {'Bob with number 1234': 3}