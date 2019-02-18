class ticker:
    def __init__(self, in_tick_time):
        self.total_time = 0.0
        self.tick_time = in_tick_time
        self.frame_time = 0.0

    def tick(self, delta_time):
        result = False
        self.total_time += delta_time
        self.frame_time += self.delta_time
        if self.frame_time > self.tick_time :
            result = True
            float_count = self.frame_time / self.tick_time
            int_count = int(float_count)
            if abs(float_count - int_count) > 0.000001:
                int_count -= 1
                self.frame_time = self.frame_time - self.tick_time * int_count
            else :
                self.frame_time = 0

        return result

    def reset(self, in_tick_time):
        self.total_time = 0.0
        self.tick_time = in_tick_time
        self.frame_time = 0.0
