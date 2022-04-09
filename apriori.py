def findFrequentOneItemsets(dataset, min_sup):
    """
    msg: 发现所有满足最小支持度计数阈值的频繁 1 项集
    param {
        dataset:numpy.ndarray Groceries 事务数据集
        min_sup:int 最小支持度计数阈值
    }
    return{
        frequent_one_itemsets:dict 字典形式的频繁 1 项集的集合，每个键值对的键为包含项的元组，值为其对应的支持度计数
    }
    """
    items_list = [i for i in dataset.flatten() if i != '']  # 将 numpy.ndarray 类型的数据集平铺并去除所有空字符串 ''，得到所有项的列表
    items_set = set(items_list)
    frequent_one_itemsets = {}
    for item in items_set:
        num = items_list.count(item)  # 项的支持度计数
        if num < min_sup:
            continue  # 当前项的支持度计数小于最小支持度计数阈值，放弃该项
        else:
            frequent_one_itemsets[(item,)] = num  # 当前项的支持度计数大于或等于最小支持度计数阈值，将该项加入频繁 1 项集的集合
    return frequent_one_itemsets


def kMinusOneSubset(superset):
    """
    msg: 得到 k 项集的所有 k - 1 项子集
    param {
        superset:tuple k 项集
    }
    return{
        k_minus_one_subset:set k 项集的所有 k - 1 项子集
    }
    """
    sub_sorted = sorted(superset)
    k_minus_one_subset = set([tuple(sub_sorted[:i] + sub_sorted[i + 1:]) for i in range(len(sub_sorted))])
    return k_minus_one_subset


def aprioriGen(frequent_k_minus_one_itemsets):
    """
    msg: 根据频繁（k - 1）项集的集合得到候选 k 项集的集合
    param {
        frequent_k_minus_one_itemsets:dict 频繁（k - 1）项集的集合
    }
    return{
        candidate_k_set:set 候选 k 项集的集合
    }
    """
    k_minus_one_list_sorted = sorted(frequent_k_minus_one_itemsets.keys())
    candidate_k_set = set()
    for i in k_minus_one_list_sorted:
        temp_set = set([
            tuple(set(i + j)) for j in k_minus_one_list_sorted if i < j
        ])  # 连接步：将频繁（k - 1）项集的集合与其自己做连接，得到候选的 k 项集的集合
        candidate_k_set.update([
            tuple(sorted(j)) for j in temp_set if len(kMinusOneSubset(j) - set(k_minus_one_list_sorted)) == 0
        ])  # 剪枝步：根据先验性质，删除非频繁的候选 k 项集
    return candidate_k_set


def candidateItemsets(candidate_k_set, t):
    """
    msg: 得到事务 t 的候选子集，这些候选子集均是候选 k 项集的集合的元素
    param {
        candidate_k_set:set 候选 k 项集的集合
        t:numpy.ndarray Groceries 事务数据集中的事务
    }
    return{
        candidate:list 以事务 t 的候选子集为元素的列表，这些候选子集均是候选 k 项集的集合的元素
    }
    """
    candidate = []
    for i in candidate_k_set:
        if t.issuperset(i):  # 判断事务 t 是否是候选 k 项集 i 的超集，即判断候选 k 项集 i 是否是事务 t 的子集
            candidate.append(tuple(sorted(i)))
    return candidate


def apriori(dataset, frequent_one_itemsets, min_sup):
    """
    msg: 获得所有的频繁项集
    param {
        dataset:numpy.ndarray Groceries 事务数据集
        frequent_one_itemsets:dict 字典形式的频繁 1 项集的集合，每个键值对的键为包含项的元组，值为其对应的支持度计数
        min_sup:int 最小支持度计数阈值
    }
    return{
        frequent_itemsets:dict 字典形式的频繁项集的集合
    }
    """
    frequent_itemsets_list = [frequent_one_itemsets]  # 创建一个以每一层的频繁项集的集合为元素的列表
    k = 1
    while len(frequent_itemsets_list[k - 1]) != 0:  # 判断上一层的（k - 1）项集的集合是否为空，为空则说明不能再找到频繁项集，退出循环，不为空则继续循环
        candidate_k_set = aprioriGen(frequent_itemsets_list[k - 1])  # 根据频繁（k - 1）项集的集合得到候选 k 项集的集合
        if len(candidate_k_set) == 0:  # 判断候选 k 项集的集合是否为空，为空则说明不能再找到频繁项集，退出循环，不为空则继续
            frequent_itemsets_list.append({})  # 对应 del frequent_itemsets_list[-1] 语句，防止误删
            break
        candidate_itemsets_list = []  # 创建一个以各个事务的子集为元素的列表，它们均是候选的
        for t in dataset:  # t 为事务数据集中的事务
            ct = candidateItemsets(candidate_k_set, set(t))  # 得到事务 t 的候选子集，这些候选子集均是候选 k 项集的集合的元素
            candidate_itemsets_list.extend(ct)
        candidate_set = set(candidate_itemsets_list)
        candidate_dict = {}  # 创建字典形式的频繁 k 项集的集合
        for key in candidate_set:
            num = candidate_itemsets_list.count(key)  # 每个候选 k 项集的支持度计数
            if num < min_sup:
                continue  # 当前候选 k 项集不满足最小支持度计数阈值，放弃该候选 k 项集并搜索下一候选 k 项集
            else:
                candidate_dict[key] = num  # 当前候选 k 项集满足最小支持度计数阈值，将该候选 k 项集加入频繁 k 项集的集合
        frequent_itemsets_list.append(candidate_dict)
        k += 1
    del frequent_itemsets_list[-1]  # 上一层的的项集的集合为空，退出循环并且删除上一层的项集
    frequent_itemsets = {}  # 创建字典形式的频繁项集的集合
    for i in frequent_itemsets_list:
        frequent_itemsets.update(i)
    return frequent_itemsets
