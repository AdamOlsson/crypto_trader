

class Window:
    def __init__(self, size):
        self.size = size
        self.window = []
        self._is_full = False
        self.local_min = self.local_max = 0
    
    def add(self, point):
        if len(self.window) < self.size:
            self.window.append(point)
            self._is_full = len(self.window) == self.size
            # set first point to be local max and min
            if len(self.window) == 1:
                self.local_min = self.local_max = point
        else:
            del self.window[0]
            self.window.append(point)

        self.local_min = min(point, self.local_min)
        self.local_max = max(point, self.local_max)

    def __len__(self):
        return len(self.window)

    def __getitem__(self, i):
        return self.window[i]
        
    def is_full(self):
        return self._is_full


if __name__ == '__main__':
    def test_fifo_assert_size_stay_at_max():
        size = 3
        window = Window(size)

        window.add(0)
        window.add(1)
        window.add(2)
        window.add(3)
        window.add(3)

        assert(len(window) == size)

    def test_fifo_property_first_pop():
        size = 5
        window = Window(size)

        window.add(0)
        window.add(1)
        window.add(2)
        window.add(3)
        window.add(4)
        window.add(5)

        assert(window[0] == 1)
        assert(window[1] == 2)
        assert(window[2] == 3)
        assert(window[3] == 4)
        assert(window[4] == 5)

    def test_fifo_propery():
        size = 5
        window = Window(size)

        window.add(0)
        window.add(1)
        window.add(2)
        window.add(3)
        window.add(4)

        assert(window[0] == 0)
        assert(window[1] == 1)
        assert(window[2] == 2)
        assert(window[3] == 3)
        assert(window[4] == 4)


    def test_fill_window_should_return_false():
        size = 5
        window = Window(size)

        window.add(1)
        window.add(2)
        window.add(3)
        window.add(4)

        assert(not window.is_full)


    def test_fill_window_should_return_true():
        size = 5
        window = Window(size)

        window.add(1)
        window.add(2)
        window.add(3)
        window.add(4)
        window.add(5)

        assert(window.is_full)


    def run_testsuite():
        def run_test(function):
            function()
            print("{} PASS".format(function.__name__))
        run_test(test_fill_window_should_return_true)
        run_test(test_fill_window_should_return_false)
        run_test(test_fifo_propery)
        run_test(test_fifo_property_first_pop)
        run_test(test_fifo_assert_size_stay_at_max)

    run_testsuite()