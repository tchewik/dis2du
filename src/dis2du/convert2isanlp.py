from isanlp.annotation_rst import DiscourseUnit

id = 0


def find_simple_nuclearity(left_node, right_node):
    if right_node.prop == 'Nucleus':
        if left_node.prop == 'Nucleus':
            return 'NN'
        return 'SN'
    return 'NS'


def correct_nuclearity(relation, nuclearity):
    if not nuclearity or not relation:
        return

    multinuc = 'joint sequence contrast comparison restatement same-unit'
    if relation in multinuc:
        return 'NN'
    return nuclearity


def bracketize_text(text):
    return text.replace('-RB-', ')').replace('-LB-', '(').replace('##### ', '\n')


def datastructure2isanlpdu(tree):
    global id
    id += 1

    if tree.lnode:
        new_relation = ''
        new_order = ''
        new_text = ''

        if tree.lnode.nucedu:
            edu_left = DiscourseUnit(
                id=tree.lnode.nucedu,
                relation='elementary',
                text=bracketize_text(tree.lnode.text)
            )
            if tree.lnode.relation != 'span':
                new_relation = tree.lnode.relation
                new_order = find_simple_nuclearity(tree.lnode, tree.rnode)
                new_text = bracketize_text(tree.text)

        if tree.rnode.nucedu:
            edu_right = DiscourseUnit(
                id=tree.rnode.nucedu,
                relation='elementary',
                text=bracketize_text(tree.rnode.text)
            )
            if not new_relation and tree.rnode.relation != 'span':
                new_relation = tree.rnode.relation
                new_order = find_simple_nuclearity(tree.lnode, tree.rnode)
                new_text = bracketize_text(tree.text)

        if not new_relation:
            new_relation = tree.relation
            new_order = tree.form
            new_text = bracketize_text(tree.text)

            if new_order:
                if new_order == 'NS' and tree.rnode:
                    new_relation = tree.rnode.relation
                elif new_order == 'SN' and tree.lnode:
                    new_relation = tree.lnode.relation

        if new_relation == 'span' or new_relation == 'virtual-root':
            if new_order == 'NS':
                new_relation = tree.rnode.relation
            elif new_order == 'SN':
                new_relation = tree.lnode.relation
            elif new_order == 'NN':
                new_relation = tree.lnode.relation

        if tree.lnode.nucedu and tree.rnode.nucedu:
            # Left node is EDU & right node is EDU
            if not new_relation:
                print(1)

            new_unit = DiscourseUnit(
                id=id,
                relation=new_relation,
                nuclearity=new_order,
                left=edu_left,
                right=edu_right,
                text=new_text
            )

        elif tree.lnode.nucedu:
            if not new_relation:
                print(2)
            # Left node is EDU & right node is not EDU
            new_unit = DiscourseUnit(
                id=id,
                relation=new_relation,
                nuclearity=new_order,
                left=edu_left,
                right=datastructure2isanlpdu(tree.rnode),
                text=new_text
            )

        elif tree.rnode.nucedu:
            if not new_relation:
                print(3)
            # Left node is not EDU & right node is EDU
            new_unit = DiscourseUnit(
                id=id,
                relation=new_relation,
                nuclearity=new_order,
                left=datastructure2isanlpdu(tree.lnode),
                right=edu_right,
                text=new_text
            )

        else:
            # Left node is not EDU & right node is not EDU
            if new_relation:
                new_unit = DiscourseUnit(
                    id=id,
                    relation=new_relation,
                    nuclearity=new_order,
                    left=datastructure2isanlpdu(tree.lnode),
                    right=datastructure2isanlpdu(tree.rnode),
                    text=new_text
                )
            else:
                # No relation defined for (assuming) root node of tree
                new_unit = DiscourseUnit(
                    id=id,
                    relation=tree.lnode.relation,
                    nuclearity=new_order,
                    left=datastructure2isanlpdu(tree.lnode),
                    right=datastructure2isanlpdu(tree.rnode),
                    text=new_text
                )


    else:
        new_unit = DiscourseUnit(
            id=tree.nucedu or id,
            relation='elementary',
            text=bracketize_text(tree.text)
        )

    new_unit.nuclearity = correct_nuclearity(new_unit.relation, new_unit.nuclearity)

    return new_unit


def split_single_pseudorst(tree):
    if not tree.relation:  # or tree.relation in ['virtual-root', 'root']:
        return [tree.lnode, tree.rnode]

    return [tree]


def split_single_pseudounit(tree):
    if not tree.text or not tree.relation or tree.relation in ['virtual-root', 'root']:
        return [tree.left, tree.right]

    return [tree]


def convert2isanlp(rst):
    global id
    id = rst.tree.eduspan[-1]  # number of edus in tree
    return datastructure2isanlpdu(rst.tree)
