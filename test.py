import gc

print(gc.isenabled())

print(gc.collect(2))

print(gc.get_stats())
print("-----------")

print("Collect")
print(gc.DEBUG_LEAK)

print("Debug ")
print(gc.DEBUG_COLLECTABLE)
print(gc.DEBUG_UNCOLLECTABLE)

print(gc.garbage)
print("-----------")
