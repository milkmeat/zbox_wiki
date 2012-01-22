#!/usr/bin/env python
import math

class Paginator(object):
    def __init__(self):
        self.current_offset = 0

        self.total = None
        self.limit = None
        self.url = None

    @property
    def count(self):
        """
        DON'T USE round build-in method, use math.ceil() instead.

        http://php.net/manual/en/function.round.php
        http://docs.python.org/library/math.html
        """
        return int(math.ceil(self.total * 1.0 / self.limit))

    @property
    def previous_page_url(self):
        return "%s?limit=%d&offset=%d" % (self.url, self.limit, self.current_offset - 1)

    @property
    def next_page_url(self):
        return "%s?limit=%d&offset=%d" % (self.url, self.limit, self.current_offset + 1)

    @property
    def has_previous_page(self):
        return self.current_offset > 0

    @property
    def has_next_page(self):
        return (self.current_offset * self.limit + self.limit) < self.total


if __name__ == "__main__":
    po = Paginator()
    
    po.total = 10
    po.limit = 3

    po.current_offset = 0
    assert po.count == 4
    assert po.has_previous_page == False
    assert po.has_next_page == True

    po.current_offset = 1
    assert po.count == 4
    assert po.has_previous_page == True
    assert po.has_next_page == True

    po.current_offset = 2
    assert po.count == 4
    assert po.has_previous_page == True
    assert po.has_next_page == True

    po.current_offset = 3
    assert po.count == 4
    assert po.has_previous_page == True
    assert po.has_next_page == False





