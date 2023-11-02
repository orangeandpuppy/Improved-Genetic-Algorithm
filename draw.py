from GA import GA_main
from AGA import AGA_main
import matplotlib.pyplot as plt

plt_GA = GA_main()
plt_AGA = AGA_main()
plt.figure()
plt.title("Best")
plt.xlabel("epoch")
plt.plot(plt_GA, label="GA")
plt.plot(plt_AGA, label="AGA")
plt.legend()
plt.savefig("image.jpg")
plt.show()