
class CacheHandlerError(Exception):pass
class CacheHandler():
    def __init__(self,*args,**kwargs):
        self.id_cursor=0

    def __call__(self, fun,*args, **kwargs):
        fun=self.forward
        return fun
    def result(self) -> any:pass

    def forward(self,fun,currentSql) -> None:
        return getattr(self,fun.sqlType)(fun,currentSql)
    def insert(self,fun,currentSql) -> any:
        result=fun.execSql(fun,currentSql)
        return result
    def update(self,fun,currentSql) -> any:
        result = fun.execSql(fun, currentSql)
        return result
    def delete(self,fun,currentSql) -> any:
        result = fun.execSql(fun, currentSql)
        return result
    def other(self,fun,currentSql) -> any:
        self.select(fun,currentSql)
    def select(self,fun,currentSql) -> result:
        if fun.accessNot>=fun.cacheSize:
            fun.accessNot=9
        if fun.id_cursor>=fun.cacheSize:
            fun.id_cursor=0
        cacheCur=None
        for i in range(len(fun.physicsTable)):
            if currentSql in fun.physicsTable[i]:
                cacheCur=i
        if fun.cacheBit==0:
            data=fun.execSql(fun,currentSql)
            fun.cache[fun.cacheBit]=data
            fun.physicsTable.append([fun.cacheBit,currentSql,self.id_cursor,fun.accessNot])

            fun.cacheBit += 1
            fun.accessNot+=1
            fun.id_cursor+=1
            return data

        if fun.cacheBit>0 and fun.cacheBit<fun.cacheSize:
            if cacheCur !=None:
                fun.access=cacheCur
                fun.physicsTable[cacheCur][3] = fun.accessNot
                for i in range(fun.accessNot+1,len(fun.physicsTable)):
                    fun.physicsTable[i][3]=fun.physicsTable[i][3]-1
                    fun.accessNot+=1
                return fun.cache[fun.physicsTable[cacheCur][2]]
            data = fun.execSql(fun,currentSql)
            fun.cache[fun.cacheBit] = data
            fun.physicsTable.append([fun.cacheBit, currentSql, fun.id_cursor,fun.accessNot])
            fun.cacheBit += 1
            fun.accessNot += 1
            fun.id_cursor += 1
            return data
        if fun.cacheBit>0 and fun.cacheBit==fun.cacheSize:
            if cacheCur !=None:
                fun.access = cacheCur
                fun.physicsTable[cacheCur][3]=fun.accessNot
                for i in range(fun.accessNot+1,len(fun.physicsTable)):
                    fun.physicsTable[i][3]=fun.physicsTable[i][3]-1
                fun.accessNot+=1
                # print(fun.id_cursor, cacheCur)
                if fun.id_cursor!=cacheCur:
                    fun.logicTable.append(cacheCur)
                if fun.id_cursor==cacheCur:
                    fun.id_cursor+=1


                return fun.cache[fun.physicsTable[cacheCur][2]]

            del fun.physicsTable[0]
            for i in range(0, len(fun.physicsTable)):
                fun.physicsTable[i][3] = fun.physicsTable[i][3] - 1
            if len(fun.logicTable)>0 and fun.id_cursor in fun.logicTable:
                fun.logicTable.remove(fun.id_cursor)
                fun.id_cursor+=1
            data = fun.execSql(fun,currentSql)
            fun.cache[fun.id_cursor] = data
            fun.physicsTable.append([fun.cacheBit, currentSql, fun.id_cursor,fun.accessNot])
            fun.id_cursor+=1
            fun.accessNot += 1
            return data




