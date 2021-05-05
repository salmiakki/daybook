import datetime
from textwrap import dedent

from daybook.daybook import add_dateline


def test_add_dateline():
    text_without_current_date = dedent(
        """\
        * a link
        * another link
        """
    )
    expected_text = dedent(
        """\
        * a link
        * another link
        
        ## 2021-04-14, Wednesday
        
        """
    )
    assert add_dateline(text_without_current_date, date=datetime.date(2021, 4, 14)) == expected_text
