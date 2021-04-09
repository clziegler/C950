#!/usr/bin/env python -u
# encoding: utf-8

class HashTable:
    """The HashTable Data Structure

    Attributes
    ----------
        size : int
            The initial size of the hashtable
        max_load; float
            Determine the at what point to resize the hashtable
        length : int
            the number of items in the hashtable
        map : list
            the list that is the hashtable
        
    Methods
    -------
        add(key, value):
            adds a key value tuple to the hashtable
        get(key):
            returns the value of of the key
        delete(key):
            deletes the key value pair from the hashtable
          
    """
    
    def __init__(self):
        self.size = 124
        self.max_load = 0.50
        self.length = 0
        self.map = [None] * self.size

    def __repr__(self):
        """returns a string of containing all the items in the hashtable
        Time Complexity: O(n)
        Space Complexity O(1)
        """
        x = [item for item in self.map if item is not None]
        return str(x)

    
    def __iter__(self): 
        """iterates through the all the items in the hashtable
        Time Complexity: O(n)
        Space Complexity O(1)
        """     
        x = sorted([item for item in self.map if item is not None])
        yield from x

    def __len__(self):
        """returns the size of the hashtable
        Time Complexity: O(1)
        Space Complexity O(1)
        """   
        return self.length
        
    def __setitem__(self, key, value):
        self.add(key, value)
    
    def __getitem__(self, key):
        index = self._find_item(key)
        return self.map[index][1]

    def __delitem__(self, key):
        """Adds a key value pair to the hashtable
        Time Complexity: O(n)
        Space Complexity O(1) 
        """
        self.delete(key)

    def add(self, key, value):
        """Adds a key value pair to he hashtable
        Time Complexity: O(n)
        Space Complexity O(1) 
        """

        self.length += 1
        key_hash = self._get_hash(key)
        while self.map[key_hash] is not None:
            #If the key is already in the table, decrement the length of the table
            if self.map[key_hash][0] == key:
                self.length -= 1
                break
            #Find an empty slot
            key_hash = self._increment_key(key_hash)
        key_value_pair = (key, value)
        self.map[key_hash] = key_value_pair
        #If size of the hashmap is 50% full, resize the map
        if self.length / float(self.size) >= self.max_load:
            self._resize()
    
    
    def get(self, key):
        """returns the value of a given key
        Time Complexity: O(n)
        Space Complexity O(1) 
        """
        index = self._find_item(key)
        return self.map[index][1]
          
    
    def delete(self, key):
        """removes a key value pair by the given key
        Time Complexity: O(1)
        Space Complexity O(1) 
        """
        index = self._find_item(key)
        self.map[index] = None

    
    def _get_hash(self, key):
        """return the hash of the key"""
        return hash(key) % self.size
  
    
    def _increment_key(self, key):
        """moves the index of the hashmap by 1
        Time Complexity: O(1)
        Space Complexity O(1) 
        """
        return (key + 3) % self.size
    
    
    def _find_item(self, key):
        """returns the keyhash of a given key
        Time Complexity: O(n)
        Space Complexity O(1) 
        """
        key_hash = self._get_hash(key)
        if self.map[key_hash] is None:
            raise KeyError
        if self.map[key_hash][0] != key:
            original_key = key_hash
            while self.map[key_hash][0] != key:
                key_hash = self._increment_key(key_hash)
                if self.map[key_hash] is None:
                    raise KeyError
                if key_hash == original_key:
                    raise KeyError
        return key_hash


   
    def _resize(self):
        """Resizes the hashtable
        Time Complexity: O(n)
        Space Complexity O(n) 
        """
        self.size *= 2
        self.length = 0
        old_map = self.map
        self.map = [None] * self.size
        for tuple in old_map:
            if tuple is not None:
                self[tuple[0]] = tuple[1]
