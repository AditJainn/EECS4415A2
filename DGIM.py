class dgim ():
    amountOfBuckets = 2
    startTime = None
    endTime = 0
    def __init__(self, userName):
        self.userName = userName  # Instance variable
        self.buckets = {} # KEY IS bucket size , value is list of buckets

    def addBit (self, timeStamp):
        if 1 not in self.buckets:
           self.buckets[1] = []  
        self.buckets[1].append(bucket(timeStamp,1))
        if dgim.startTime is None :
            dgim.startTime = timeStamp
        else:
            dgim.endTime = timeStamp
        self.consolidate(1)
    
    # Where b1 is the older timestamp and b2 is relatively newer
    def combineBucket(self, b1,b2):
        return bucket(b2.timeStamp, b2.count*2)


    def consolidate (self,bucketSize): # we only ever consolodiate 2 buckets for every time this function is called
        if len(self.buckets[bucketSize])>self.amountOfBuckets:
            b1 = self.buckets[bucketSize].pop(0) # gets rid of the first 2 from the list
            b2 = self.buckets[bucketSize].pop(0)
            newBucket = self.combineBucket(b1,b2)
            if bucketSize + 1 not in self.buckets:
                self.buckets[bucketSize + 1] = [] 
            self.buckets[bucketSize+1].append(newBucket)
            self.consolidate(bucketSize+1)

    def queryTwo (self,endtime):
        # endtime = dgim.endTime + endTime
        currentTime = None
        count = 0
        for key in sorted(self.buckets):
            bucketList = self.buckets.get(key)
            if bucketList != None:
                for b in reversed(bucketList):
                    currentTime = b.timeStamp
                    if currentTime <= endtime:
                        count+= ceil(b.count/2) # ceiling  incase its a 1 
                        return count
                    count += b.count
        return count




    def query (self,endtime): # where endTime is less than current time 1,2,3,4,5,6
        currentTime = None
        bucketSize = 1
        count = 0 
        while currentTime is None or currentTime > endtime :
            bucketList = self.buckets.get(bucketSize)
            if bucketList != None:
                for b in reversed(bucketList):
                    currentTime = b.timeStamp
                    delta = currentTime - endtime
                    if currentTime <= endtime:
                        count+= ceil(b.count/2) # ceiling  incase its a 1 
                        return count
                    count += b.count
            bucketSize+=1
        return count
    # DUNNo IFF THIS works but ima leave it here for now...
    def getTotal(self):
        total = 0
        for bucketSize in self.buckets:
            if self.buckets[bucketSize] != None:
                for bucket in self.buckets[bucketSize]:
                    total+=bucket.count
        return total

    def __str__(self):
        return f"DGIM(userName={self.userName}, buckets={self.buckets})"
class bucket():
    def __init__(self, timeStamp, count):
        self.count = count  # Instance variable
        self.timeStamp = timeStamp
    def __str__(self):
        return f"\n Bucket(timeStamp={self.timeStamp}, count={self.count})"
    def __repr__(self):  # For debugging
        return self.__str__()