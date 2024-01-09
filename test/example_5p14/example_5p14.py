import numpy as np
import fepy

u = fepy.Field("u", np.array(["u"]))

data = fepy.inputReader("example_5p14.i")

model = fepy.Model(data, np.array(u))

print(model.tdofs)



