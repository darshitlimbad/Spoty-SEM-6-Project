class Queue:
    def __init__(self):
        self.Queue = []

    def put(self, item=None):
        if item:
            self.Queue.append(item)
            return len(self.Queue) - 1
        return None
    
    def put_at(self, item, index: int):
        if 0 <= index < self.qsize():
            self.Queue.insert(index, item)
            return True
        raise IndexError("Index out of range")
    
    def merge(self, merge_list):
        if len(merge_list):
            for item in merge_list:
                self.Queue.append(item)
            return True
        return False
    
    def shuffle_index(self, from_index: int, to_index: int) -> bool :
        if 0 <= from_index < self.qsize() and 0 <= to_index < self.qsize():
            self.Queue.insert(to_index, self.Queue.pop(from_index))
            return True
        else:
            raise IndexError("Index out of range")
       
    def get(self, index: int = 0):
        if 0 <= index < self.qsize():
            return self.Queue.pop(index)
        raise IndexError("Index out of range")
       
    def queue(self):
        return self.Queue if not self.is_empty() else None 
    
    def clear(self):
        self.Queue = []
        return True
        
    def qsize(self):
        return len(self.Queue)

    def is_empty(self):
        return self.qsize() == 0
