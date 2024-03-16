import networkx as nx
import numpy as np
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import graph_operations as go
import run, math
import data_generate as dg


def sample_assign100(fName):
    A, G = go.create_graph_from_text(fName)
    M = bipartite.minimum_weight_full_matching(G)
    sumVal = go.compute_sum_from_matching(A, M)
    return sumVal, A, M, G


def sample_error(A_o):
    G = go.create_graph_from_numpy(A_o)
    M = bipartite.minimum_weight_full_matching(G)
    return M, G


# Creates a list of Matrix A type matrix
def create_pred_matrixA(shape, error_li=[0.1, 0.2, 0.3, 0.4, 0.5]):
    matA = []
    for i in error_li:
        arr = dg.generate_matrixA(shape)
        err_arr = dg.perturb_matrixA(arr, i)
        matA.append(err_arr)
    return matA


def plot_brunel_error():
    file_name_list = [
        "../test/assign100.txt", "../test/assign200.txt",
        "../test/assign300.txt", "../test/assign400.txt",
        "../test/assign500.txt", "../test/assign600.txt",
        "../test/assign700.txt", "../test/assign800.txt"
    ]
    k = 50
    ave0, rmsd = go.iterate_for_different_error(file_name_list, 0, k)
    ave01, rmsd = go.iterate_for_different_error(file_name_list, 0.1, k)
    ave02, rmsd = go.iterate_for_different_error(file_name_list, 0.2, k)
    ave03, rmsd = go.iterate_for_different_error(file_name_list, 0.3, k)
    ave04, rmsd = go.iterate_for_different_error(file_name_list, 0.4, k)
    ave05, rmsd = go.iterate_for_different_error(file_name_list, 0.5, k)
    print(ave0, ave01, ave02, ave03, ave04, ave05)
    plt.plot(ave0)
    plt.plot(ave01)
    plt.plot(ave02)
    plt.plot(ave03)
    plt.plot(ave04)
    plt.plot(ave05)
    plt.ylabel("solution quality")
    plt.xlabel("size (in hundreds - 100")
    plt.title("Brunel Error Graph")
    # y = (2*x)-1
    # plt.plot(x, y, 'g')
    # y = (np.log10(x))*(np.log10(x))
    # plt.plot(x, y, 'g')
    # y = (np.log(x))
    # plt.plot(x, y, 'g')
    plt.legend([
        r'$\epsilon=0$', r'$\epsilon=0.1$', r'$\epsilon=0.2$',
        r'$\epsilon=0.3$', r'$\epsilon=0.4$', r'$\epsilon=0.5$'
    ])
    # plt.savefig("../results/error_graphs/Brunel_error" + "_mu" + str(mu) + "SEED2" + ".png")
    # plt.clf()
    plt.show()
    return


def plot_brunel_size():
    epsilon_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    k = 50
    ave100, rmsd = go.iterate_for_increasing_n_graph("../test/assign100.txt",
                                                     epsilon_list, k)
    ave200, rmsd = go.iterate_for_increasing_n_graph("../test/assign200.txt",
                                                     epsilon_list, k)
    ave300, rmsd = go.iterate_for_increasing_n_graph("../test/assign300.txt",
                                                     epsilon_list, k)
    ave400, rmsd = go.iterate_for_increasing_n_graph("../test/assign400.txt",
                                                     epsilon_list, k)
    ave500, rmsd = go.iterate_for_increasing_n_graph("../test/assign500.txt",
                                                     epsilon_list, k)
    ave600, rmsd = go.iterate_for_increasing_n_graph("../test/assign600.txt",
                                                     epsilon_list, k)
    ave700, rmsd = go.iterate_for_increasing_n_graph("../test/assign700.txt",
                                                     epsilon_list, k)
    ave800, rmsd = go.iterate_for_increasing_n_graph("../test/assign800.txt",
                                                     epsilon_list, k)

    print("Solutions with Advice ")
    print(ave100, ave200, ave300, ave400, ave500, ave600)
    x = np.linspace(0, 0.5, 6)
    plt.plot(x, ave100)
    plt.plot(x, ave200)
    plt.plot(x, ave300)
    plt.plot(x, ave400)
    plt.plot(x, ave500)
    plt.plot(x, ave600)
    plt.plot(x, ave700)
    plt.plot(x, ave800)
    plt.legend([
        'size100', 'size200', 'size300', 'size400', 'size500', 'size600',
        'size700', 'size800'
    ])
    plt.ylabel("solution quality")
    plt.xlabel("error")
    plt.title("Brunel Size Graph")
    plt.show()
    return


def plot_rmsd():
    epsilon_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
    k_list = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
    file_name_list = [
        "../test/assign100.txt", "../test/assign200.txt",
        "../test/assign300.txt", "../test/assign400.txt",
        "../test/assign500.txt", "../test/assign600.txt",
        "../test/assign700.txt", "../test/assign800.txt"
    ]
    sol_list, rmsd_list = go.iterate_get_rmsd(file_name_list, epsilon_list,
                                              k_list)
    np.sort(rmsd_list)
    plt.scatter(rmsd_list, sol_list)
    plt.show()
    # print(rmsd_list)

    return


def main():
    # sumVal, A, M, G = sample_assign100("../test/assign100.txt")
    # A_o, _ = dg.perturb_choice(A, 0.5, 100)
    # M_o, _ = sample_error(A_co)
    # choice = run.generate_choice_matrix(A_o, M_o)
    # pred_sum = np.sum(np.multiply(A, choice))
    # print(pred_sum)
    # sol0, sol1, sol2, sol3, sol4, sol5 = [], [], [], [], [], []
    # arr, graph = go.create_graph_from_text("../test/assign200.txt")
    # optimal_offline = go.compute_from_numpy(arr)
    # print("Optimal solution from Karp: ", optimal_offline[0])

    # plot_brunel_error()
    # plot_brunel_size()
    plot_rmsd()
    # plot_matrixA_size()
    # plot_matrixA_error()
    # plot_brunel_error_2()
    # plot_brunel_size_2()

    # plot_brunel_size_2()
    # plot_brunel_error_2()


if __name__ == "__main__":
    main()
