import gen

rsvm = gen.RSVM()
rsvm.spawnThread(0, 0, 0, 0)
print("init thread ok")
for i in xrange(1000):
    print(rsvm.threads)
    rsvm.run()

