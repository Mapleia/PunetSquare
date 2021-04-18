# Press Shift+F10 to execute it or replace it with your code.
from itertools import combinations, product
import csv


# + refers to WT
# - refers to Mutated Type
# genes: [{"gene": "", "dom_allele": ["+" or "-"],"rec_allele": ["+" or "-"], "trait_dom": "", "trait_rec": ""}]
def create_allele_array(genes):
    result = []
    for gene in genes:
        result.append({
            "gene": gene["gene"],
            "allele": "{gene}+".format(gene=gene["gene"])
        })
        result.append({
            "gene": gene["gene"],
            "allele": "{gene}-".format(gene=gene["gene"])
        })

    return result


# from a list of genotypes of the offspring and list of genes, create the according phenotype
def create_pheno_list(genotypes, genes):
    dom_alleles = [gene['gene'] + gene['dom_allele'] for gene in genes]
    gene_dict = {}
    for gene in genes:
        gene_dict[gene['gene'] + gene['dom_allele']] = gene['trait_dom']
        gene_dict[gene['gene'] + gene['rec_allele']] = gene['trait_rec']

    list_of_phenotypes = []
    for genotype in genotypes:
        pheno = []
        visited = []
        for allele in genotype:
            if allele not in visited:
                if allele in dom_alleles:
                    pheno.append(gene_dict[allele])
                elif len(list(filter(lambda x: x == allele, genotype))) > 1:
                    pheno.append(gene_dict[allele])
            visited.append(allele)

        list_of_phenotypes.append(" and ".join(pheno))

    print(list_of_phenotypes)
    return list_of_phenotypes


# from a list of alleles and the associated genes, create a .csv file with the punnett square
def create_csv(alleles, num_of_genes, genes):
    # make all of the combos possible
    gametes_raw = list(combinations(alleles, num_of_genes))

    def unique_values(g):
        s = set()
        for x in g:
            if x in s:
                return False
            else:
                s.add(x)
        return True

    # from the combo of dict of alleles, return boolean of if the genes are all unique
    def combo_allele(combo):
        available = [allele['gene'] for allele in combo]
        return unique_values(available)

    # filter for unique gene combos
    gametes_available = list(filter(combo_allele, gametes_raw))

    # make a list of lists containing the alleles
    gametes = [[allele['allele'] for allele in group] for group in gametes_available]
    print('gametes')
    print(gametes)

    # make a table of gametes each crossing each other (products of each other)
    combo_list = [p for p in product(gametes, repeat=2)]
    print('products list')
    print(combo_list)

    def nested_list(convert_me):
        result = []
        for item in convert_me:
            result += item
        return result

    # divide the list into chunks of size n
    def divide_chunks(chunk_me, n):
        # looping till length l
        for i in range(0, len(chunk_me), n):
            yield chunk_me[i:i + n]

    def make_genotype(list_of_alleles):
        # split the list [1, 2, 3, 4] into lists of length 2 [[1, 2], [3, 4]]
        # join the inner list [1, 2] with "", creating a list of [12, 34]
        # join that list by /, creating a string of 12/34 and return it
        return "/".join(["".join(item) for item in divide_chunks(list_of_alleles, 2)])

    # for every row in the list, add a row name from a list of rows (in the same order)
    def add_row_name(rows, row_names):
        i = 0
        while i < len(row_names):
            rows[i] = [row_names[i]] + rows[i]
            i += 1

    # flatten the list of lists with lists [[[], []...], ...] to a singular list [[], []...]
    combos = [nested_list(list(combo)) for combo in combo_list]
    print("combos")
    print(combos)

    print('offspring:')
    # sort the flattened list in alphabetical order
    sorted_combos = [sorted(offspring, key=lambda x: x[:-1]) for offspring in combos]

    phenos = create_pheno_list(sorted_combos, genes)
    # for the list of listed alleles, make a list of genotype strings
    genotypes = [make_genotype(baby) for baby in sorted_combos]
    print(genotypes)

    chunked_geno = list(divide_chunks(genotypes, len(gametes)))
    chunked_pheno = list(divide_chunks(phenos, len(gametes)))
    # for all of the gametes dict, make a string for the gamete
    allele_names = ["".join([allele['allele'] for allele in group]) for group in gametes_available]
    # add extra header
    column_names = ["Gametes"] + allele_names
    # add row name
    add_row_name(chunked_geno, allele_names)
    add_row_name(chunked_pheno, allele_names)

    print(chunked_geno)
    print(chunked_pheno)

    with open('biol_punnett.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        writer.writerows(chunked_geno)
        writer.writerows([" "])
        writer.writerow(column_names)
        writer.writerows(chunked_pheno)

    return column_names + chunked_geno + chunked_pheno


def main(genes):
    allele_list = create_allele_array(genes)
    create_csv(allele_list, len(genes), genes)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    arr_genes = [
        {"gene": "A", "dom_allele": "+", "rec_allele": "-", "trait_dom": "winged", "trait_rec": "shriveled winged"},
        {"gene": "B", "dom_allele": "+", "rec_allele": "-", "trait_dom": "pink", "trait_rec": "blue"},
        {"gene": "C", "dom_allele": "+", "rec_allele": "-", "trait_dom": "horned", "trait_rec": "spiked"}
        ]
    main(arr_genes)
