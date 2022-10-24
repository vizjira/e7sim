import random
import math

class Simulator:
    def get_base_speed(self, slot = 0):
        stats = [
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8,9,10],
            [1,2,3,4,5,6,7,8],
            [1,2,3,4,5,6,7,8,9,10,11],
            [1,2,3,4,5,6,7,8,9,10,11],             
        ]
        
        random.shuffle(stats[slot])

        for i in range(4): # try four times
            if stats[slot].pop() == 1:  # found speed
                return self.get_random_speed_upgrade() # presume that the spread is the same as for upgrading
            
        return 0 # no speed found

    def get_random_speed_upgrade(self):
        n = random.randrange(1, 100_000)
        
        if n <= 33223:
            return 2
        elif n <= 66446:
            return 3
        elif n <= 99668:
            return 4
        else:
            return 5

    def roll(self):
        for i in range(5): # roll 5 upgrades
            which_substat = random.randrange(1, 5) # 1,2,3,4  we only care about 1, speed
            if which_substat != 1:
                yield 0 # did not roll speed
            else:
                yield self.get_random_speed_upgrade() # rolled 2, 3, 4 speed

    def try_until(self, required_speed, slot):
        counter = 0
        counter_no_speed = 0
        counter_insufficient_speed = 0
        
        while True:
            counter += 1
                
            base_speed = self.get_base_speed(slot)
            
            if base_speed == 0:
                counter_no_speed += 1
                    
            if base_speed > 0:            
                rolls = list(self.roll())
                speed_roll_count = len(list(filter(lambda x: x > 0, rolls)))
                total_speed = sum(rolls) + base_speed
                
                reforge = {
                    0: 0,
                    1: 1,
                    2: 2,
                    3: 3,
                    4: 4,
                    5: 4
                }    
                
                # print(rolls)
                # print("Speed roll count: %s" % speed_roll_count)
                # print("Base speed: %s" % base_speed)
                # print("Total Speed: %s" % total_speed)
                # print("Reforge value: %s" % reforge[speed_roll_count])
                # print("\n")

                if total_speed + reforge[speed_roll_count] >= required_speed:
                    return (counter, counter_no_speed, counter_insufficient_speed, total_speed + reforge[speed_roll_count])
                else:
                    counter_insufficient_speed += 1

    def gear_ran(self, count, up_to_speed):
        # print("Gearing Ran to %s speed" % up_to_speed)
        
        tries_until = []
        
        base_speed = 206 # speed set ran + 90 boots
        speed_required_per_slot = math.ceil((up_to_speed - base_speed) / 5.0) # split the remaining required speed across the 5 non-boot items
        
        for i in range(count):
            total_item_count = 0
            total_item_no_speed = 0
            total_speed_acquired = 0
            
            for slot in range(5): # go through all gear slots one by one and get one item which beats the average required (except ring)
                if slot == 4: 
                    # ring, last and hard to gear item slot, only try to reach what is absolutly necessary the reach the goal
                    result = self.try_until(up_to_speed - base_speed - total_speed_acquired, slot)
                else:
                    result = self.try_until(speed_required_per_slot, slot)
                    
                item_count, item_counter_no_speed, item_counter_insufficient_speed, speed = result                
                total_item_count += item_count
                total_item_no_speed += item_counter_no_speed
                
                total_speed_acquired += speed        
                
                print("[Slot: %s] Total item count %s, items without speed: %s, items with insufficient speed: %s, speed: %s" % (slot, item_count, item_counter_no_speed, item_counter_insufficient_speed, speed))
                
            print("Total tries required: %s" % total_item_count)  

            tries_until.append(total_item_count - total_item_no_speed) # exclude non speed items from the total count, we are upgrading only
        
        with open("result.txt", mode='w') as f:
            for x in tries_until:
                f.write(str(x) + "\n")


if __name__ == "__main__":
    sim = Simulator()
    
    
    # How Long does it take to craft x of speed y for slot z
    count = 1 # nr of items to craft (craft until [count] of speed [x] is reached)
    
    for slot in [0,1,4]:
        for speed in range(18, 26):
            total_tries = 0
            total_tries_speed_base = 0

            for x in range(count):
                tries_needed, counter_no_speed, _, _= sim.try_until(speed, slot)
                total_tries += tries_needed
                total_tries_speed_base += tries_needed - counter_no_speed

            print("It took %s acquired epics of which %s had speed to craft %s of slot %s with speed %s" % (total_tries, total_tries_speed_base, count, slot, speed))
    
    # gear x rans to y speed        
    # sim.gear_ran(1, 315)
