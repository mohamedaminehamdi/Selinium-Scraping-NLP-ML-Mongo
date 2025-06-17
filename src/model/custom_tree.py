import json
import os
import sys
from typing import List, Literal, Optional

import dacite
from treelib import Node, Tree  # type: ignore

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'model'))
sys.path.append(parent_dir)
from src.model.my_model import AislesSub
from src.model.product import Category

parent_dir2 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'utils'))
sys.path.append(parent_dir2)
from src.utils.my_utils import custom_dump

class CustomTree:
    @staticmethod
    def get_node_info(tree: Tree, node_el: Optional[Node] = None, identifier: Optional[str] = None) -> Optional[str]:
        if node_el is None and isinstance(identifier, str):
            node_el = tree.get_node(identifier)
        if node_el is None:
            return ("node_el: " + str(node_el) + ", identifier: " + str(identifier) + " not found")
        return ("node_el: " + str(node_el) + ", is_leaf: " + str(node_el.is_leaf()) + ", is_root: " + str(node_el.is_root())
                + ", ancestor id: " + str(tree.ancestor(node_el.identifier)))  # + ", successors: " + [str(successor) for successor in node_el.successors(tree_id=tree)])

    @staticmethod
    def get_ancestors_ids(tree: Tree, search_with_node: Optional[Node] = None, search_with_identifier: Optional[str] = None) -> List[Node]:
        ancestors_ids: List[Node] = []
        ancestor_identifier = tree.ancestor(search_with_identifier) if search_with_node is None and isinstance(search_with_identifier, str) else tree.ancestor(search_with_node.identifier)
        while ancestor_identifier is not None:
            ancestors_ids.insert(0, ancestor_identifier)
            ancestor_identifier = tree.ancestor(ancestor_identifier)
        return ancestors_ids

    @staticmethod
    def get_nodes_from_ids(tree: Tree, identifiers: List[str]) -> List[Node]:
        nodes: List[Node] = []
        for identifier in identifiers:
            node_el = tree.get_node(identifier)
            nodes.append(node_el)
        return nodes

    @staticmethod
    def remove_root_node(nodes: List[Node]) -> List[Node]:
        for node_el in nodes:
            if node_el.is_root():
                nodes.remove(node_el)
                return nodes
        return nodes

    @staticmethod
    def get_objs_from_nodes(nodes: List[Node]) -> List[Category]:
        objs: List[Category] = []
        for node in nodes:
            data = node.data # data is already of type Category, so no cast needed
            objs.append(data)
        return objs

    @staticmethod
    def search_node_in_tree(tree: Tree, search: str) -> Node | None:
        for node1 in tree.all_nodes_itr():
            if search == node1.data.label:
                print(f"identifier: {node1.identifier}, data.label: {node1.data.label}, data.id: {node1.data.id}")
                return node1
        return None

    @staticmethod
    def get_ancestors_from_search_node(tree: Tree, search: str, remove_root: bool = False, add_current_root: bool = False) -> List[Category] | None:
        node1 = CustomTree.search_node_in_tree(tree, search)
        if isinstance(node1, Node):
            ancestors_ids = CustomTree.get_ancestors_ids(tree=tree, search_with_node=node1)
            ancestors_nodes = CustomTree.get_nodes_from_ids(tree=tree, identifiers=ancestors_ids)
            if add_current_root:
                ancestors_nodes.append(node1)
            ancestors_nodes = ancestors_nodes if not remove_root else CustomTree.remove_root_node(ancestors_nodes)
            ancestors_objs = CustomTree.get_objs_from_nodes(nodes=ancestors_nodes)
            return ancestors_objs

        else:
            return None

    @staticmethod
    def create_all_nodes(tree: Tree, data: List[AislesSub], parent_id: str):
        for item in data:
            aisle_sub = AislesSub(id=item.id, label=item.label, subs=item.subs)
            aisle_sub2 = Category(aisle_sub.id, aisle_sub.label)
            tree.create_node(aisle_sub.id, aisle_sub.id, parent=parent_id, data=aisle_sub2)
            # tree.create_node(aisle_sub2, aisle_sub.id, parent=parent_id)
            if isinstance(aisle_sub.subs, list):
                CustomTree.create_all_nodes(tree=tree, data=aisle_sub.subs, parent_id=aisle_sub.id)
        return tree

    _data_property_type = Literal["id", "label"]

    @staticmethod
    def build_tree_from_file(file_uri: str, save2file: bool = False, data_property: _data_property_type = "label"):
        json_file = open(file_uri, encoding='utf-8')
        products = json.load(json_file)
        products:AislesSub = dacite.from_dict(data_class=AislesSub, data=products, config=dacite.Config(strict=True))
        aisles_sub_list = products.subs
        tree = Tree()
        aisle_sub2 = Category(products.id, label=products.id)
        tree.create_node(aisle_sub2.id, identifier=aisle_sub2.id, data=aisle_sub2)  # root node
        tree = CustomTree.create_all_nodes(tree=tree, data=aisles_sub_list, parent_id=aisle_sub2.id)
        tree2_str = tree.show(data_property="label", stdout=False, line_type="ascii-em")
        file_uri = file_uri.replace(".json", ".txt")
        if os.path.exists(file_uri):
            os.remove(file_uri)
        if save2file:
            tree.save2file(file_uri, data_property=data_property, line_type="ascii-em")
        # print(tree2)
        return tree

    @staticmethod
    def find_sub_aisle(aisles_subs: List[any], search: str) -> Optional[AislesSub]:
        for aisle_sub in aisles_subs:
            aisle_sub = AislesSub(**aisle_sub)
            print("aisle_sub.label: " + str(aisle_sub.label))
            if aisle_sub.label.lower() == search.lower():
                return aisle_sub
            elif aisle_sub.subs is not None:
                found2 = CustomTree.find_sub_aisle(aisle_sub.subs, search)
                if found2:
                    print("found2: " + str(found2))
                    return aisle_sub
        return None

    @staticmethod
    def aisles_ancestors_fetcher(search: str = "Boissons", file_uri: str = "src/model/Auchan/categories_auchan.json") -> List[Category] | None:
        tree = CustomTree.build_tree_from_file(file_uri=file_uri, save2file=True)
        objs = CustomTree.get_ancestors_from_search_node(tree=tree, search=search, remove_root=True, add_current_root=True)
        return objs

    @staticmethod
    def aisles_ancestors_fetcher_to_json(search: str, file_uri: str = "src\model\categories_casino.json") -> str | None:
        objs = CustomTree.aisles_ancestors_fetcher(search, file_uri)
        json_data = custom_dump(objs)
        return json_data


if __name__ == "__main__":
    '''
    first arg : the script name
    second arg: the categories file_path
    third arg: data_property: either label or id
    auchan_uri = "src/model/Auchan/categories_auchan.json"
    casino_uri = "src/model/Casino/categories_casino.json"
    carrefour_uri = "src/model/Carrefour/categories_carrefour.json"
    '''
    cmdargs = sys.argv
    # Print it
    # first arg section, second arg aisle
    file_uri = cmdargs[1] if len(cmdargs) > 1 else "src/model/Carrefour/categories_carrefour.json"
    data_property = cmdargs[2] if len(cmdargs) > 2 else None

    print("building CustomTree for: " + file_uri)
    if data_property:
        CustomTree.build_tree_from_file(file_uri=file_uri, save2file=True, data_property=data_property)
    else:
        CustomTree.build_tree_from_file(file_uri=file_uri, save2file=True)
