
class BreadCrumbs:
    def __init__(self, start):
        self.start = start
        self.trail = []
        self.add_next(self.start)

    def add_next(self, page):
        self.trail.append(page)

    def previous(self):
        try:
            return self.trail.pop(len(self.trail) - 1)
        except IndexError:
            return None
