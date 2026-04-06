import math

class CacheSimulator:
    def __init__(self, cache_size, block_size, associativity):
        # 1. Save the hardware settings 
        self.cache_size = cache_size
        self.block_size = block_size
        self.associativity = associativity
        
        # 2. Calculate the architecture 
        # Number of Sets = Cache Size / (Block Size * Associativity)
        self.num_sets = cache_size // (block_size * associativity)
        
        # 3. Calculate how many bits go to each "slice" of the 32-bit address
        self.offset_bits = int(math.log2(block_size))
        self.index_bits = int(math.log2(self.num_sets))
        self.tag_bits = 32 - (self.offset_bits + self.index_bits)
        
        # 4. Create the empty "Desk" (The Cache structure)
        # We make a list of empty lists. Each sub-list represents a 'Set' in the hardware.
        self.cache = [[] for _ in range(self.num_sets)]
        
        # 5. Set up the scoreboards to track performance
        self.hits = 0
        self.misses = 0
        self.total_accesses = 0

    def access_memory(self, hex_address):
        self.total_accesses += 1
        
        # 1. Convert the hex string (e.g., "0x4A3F") into a regular integer
        address_int = int(hex_address, 16)
        
        # 2. Extract the Index Bits
        # We shift right (>>) to delete the offset bits.
        # Then we use an AND mask (&) to grab exactly the number of index bits we need.
        index_mask = (1 << self.index_bits) - 1
        index = (address_int >> self.offset_bits) & index_mask
        
        # 3. Extract the Tag Bits
        # We shift right past BOTH the offset and index bits to get what's left.
        tag = address_int >> (self.offset_bits + self.index_bits)
        
        # 4. Find the specific Set on our "Desk"
        target_set = self.cache[index]
        
        # 5. Check for a Hit or Miss
        if tag in target_set:
            # CACHE HIT: The data was found!
            self.hits += 1
            
            # Update LRU (Least Recently Used) policy:
            # Move this tag to the end of the list so we know it was just used.
            target_set.remove(tag)
            target_set.append(tag)
            
        else:
            # CACHE MISS: Data not found, we have to fetch it.
            self.misses += 1
            
            # If the set is full, we must kick out the oldest item (at index 0)
            if len(target_set) >= self.associativity:
                target_set.pop(0)
                
            # Add the new tag to the end of the list
            target_set.append(tag)

    def get_stats(self):
        # A simple helper function to calculate our final scores
        if self.total_accesses == 0:
            return {
                "Total Accesses": 0,
                "Hits": 0,
                "Misses": 0,
                "Hit Rate (%)": 0, 
                "Miss Rate (%)": 0
            }
            
        hit_rate = (self.hits / self.total_accesses) * 100
        miss_rate = 100 - hit_rate
        
        return {
            "Total Accesses": self.total_accesses,
            "Hits": self.hits,
            "Misses": self.misses,
            "Hit Rate (%)": round(hit_rate, 2),
            "Miss Rate (%)": round(miss_rate, 2)
        }