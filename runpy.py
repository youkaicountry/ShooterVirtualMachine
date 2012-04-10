import gen

rsvm = gen.RSVM()
rsvm.spawnThread(0, 0, 0, 0)
print("init thread ok")
print(rsvm.threads)
rsvm.run()

