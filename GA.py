import random
from data import location
import math

gene_len = 20
city_dist_mat = []
group_size = 100
P_cross = 0.88
P_mu = 0.1
plt_best = []


def get_city_dist_mat(loc):
    city_dist_mat = []
    # 由坐标计算每对城市之间的距离
    for i in range(gene_len):
        row = []
        for j in range(gene_len):
            dist_x = loc[i][0] - loc[j][0]
            dist_y = loc[i][1] - loc[j][1]
            row.append(math.sqrt(dist_x*dist_x + dist_y*dist_y))
        city_dist_mat.append(row)
    return city_dist_mat


class Individual:
    def __init__(self, genes=None):
        # 随机生成序列
        if genes is None:
            genes = [i for i in range(gene_len)]
            random.shuffle(genes)
        self.genes = genes
        self.fitness = self.evaluate_fitness()

    # 适应度即以当前序列走完一个闭合曲线的路径之和
    def evaluate_fitness(self):
        # 计算个体适应度
        fitness = 0.0
        for i in range(gene_len - 1):
            # 起始城市和目标城市
            from_idx = self.genes[i]
            to_idx = self.genes[i + 1]
            fitness += city_dist_mat[from_idx][to_idx]
        # 连接首尾【最后一个城市->起点城市】
        fitness += city_dist_mat[self.genes[-1]][self.genes[0]]
        return fitness


def initialize(group_size):
    Group = []
    for i in range(group_size):
        Group.append(Individual())
    return Group


def evaluate(Group: list, group_size):
    Eval = []
    Best = 0.0
    for i in range(group_size):
        Eval.append(1000000.0 / Group[i].evaluate_fitness())
        if i == 0 or Best < Eval[i]:
            Best = Eval[i]
    return Eval, Best


def selection(Group: list, Eval: list, group_size):
    sum = 0
    for i in range(group_size):
        sum += Eval[i]
    P = []
    for i in range(group_size):
        P.append(Eval[i]/sum)
    new_Group = []
    for i in range(group_size):
        m = 0
        r = random.random()
        for j in range(group_size):
            m = m + P[j]
            if r <= m:
                new_Group.append(Group[j])
                break
    return new_Group


def crossover(Group: list, group_size, gene_len):
    Group_cross = []
    for i in range(group_size):
        P = random.random()
        if P < P_cross:
            Group_cross.append(i)
    a = 0
    while a < len(Group_cross) - 1:
        b = a + 1
        f1 = Group_cross[a]
        f2 = Group_cross[b]
        s = random.randint(0, max(gene_len - 5, 0))
        pos_f1 = []
        for i in range(gene_len):
            if Group[f1].genes[i] >= s:
                pos_f1.append(i)
        pos_f2 = []
        for i in range(gene_len):
            if Group[f2].genes[i] >= s:
                pos_f2.append(i)
        for i in range(len(pos_f1)):
            t = Group[f1].genes[pos_f1[i]]
            Group[f1].genes[pos_f1[i]] = Group[f2].genes[pos_f2[i]]
            Group[f2].genes[pos_f2[i]] = t
        a = a + 2
    return Group


def reverse_mutation(Group: list, group_size, gene_len):
    for i in range(group_size):
        P = random.random()
        if P < P_mu:
            s = random.randint(0, gene_len - 4)
            t = Group[i].genes[s]
            Group[i].genes[s] = Group[i].genes[s + 2]
            Group[i].genes[s + 2] = t
    return Group


def GA_main():
    random.seed(0)
    global city_dist_mat
    loc, s = location(gene_len)
    city_dist_mat = get_city_dist_mat(loc)
    # 初始化一个规模为5的群体
    Group = initialize(group_size)
    # 适应值评价
    Eval, Best = evaluate(Group, group_size)
    plt_best.append(Best)
    Best_group = Group
    # 迭代
    epoch = 0
    while epoch < 100:
        # 选择 采用轮盘赌选择算法
        Group = selection(Group, Eval, group_size)
        # 杂交
        Group = crossover(Group, group_size, gene_len)
        # 变异
        Group = reverse_mutation(Group, group_size, gene_len)
        Eval, Max = evaluate(Group, group_size)
        if Max > Best:
            Best = Max
            Best_group = Group
        epoch = epoch + 1
        plt_best.append(Best)
        print("GA_Epoch:", epoch, " Best:", Best)

    return plt_best


if __name__ == '__main__':
    GA_main()