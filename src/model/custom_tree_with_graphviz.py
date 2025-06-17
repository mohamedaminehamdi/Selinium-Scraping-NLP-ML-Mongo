import json
import sys
import graphviz


class CustomTreeGraphviz:

    @staticmethod
    def get_node_info(node):
        node_name = str(node['id']) + "->" + str(node['label'])
        node_data = str(node['id'])
        node_children = node.get('subs', None)
        return node_name, node_data, node_children

    @staticmethod
    def display_tree_from_file(file_uri: str):
        json_file = open(file_uri, encoding='utf-8')
        json_data = json.load(json_file)

        traversed_nodes = [json_data]  # start with root node

        # initialize the graph
        f = graphviz.Digraph('finite_state_machine', filename=file_uri.replace(".json", ".gv"))
        f.attr(rankdir='LR', size='10')
        f.attr('node', shape='rectangle')

        while (len(traversed_nodes) > 0):
            cur_node = traversed_nodes.pop(0)
            cur_node_name, cur_node_data, cur_node_children = CustomTreeGraphviz.get_node_info(cur_node)
            if (cur_node_children is not None):  # check if the cur_node has a child
                for next_node in cur_node_children:
                    traversed_nodes.append(next_node)
                    next_node_name = CustomTreeGraphviz.get_node_info(next_node)[0]
                    f.edge(cur_node_name, next_node_name, label='')  # add edge to the graph
        f.view()


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
    # first arg section, second arg rayon
    file_uri = cmdargs[1] if len(cmdargs) > 1 else "src/model/Carrefour/categories_carrefour.json"
    CustomTreeGraphviz.display_tree_from_file(file_uri=file_uri)
