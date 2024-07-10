"""Is 4 am, I can't fall a sleep, so I have to create a script to crerate vagrant infraastructure XDDD"""
import subprocess
import utils


def main(nodes):
    utils.make_vagrantfile_template(nodes=nodes)
    utils.make_hosts(nodes=nodes)
    utils.run()


if __name__ == "__main__":
    parser = utils.parser()
    args = parser.parse_args()
    nodes = args.nodes
    main(nodes=nodes)