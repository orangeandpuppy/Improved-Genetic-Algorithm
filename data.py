import random

# 便于复现
random.seed(0)


def location(n):
    loc = []
    s = random.randint(0, n - 1)
    for i in range(n):
        loc.append([random.uniform(0, 100), random.uniform(0, 100)])
    return loc, s


# 打印数据
def main():
    loc, s = location(20)
    print("Start city:", s)
    for i in range(20):
        print("Location of city {}: x {:.2f} y {:.2f}".format(i, loc[i][0], loc[i][1]))


if __name__ == '__main__':
    main()

