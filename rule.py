from math import sqrt


def allProperSubset(superset):
    """
    msg: 获得集合的所有非空真子集
    param {
        superset:tuple 元组形式的集合
    }
    return{
        proper_subsets:list 列表形式的集合，列表当中的每个元素均为元组形式的给定集合的非空真子集
    }
    """
    n = len(superset)
    proper_subsets = []
    for i in range(1, 2 ** n - 1):  # 根据子集个数，循环遍历所有非空真子集
        proper_subset = []
        for j in range(n):
            if (i >> j) % 2:  # 判断二进制下标为 j 的位置数是否为 1
                proper_subset.append(superset[j])
        proper_subsets.append(tuple(proper_subset))
    return proper_subsets


def associationRules(frequent_itemsets, min_conf):
    """
    msg: 由频繁项集产生强关联规则
    param {
        frequent_itemsets:dict 字典形式的频繁项集的集合
        min_conf:double 最小置信度阈值
    }
    return{
        rules_list:list 以规则为元素的列表，其中规则以三元组 (频繁项集 Z，子集 S，子集 Z-S) 形式组织，对应规则 S⇒Z−S
    }
    """
    rules_list = []  # 创建一个以规则为元素的列表，其中规则以三元组 (频繁项集 Z，子集 S，子集 Z-S) 形式组织，对应规则 S⇒Z−S
    for itemset in frequent_itemsets:  # 遍历所有的频繁项集
        if len(itemset) == 1:  # 判断是否为频繁 1 项集，因为使用频繁 1 项集产生的规则是无用的
            continue
        else:
            proper_subsets = allProperSubset(itemset)  # 得到当前频繁项集的所有非空真子集
            frequent_itemset_support = frequent_itemsets[itemset]  # 得到当前频繁项集对应的支持度计数
            for proper_subset in proper_subsets:  # 遍历当前频繁项集的所有非空真子集并生成对应规则
                if frequent_itemset_support / frequent_itemsets[proper_subset] >= min_conf:
                    rules_list.append((
                        itemset, proper_subset, tuple(sorted(set(itemset) - set(proper_subset)))
                    ))  # 当前规则满足最小置信度阈值，将其以三元组形式加入规则列表
    return rules_list


def conf(rule, frequent_itemsets):
    """
    msg: 计算关联规则的置信度
    param {
        rule:tuple 以三元组 (频繁项集 Z，子集 S，子集 Z-S) 形式组织的规则
        frequent_itemsets:dict 字典形式的频繁项集的集合
    }
    return{
        rule_conf:double 关联规则的置信度
    }
    """
    rule_conf = frequent_itemsets[rule[0]] / frequent_itemsets[rule[1]]
    return rule_conf


def sup(rule, total_num, frequent_itemsets):
    """
    msg: 计算关联规则的支持度
    param {
        rule:tuple 以三元组 (频繁项集 Z，子集 S，子集 Z-S) 形式组织的规则
        total_num:int 事务数据集中所有事务的数量
        frequent_itemsets:dict 字典形式的频繁项集的集合
    }
    return{
        rule_sup:double 关联规则的支持度
    }
    """
    rule_sup = frequent_itemsets[rule[0]] / total_num
    return rule_sup


def lift(rule, total_num, frequent_itemsets):
    """
    msg: 使用提升度评判关联规则
    param {
        rule:tuple 以三元组 (频繁项集 Z，子集 S，子集 Z-S) 形式组织的规则
        total_num:int 事务数据集中所有事务的数量
        frequent_itemsets:dict 字典形式的频繁项集的集合
    }
    return{
        rule_lift:double 关联规则的提升度
    }
    """
    rule_lift = frequent_itemsets[rule[0]] * total_num / (frequent_itemsets[rule[1]] * frequent_itemsets[rule[2]])
    return rule_lift


def cosine(rule, frequent_itemsets):
    """
    msg: 使用余弦评判关联规则
    param {
        rule:tuple 以三元组 (频繁项集 Z，子集 S，子集 Z-S) 形式组织的规则
    }
    return{
        rule_cosine:double 关联规则的余弦
    }
    """
    rule_cosine = frequent_itemsets[rule[0]] / sqrt(frequent_itemsets[rule[1]] * frequent_itemsets[rule[2]])
    return rule_cosine


def printRules(frequent_itemsets, rules_list, total_num):
    """
    msg: 以固定格式打印所有规则
    param {
        frequent_itemsets:dict 字典形式的频繁项集的集合
        rules_list:list 以规则为元素的列表，其中规则以三元组 (频繁项集 Z，子集 S，子集 Z-S) 形式组织，对应规则 S⇒Z−S
        total_num:int 事务数据集中所有事务的数量
    }
    return: None
    """
    for rule in rules_list:
        rule_lift = lift(rule, total_num, frequent_itemsets)
        rule_cosine = cosine(rule, frequent_itemsets)
        rule_conf = conf(rule, frequent_itemsets)
        rule_sup = sup(rule, total_num, frequent_itemsets)
        print(
            '{:}-->{:}: support = {:.2%}, confidence = {:.2%}, lift = {:.3}, cosine = {:.3}'.format(str(rule[1]),
                                                                                                    str(rule[2]),
                                                                                                    rule_sup,
                                                                                                    rule_conf,
                                                                                                    rule_lift,
                                                                                                    rule_cosine))
